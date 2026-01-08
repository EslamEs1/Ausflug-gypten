# Test Data Management Commands

## create_test_data

This management command creates comprehensive test data for all models in the AusflugÄgypten project.

### Usage

```bash
# Create test data (default: 10 items per model)
python manage.py create_test_data

# Create more items
python manage.py create_test_data --count=20

# Clear existing data and create new data
python manage.py create_test_data --clear

# Clear and create with custom count
python manage.py create_test_data --clear --count=15
```

### What it creates

The command creates test data for:

1. **Core Models:**
   - SiteSettings (singleton)
   - HeroSlides (3 slides)
   - PageHeroes (for all pages)
   - PageHeroBadges
   - ContactMessages
   - NewsletterSubscribers

2. **Tours App:**
   - Locations (8 locations)
   - TourCategories (8 categories)
   - Tours (with itinerary and inclusions)
   - TourImages (skipped - requires actual images)

3. **Excursions App:**
   - Excursions

4. **Activities App:**
   - ActivityCategories (5 categories)
   - Activities

5. **Transfers App:**
   - TransferTypes (4 types)
   - VehicleTypes (4 types)
   - Transfers (with inclusions)

6. **Gallery App:**
   - GalleryCategories (5 categories)
   - GalleryImages

7. **Blog App:**
   - BlogCategories (5 categories)
   - BlogPosts

8. **Reviews App:**
   - Reviews (for tours, excursions, activities)

9. **Bookings App:**
   - Bookings
   - Payments (for confirmed/completed bookings)

### Important Notes

#### Image Fields

The command creates all data **except actual image files**. Image fields (like `featured_image`, `background_image`, etc.) will be empty and need to be set manually through:

1. **Django Admin:** Upload images through the admin interface
2. **Management Script:** Create a separate script to download placeholder images
3. **Manual Upload:** Use the admin interface to upload real images

#### To add placeholder images:

You can create a simple script to download placeholder images from a service like:
- Unsplash Source API
- Placeholder.com
- Lorem Picsum

Example:
```python
import requests
from django.core.files.base import ContentFile
from apps.tours.models import Tour

for tour in Tour.objects.filter(featured_image=''):
    response = requests.get('https://picsum.photos/800/600')
    tour.featured_image.save(
        f'tour_{tour.id}.jpg',
        ContentFile(response.content),
        save=True
    )
```

### Dependencies

- Faker: For generating realistic test data
- Install with: `pip install Faker==20.1.0`

### Customization

You can modify the command to:
- Add more realistic data patterns
- Include image downloads
- Create specific test scenarios
- Add more relationships between models

### Clearing Data

Use `--clear` flag to remove all existing test data before creating new data. This ensures a clean state.

**Warning:** The `--clear` flag will delete all data from the models listed above. Use with caution in production!

