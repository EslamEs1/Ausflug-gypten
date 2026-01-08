"""
Management command to create test data for all models in the project.
Usage: python manage.py create_test_data [--clear] [--count=N]
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from decimal import Decimal
from datetime import timedelta
import random
import uuid
from io import BytesIO
from PIL import Image

from faker import Faker

# Import all models
from apps.core.models import (
    SiteSettings, HeroSlide, ContactMessage, NewsletterSubscriber,
    PageHero, PageHeroBadge
)
from apps.tours.models import Location, TourCategory, Tour, TourImage, Itinerary, TourInclusion
from apps.excursions.models import Excursion
from apps.blog.models import BlogCategory, BlogPost
from apps.activities.models import ActivityCategory, Activity, ActivityImage, ActivityInclusion, ActivityImportantInfo
from apps.transfers.models import TransferType, VehicleType, Transfer, TransferImage, TransferInclusion, TransferImportantInfo, TransferRoute
from apps.gallery.models import GalleryCategory, GalleryImage
from apps.reviews.models import Review
from apps.bookings.models import Booking, Payment

User = get_user_model()
fake = Faker(['de_DE', 'en_US'])


def create_placeholder_image(width=800, height=600, color=(52, 152, 219)):
    """Create a simple placeholder image"""
    img = Image.new('RGB', (width, height), color=color)
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=f'placeholder_{uuid.uuid4().hex[:8]}.jpg')


class Command(BaseCommand):
    help = 'Creates test data for all models in the project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of items to create for each model (default: 10)',
        )

    def handle(self, *args, **options):
        clear = options['clear']
        count = options['count']
        
        self.stdout.write(self.style.SUCCESS('Starting test data creation...'))
        
        # Check if migrations are up to date
        from django.db import connection
        tables = connection.introspection.table_names()
        required_tables = ['core_pagehero', 'tours_location', 'tours_tour']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            self.stdout.write(
                self.style.ERROR(
                    f'\n❌ Missing database tables: {", ".join(missing_tables)}\n'
                    'Please run migrations first: python manage.py migrate'
                )
            )
            return
        
        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()
        
        # Create data in order of dependencies
        self.create_site_settings()
        self.create_locations(count)
        self.create_tour_categories(count)
        self.create_activity_categories(count)
        self.create_transfer_types(count)
        self.create_vehicle_types()
        self.create_gallery_categories(count)
        self.create_blog_categories(count)
        
        self.create_hero_slides()
        self.create_page_heroes()
        
        locations = Location.objects.all()
        tour_categories = TourCategory.objects.all()
        activity_categories = ActivityCategory.objects.all()
        transfer_types = TransferType.objects.all()
        vehicle_types = VehicleType.objects.all()
        gallery_categories = GalleryCategory.objects.all()
        blog_categories = BlogCategory.objects.all()
        
        self.create_tours(count, locations, tour_categories)
        self.create_excursions(count, locations, tour_categories)
        self.create_activities(count, locations, activity_categories)
        self.create_transfers(count, locations, transfer_types, vehicle_types)
        self.create_gallery_images(count * 2, locations, gallery_categories)
        
        # Get a user for blog posts
        user = self.get_or_create_user()
        self.create_blog_posts(count, blog_categories, user)
        
        # Create reviews for tours
        tours = Tour.objects.all()
        excursions = Excursion.objects.all()
        activities = Activity.objects.all()
        self.create_reviews(count * 3, tours, excursions, activities)
        
        # Create bookings
        self.create_bookings(count, tours)
        
        # Create contact messages
        self.create_contact_messages(count)
        
        # Create newsletter subscribers
        self.create_newsletter_subscribers(count)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created test data!'))
        self.stdout.write(self.style.SUCCESS(f'Created {count} items for each main model.'))

    def clear_data(self):
        """Clear all test data"""
        try:
            Payment.objects.all().delete()
            Booking.objects.all().delete()
            Review.objects.all().delete()
            GalleryImage.objects.all().delete()
            TransferRoute.objects.all().delete()
            TransferImportantInfo.objects.all().delete()
            TransferInclusion.objects.all().delete()
            TransferImage.objects.all().delete()
            Transfer.objects.all().delete()
            ActivityImportantInfo.objects.all().delete()
            ActivityInclusion.objects.all().delete()
            ActivityImage.objects.all().delete()
            Activity.objects.all().delete()
            BlogPost.objects.all().delete()
            TourInclusion.objects.all().delete()
            Itinerary.objects.all().delete()
            TourImage.objects.all().delete()
            Tour.objects.all().delete()
            Excursion.objects.all().delete()
            PageHeroBadge.objects.all().delete()
            PageHero.objects.all().delete()
            HeroSlide.objects.all().delete()
            NewsletterSubscriber.objects.all().delete()
            ContactMessage.objects.all().delete()
            GalleryCategory.objects.all().delete()
            VehicleType.objects.all().delete()
            TransferType.objects.all().delete()
            ActivityCategory.objects.all().delete()
            BlogCategory.objects.all().delete()
            TourCategory.objects.all().delete()
            Location.objects.all().delete()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Some tables may not exist yet: {e}'))

    def get_or_create_user(self):
        """Get or create a test user"""
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@ausflugagypten.com',
                'first_name': 'Test',
                'last_name': 'User',
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
        return user

    def create_site_settings(self):
        """Create or update site settings"""
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'AusflugÄgypten',
                'site_title': 'AusflugÄgypten - Touren, Ausflüge & Aktivitäten in Ägypten',
                'site_description': 'Entdecken Sie die besten Touren und Ausflüge in Ägypten',
                'address': 'Hurghada, Ägypten',
                'phone': '+20 123 456 7890',
                'email': 'info@ausflugagypten.com',
                'whatsapp': '+201234567890',
            }
        )
        if created:
            self.stdout.write('✓ Created SiteSettings')

    def create_locations(self, count):
        """Create locations"""
        locations_data = [
            ('Hurghada', 'Hurghada'),
            ('Luxor', 'Luxor'),
            ('Kairo', 'Cairo'),
            ('Sharm El Sheikh', 'Sharm El Sheikh'),
            ('Marsa Alam', 'Marsa Alam'),
            ('Aswan', 'Aswan'),
            ('Alexandria', 'Alexandria'),
            ('Dahab', 'Dahab'),
        ]
        
        for i, (name_de, name_en) in enumerate(locations_data[:count]):
            Location.objects.get_or_create(
                slug=f"{name_de.lower().replace(' ', '-')}",
                defaults={
                    'name': name_de,
                    'name_en': name_en,
                    'description': fake.text(max_nb_chars=200),
                    'description_en': fake.text(max_nb_chars=200),
                    'is_active': True,
                    'order': i,
                }
            )
        self.stdout.write(f'✓ Created {Location.objects.count()} locations')

    def create_tour_categories(self, count):
        """Create tour categories"""
        categories_data = [
            ('Kultur & Geschichte', 'Culture & History', '🏛️'),
            ('Schnorcheln & Tauchen', 'Snorkeling & Diving', '🏊'),
            ('Wüsten-Safari', 'Desert Safari', '🏜️'),
            ('Bootstouren', 'Boat Tours', '⛵'),
            ('Stadtrundfahrten', 'City Tours', '🚌'),
            ('Abenteuer', 'Adventure', '🎢'),
            ('Wellness & Entspannung', 'Wellness & Relaxation', '🧘'),
            ('Nachtleben', 'Nightlife', '🌃'),
        ]
        
        for i, (name_de, name_en, icon) in enumerate(categories_data[:count]):
            TourCategory.objects.get_or_create(
                slug=f"{name_de.lower().replace(' ', '-').replace('&', '')}",
                defaults={
                    'name': name_de,
                    'name_en': name_en,
                    'description': fake.text(max_nb_chars=200),
                    'description_en': fake.text(max_nb_chars=200),
                    'icon': icon,
                    'is_active': True,
                    'order': i,
                }
            )
        self.stdout.write(f'✓ Created {TourCategory.objects.count()} tour categories')

    def create_activity_categories(self, count):
        """Create activity categories"""
        categories_data = [
            ('Schnorcheln', 'Snorkeling', '🏊', 'primary-blue'),
            ('Kultur', 'Culture', '🏛️', 'primary-gold'),
            ('Safari', 'Safari', '🏜️', 'orange-600'),
            ('Wassersport', 'Water Sports', '🏄', 'primary-blue'),
            ('Abenteuer', 'Adventure', '🎢', 'primary-gold'),
        ]
        
        for i, (name_de, name_en, icon, gradient) in enumerate(categories_data[:count]):
            ActivityCategory.objects.get_or_create(
                slug=f"{name_de.lower().replace(' ', '-')}",
                defaults={
                    'name': name_de,
                    'name_en': name_en,
                    'description': fake.text(max_nb_chars=200),
                    'description_en': fake.text(max_nb_chars=200),
                    'icon': icon,
                    'gradient_color': gradient,
                    'is_active': True,
                    'order': i,
                }
            )
        self.stdout.write(f'✓ Created {ActivityCategory.objects.count()} activity categories')

    def create_transfer_types(self, count):
        """Create transfer types"""
        types_data = [
            ('Flughafen Transfer', 'Airport Transfer', '✈️'),
            ('Hotel Transfer', 'Hotel Transfer', '🏨'),
            ('Privat Transfer', 'Private Transfer', '🚗'),
            ('Gruppen Transfer', 'Group Transfer', '🚌'),
        ]
        
        for i, (name_de, name_en, icon) in enumerate(types_data[:count]):
            TransferType.objects.get_or_create(
                slug=f"{name_de.lower().replace(' ', '-')}",
                defaults={
                    'name': name_de,
                    'name_en': name_en,
                    'description': fake.text(max_nb_chars=200),
                    'description_en': fake.text(max_nb_chars=200),
                    'icon': icon,
                    'is_active': True,
                    'order': i,
                }
            )
        self.stdout.write(f'✓ Created {TransferType.objects.count()} transfer types')

    def create_vehicle_types(self):
        """Create vehicle types"""
        vehicles_data = [
            ('Limousine', 'Limousine', 3, 3, '🚗'),
            ('SUV', 'SUV', 5, 4, '🚙'),
            ('Minivan', 'Minivan', 8, 6, '🚐'),
            ('Bus', 'Bus', 50, 50, '🚌'),
        ]
        
        for i, (name_de, name_en, capacity, luggage, icon) in enumerate(vehicles_data):
            VehicleType.objects.get_or_create(
                slug=f"{name_de.lower()}",
                defaults={
                    'name': name_de,
                    'name_en': name_en,
                    'capacity': capacity,
                    'luggage_capacity': luggage,
                    'description': fake.text(max_nb_chars=200),
                    'icon': icon,
                    'is_active': True,
                    'order': i,
                }
            )
        self.stdout.write(f'✓ Created {VehicleType.objects.count()} vehicle types')

    def create_gallery_categories(self, count):
        """Create gallery categories"""
        categories_data = [
            ('Hurghada', 'Hurghada', '🏖️'),
            ('Luxor', 'Luxor', '🏛️'),
            ('Wüste', 'Desert', '🏜️'),
            ('Unterwasser', 'Underwater', '🐠'),
            ('Kultur', 'Culture', '🎭'),
        ]
        
        for i, (name_de, name_en, icon) in enumerate(categories_data[:count]):
            GalleryCategory.objects.get_or_create(
                slug=f"{name_de.lower().replace(' ', '-')}",
                defaults={
                    'name': name_de,
                    'name_en': name_en,
                    'description': fake.text(max_nb_chars=200),
                    'description_en': fake.text(max_nb_chars=200),
                    'icon': icon,
                    'is_active': True,
                    'order': i,
                }
            )
        self.stdout.write(f'✓ Created {GalleryCategory.objects.count()} gallery categories')

    def create_blog_categories(self, count):
        """Create blog categories"""
        categories_data = [
            ('Reisetipps', 'Travel Tips'),
            ('Kultur & Geschichte', 'Culture & History'),
            ('Aktivitäten', 'Activities'),
            ('Reiseführer', 'Travel Guide'),
            ('News', 'News'),
        ]
        
        for name_de, name_en in categories_data[:count]:
            BlogCategory.objects.get_or_create(
                slug=f"{name_de.lower().replace(' ', '-').replace('&', '')}",
                defaults={
                    'name': name_de,
                    'name_en': name_en,
                    'description': fake.text(max_nb_chars=200),
                    'is_active': True,
                }
            )
        self.stdout.write(f'✓ Created {BlogCategory.objects.count()} blog categories')

    def create_hero_slides(self):
        """Create hero slides"""
        slides_data = [
            {
                'title': 'Entdecken Sie das magische Ägypten',
                'subtitle': 'Erleben Sie unvergessliche Abenteuer mit unseren exklusiven Touren und Ausflügen',
                'button_1_text': 'Touren Entdecken',
                'button_1_url': 'excursions:list',
                'button_1_style': 'primary',
                'button_2_text': 'Kontakt Aufnehmen',
                'button_2_url': 'core:contact',
                'button_2_style': 'outline',
                'order': 0,
            },
            {
                'title': 'Luxor - Die Stadt der Pharaonen',
                'subtitle': 'Tauchen Sie ein in 5000 Jahre Geschichte',
                'button_1_text': 'Kulturtouren Ansehen',
                'button_1_url': 'activities:list',
                'button_1_style': 'primary',
                'order': 1,
            },
            {
                'title': 'Wüsten-Abenteuer erleben',
                'subtitle': 'Safari-Touren durch die majestätische Wüste Ägyptens',
                'button_1_text': 'Safari Buchen',
                'button_1_url': 'activities:list',
                'button_1_style': 'primary',
                'order': 2,
            },
        ]
        
        for slide_data in slides_data:
            HeroSlide.objects.get_or_create(
                title=slide_data['title'],
                defaults={
                    **slide_data,
                    'image': create_placeholder_image(),
                    'is_active': True,
                }
            )
        self.stdout.write(f'✓ Created {HeroSlide.objects.count()} hero slides')

    def create_page_heroes(self):
        """Create page heroes"""
        try:
            heroes_data = [
            {
                'page': 'excursions',
                'title': 'Ägypten Ausflüge & Touren',
                'subtitle': 'Entdecken Sie die besten Ausflüge in Ägypten - von historischen Stätten bis zu Wüstenabenteuern',
                'breadcrumb_text': 'Ägypten Ausflüge',
                'height': '450px',
                'overlay_opacity': '0.7',
                'badges': [
                    {'text': 'Zertifiziert', 'icon': '✓', 'order': 0},
                    {'text': 'Sofortige Bestätigung', 'icon': '⏰', 'order': 1},
                    {'text': 'Beste Preise', 'icon': '€', 'order': 2},
                ]
            },
            {
                'page': 'blog',
                'title': 'Ägypten & Hurghada Reiseblog',
                'subtitle': 'Tipps, Infos und Inspiration für Ihre Ägypten-Reise',
                'breadcrumb_text': 'Blog',
                'height': '400px',
                'overlay_opacity': '0.8',
            },
            {
                'page': 'gallery',
                'title': 'Galerie',
                'subtitle': 'Entdecken Sie die Schönheit Ägyptens in unseren Fotos',
                'breadcrumb_text': 'Galerie',
                'height': '450px',
                'overlay_opacity': '0.8',
            },
            {
                'page': 'transfers',
                'title': 'Transfer Service in Ägypten',
                'subtitle': 'Zuverlässig, komfortabel und pünktlich - Ihr Transfer-Partner in Ägypten',
                'breadcrumb_text': 'Transfer',
                'height': '500px',
                'overlay_opacity': '0.8',
            },
            {
                'page': 'activities',
                'title': 'Ägypten Aktivitäten & Sehenswürdigkeiten',
                'subtitle': 'Erleben Sie unvergessliche Abenteuer - von Schnorcheln im Roten Meer bis zu Wüsten-Safaris',
                'breadcrumb_text': 'Ägypten Aktivitäten',
                'height': '500px',
                'overlay_opacity': '0.7',
            },
        ]
        
            for hero_data in heroes_data:
                badges = hero_data.pop('badges', [])
                hero, created = PageHero.objects.get_or_create(
                    page=hero_data['page'],
                    defaults={
                        **hero_data,
                        'background_image': create_placeholder_image(),
                        'is_active': True,
                    }
                )
                if created and badges:
                    for badge_data in badges:
                        PageHeroBadge.objects.create(
                            page_hero=hero,
                            **badge_data
                        )
            self.stdout.write(f'✓ Created {PageHero.objects.count()} page heroes')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create page heroes: {e}'))

    def create_tours(self, count, locations, categories):
        """Create tours"""
        group_types = ['private', 'small_group', 'group']
        durations = ['4 Stunden', '8 Stunden', 'Tagesausflug', '2 Tage', '3 Tage']
        
        for i in range(count):
            location = random.choice(locations)
            category = random.choice(categories) if categories.exists() else None
            
            title_de = f"{fake.catch_phrase()} in {location.name}"
            title_en = f"{fake.catch_phrase()} in {location.name_en}"
            
            # Ensure unique slug
            base_slug = slugify(title_de)
            slug = base_slug
            counter = 1
            while Tour.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            price = Decimal(random.randint(30, 500))
            original_price = price * Decimal('1.2') if random.choice([True, False]) else None
            
            tour = Tour.objects.create(
                title=title_de,
                title_en=title_en,
                slug=slug,
                description=fake.text(max_nb_chars=1000),
                description_en=fake.text(max_nb_chars=1000),
                short_description=fake.sentence(),
                short_description_en=fake.sentence(),
                location=location,
                category=category,
                featured_image=create_placeholder_image(),
                price=price,
                original_price=original_price,
                duration=random.choice(durations),
                group_type=random.choice(group_types),
                max_participants=random.randint(10, 50),
                min_age=random.choice([0, 6, 12, 18]),
                languages='Deutsch, English',
                available_days='Täglich',
                pickup_included=random.choice([True, False]),
                is_featured=random.choice([True, False]),
                is_active=True,
            )
            
            # Create itinerary items
            for j in range(random.randint(3, 6)):
                Itinerary.objects.create(
                    tour=tour,
                    time=f"{8 + j * 2}:00",
                    title=fake.sentence(nb_words=4),
                    title_en=fake.sentence(nb_words=4),
                    description=fake.text(max_nb_chars=200),
                    description_en=fake.text(max_nb_chars=200),
                    order=j,
                )
            
            # Create inclusions
            included_items = [
                ('Abholung vom Hotel', 'Hotel Pickup'),
                ('Professioneller Guide', 'Professional Guide'),
                ('Eintrittskarten', 'Entrance Tickets'),
                ('Mittagessen', 'Lunch'),
                ('Getränke', 'Drinks'),
            ]
            excluded_items = [
                ('Persönliche Ausgaben', 'Personal Expenses'),
                ('Trinkgeld', 'Tips'),
            ]
            
            for k, (item_de, item_en) in enumerate(included_items[:random.randint(3, 5)]):
                TourInclusion.objects.create(
                    tour=tour,
                    item=item_de,
                    item_en=item_en,
                    is_included=True,
                    order=k,
                )
            
            for k, (item_de, item_en) in enumerate(excluded_items):
                TourInclusion.objects.create(
                    tour=tour,
                    item=item_de,
                    item_en=item_en,
                    is_included=False,
                    order=k,
                )
        
        self.stdout.write(f'✓ Created {Tour.objects.count()} tours')

    def create_excursions(self, count, locations, categories):
        """Create excursions"""
        group_types = ['private', 'small_group', 'group']
        durations = ['4 Stunden', '8 Stunden', 'Tagesausflug']
        
        for i in range(count):
            location = random.choice(locations)
            category = random.choice(categories) if categories.exists() else None
            
            title_de = f"{fake.catch_phrase()} - {location.name}"
            title_en = f"{fake.catch_phrase()} - {location.name_en}"
            
            # Ensure unique slug
            base_slug = slugify(title_de)
            slug = base_slug
            counter = 1
            while Excursion.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            price = Decimal(random.randint(25, 400))
            original_price = price * Decimal('1.15') if random.choice([True, False]) else None
            
            Excursion.objects.create(
                title=title_de,
                title_en=title_en,
                slug=slug,
                description=fake.text(max_nb_chars=1000),
                description_en=fake.text(max_nb_chars=1000),
                short_description=fake.sentence(),
                short_description_en=fake.sentence(),
                location=location,
                category=category,
                featured_image=create_placeholder_image(),
                price=price,
                original_price=original_price,
                duration=random.choice(durations),
                group_type=random.choice(group_types),
                max_participants=random.randint(10, 40),
                min_age=random.choice([0, 6, 12]),
                languages='Deutsch, English',
                available_days='Täglich',
                pickup_included=True,
                is_featured=random.choice([True, False]),
                is_popular=random.choice([True, False]),
                is_bestseller=random.choice([True, False]),
                is_active=True,
            )
        
        self.stdout.write(f'✓ Created {Excursion.objects.count()} excursions')

    def create_activities(self, count, locations, categories):
        """Create activities"""
        group_sizes = ['Privat', 'Klein', 'Mittel', 'Groß']
        
        for i in range(count):
            location = random.choice(locations) if locations.exists() else None
            category = random.choice(categories) if categories.exists() else None
            
            title_de = f"{fake.catch_phrase()}"
            title_en = f"{fake.catch_phrase()}"
            
            # Ensure unique slug
            base_slug = slugify(title_de)
            slug = base_slug
            counter = 1
            while Activity.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            price = Decimal(random.randint(20, 300))
            discount_price = price * Decimal('0.85') if random.choice([True, False]) else None
            
            Activity.objects.create(
                title=title_de,
                title_en=title_en,
                slug=slug,
                short_description=fake.sentence(),
                short_description_en=fake.sentence(),
                description=fake.text(max_nb_chars=1000),
                description_en=fake.text(max_nb_chars=1000),
                category=category,
                location=location,
                featured_image=create_placeholder_image(),
                price=price,
                discount_price=discount_price,
                duration_hours=random.randint(2, 8),
                group_size=random.choice(group_sizes),
                languages='DE, EN',
                pickup_included=random.choice([True, False]),
                is_featured=random.choice([True, False]),
                is_popular=random.choice([True, False]),
                is_active=True,
            )
        
        self.stdout.write(f'✓ Created {Activity.objects.count()} activities')

    def create_transfers(self, count, locations, transfer_types, vehicle_types):
        """Create transfers"""
        for i in range(count):
            transfer_type = random.choice(transfer_types) if transfer_types.exists() else None
            vehicle_type = random.choice(vehicle_types) if vehicle_types.exists() else None
            from_location = random.choice(locations) if locations.exists() else None
            to_location = random.choice(locations) if locations.exists() else None
            
            # Make title unique to avoid slug conflicts
            base_title = f"Transfer {from_location.name if from_location else 'Hurghada'} → {to_location.name if to_location else 'Flughafen'}"
            title_de = f"{base_title} #{i+1}" if i > 0 else base_title
            title_en = f"Transfer {from_location.name_en if from_location else 'Hurghada'} → {to_location.name_en if to_location else 'Airport'}"
            if i > 0:
                title_en = f"{title_en} #{i+1}"
            
            # Generate unique slug
            from django.utils.text import slugify
            base_slug = slugify(title_de)
            slug = base_slug
            counter = 1
            while Transfer.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            base_price = Decimal(random.randint(20, 200))
            discount_price = base_price * Decimal('0.9') if random.choice([True, False]) else None
            
            transfer = Transfer.objects.create(
                title=title_de,
                title_en=title_en,
                slug=slug,
                short_description=fake.sentence(),
                short_description_en=fake.sentence(),
                description=fake.text(max_nb_chars=500),
                description_en=fake.text(max_nb_chars=500),
                transfer_type=transfer_type,
                vehicle_type=vehicle_type,
                from_location=from_location,
                to_location=to_location,
                base_price=base_price,
                discount_price=discount_price,
                price_per_person=random.choice([True, False]),
                duration_minutes=random.randint(15, 120),
                availability='24/7',
                languages='DE, EN',
                free_cancellation=random.choice([True, False]),
                flight_monitoring=random.choice([True, False]),
                meet_greet=random.choice([True, False]),
                is_featured=random.choice([True, False]),
                is_popular=random.choice([True, False]),
                is_active=True,
            )
            
            # Create inclusions
            inclusions = [
                ('Klimatisiertes Fahrzeug', 'Air-conditioned Vehicle'),
                ('Professioneller Fahrer', 'Professional Driver'),
                ('Versicherung', 'Insurance'),
            ]
            
            for j, (title_de, title_en) in enumerate(inclusions):
                TransferInclusion.objects.create(
                    transfer=transfer,
                    title=title_de,
                    title_en=title_en,
                    order=j,
                )
        
        self.stdout.write(f'✓ Created {Transfer.objects.count()} transfers')

    def create_gallery_images(self, count, locations, categories):
        """Create gallery images"""
        for i in range(count):
            location = random.choice(locations) if locations.exists() else None
            category = random.choice(categories) if categories.exists() else None
            
            title_de = f"{fake.catch_phrase()} - {location.name if location else 'Ägypten'}"
            title_en = f"{fake.catch_phrase()} - {location.name_en if location else 'Egypt'}"
            
            GalleryImage.objects.create(
                title=title_de,
                title_en=title_en,
                description=fake.text(max_nb_chars=200),
                description_en=fake.text(max_nb_chars=200),
                image=create_placeholder_image(),
                category=category,
                location=location,
                photographer=fake.name(),
                taken_at=fake.date_between(start_date='-2y', end_date='today'),
                alt_text=title_de,
                is_featured=random.choice([True, False]),
                is_active=True,
                order=i,
            )
        
        self.stdout.write(f'✓ Created {GalleryImage.objects.count()} gallery images')

    def create_blog_posts(self, count, categories, user):
        """Create blog posts"""
        for i in range(count):
            category = random.choice(categories) if categories.exists() else None
            
            title_de = f"{fake.sentence(nb_words=6)}"
            title_en = f"{fake.sentence(nb_words=6)}"
            
            # Ensure unique slug
            base_slug = slugify(title_de)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            published_at = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc) if random.choice([True, False]) else None
            
            BlogPost.objects.create(
                title=title_de,
                title_en=title_en,
                slug=slug,
                content=fake.text(max_nb_chars=2000),
                content_en=fake.text(max_nb_chars=2000),
                excerpt=fake.sentence(),
                excerpt_en=fake.sentence(),
                featured_image=create_placeholder_image(),
                category=category,
                author=user,
                published_at=published_at,
                is_published=published_at is not None,
                reading_time=random.randint(3, 15),
            )
        
        self.stdout.write(f'✓ Created {BlogPost.objects.count()} blog posts')

    def create_reviews(self, count, tours, excursions, activities):
        """Create reviews"""
        all_items = list(tours) + list(excursions) + list(activities)
        
        for i in range(count):
            if not all_items:
                break
            
            item = random.choice(all_items)
            content_type = ContentType.objects.get_for_model(item)
            
            Review.objects.create(
                content_type=content_type,
                object_id=item.id,
                name=fake.name(),
                email=fake.email(),
                rating=random.randint(3, 5),
                title=fake.sentence(nb_words=4),
                comment=fake.text(max_nb_chars=300),
                is_approved=random.choice([True, True, True, False]),  # 75% approved
            )
        
        self.stdout.write(f'✓ Created {Review.objects.count()} reviews')

    def create_bookings(self, count, tours):
        """Create bookings"""
        statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        
        for i in range(count):
            if not tours.exists():
                break
            
            tour = random.choice(tours)
            participants = random.randint(1, 8)
            total_price = tour.price * participants
            
            booking = Booking.objects.create(
                tour=tour,
                customer_name=fake.name(),
                customer_email=fake.email(),
                customer_phone=fake.phone_number(),
                booking_date=fake.date_between(start_date='today', end_date='+3m'),
                number_of_participants=participants,
                total_price=total_price,
                status=random.choice(statuses),
                special_requests=fake.text(max_nb_chars=200) if random.choice([True, False]) else '',
            )
            
            # Create payment for confirmed/completed bookings
            if booking.status in ['confirmed', 'completed']:
                Payment.objects.create(
                    booking=booking,
                    stripe_payment_intent_id=f'pi_{uuid.uuid4().hex[:24]}',
                    amount=total_price,
                    status='succeeded',
                    paid_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                )
        
        self.stdout.write(f'✓ Created {Booking.objects.count()} bookings')

    def create_contact_messages(self, count):
        """Create contact messages"""
        subjects = ['tour_booking', 'general_inquiry', 'complaint', 'other']
        statuses = ['new', 'read', 'replied', 'archived']
        
        for i in range(count):
            ContactMessage.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number() if random.choice([True, False]) else '',
                subject=random.choice(subjects),
                message=fake.text(max_nb_chars=500),
                status=random.choice(statuses),
                is_read=random.choice([True, False]),
            )
        
        self.stdout.write(f'✓ Created {ContactMessage.objects.count()} contact messages')

    def create_newsletter_subscribers(self, count):
        """Create newsletter subscribers"""
        for i in range(count):
            NewsletterSubscriber.objects.get_or_create(
                email=fake.email(),
                defaults={
                    'is_active': random.choice([True, True, False]),  # 66% active
                }
            )
        
        self.stdout.write(f'✓ Created {NewsletterSubscriber.objects.count()} newsletter subscribers')

