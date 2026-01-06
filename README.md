# AusflugÄgypten - Premium Egyptian Tourism Platform

A modern, luxury tourism website for Egypt tours and activities, built with Tailwind CSS and designed for Django backend integration.

## 🌟 Project Overview

**Website Type:** Tourism / Egypt Tours & Activities  
**Languages:** German (Primary), English (Secondary)  
**Design:** Modern, Luxury, High-end travel experience  
**Goal:** Compete with and outperform aegyptentouren.de

## 🎨 Design & Branding

### Colors
- **Primary Gold:** `#c8a66e` - Luxurious, warm
- **Primary Blue:** `#245d81` - Deep, trustworthy
- **Secondary Gold Light:** `#d4b886`
- **Secondary Gold Dark:** `#b39456`
- **Secondary Blue Light:** `#2e7aa8`
- **Secondary Blue Dark:** `#1a4660`

### Typography
- **Headings:** Montserrat Bold
- **Body Text:** Lato Regular
- **Arabic Support:** JF-Flat Regular (future use)

### Logo
Egyptian scarab beetle design in diamond frame - premium, distinctive branding.

## 📁 Project Structure

```
AusflugÄgypten/
├── index.html                    # Homepage with all sections
├── pages/
│   ├── activities/               # Activity listings and details
│   ├── excursions/               # Tour listings (location-based)
│   │   └── index.html           # Main tours listing with filters
│   ├── tours/
│   │   └── detail.html          # Tour detail page with booking
│   ├── blog/                     # Blog listings and articles
│   ├── transfer/                 # Transfer services
│   └── contact.html             # Contact page with form
├── css/
│   ├── input.css                # Tailwind input file
│   ├── main.css                 # Compiled Tailwind (generated)
│   └── components.css           # Custom component styles
├── js/
│   └── main.js                  # Main JavaScript functionality
├── fonts/
│   ├── Montserrat-Bold.ttf
│   ├── Lato-Regular.ttf
│   └── JF-Flat-Regular.ttf
├── img/                         # Image assets
│   ├── hero/                    # Hero section images
│   ├── tours/                   # Tour images
│   ├── blog/                    # Blog images
│   ├── categories/              # Category images
│   └── logo/                    # Logo files
├── components/                  # HTML component templates
│   ├── header.html
│   ├── footer.html
│   └── card-templates.html
├── backend/                     # Django backend (Phase 2)
│   ├── config/                  # Project settings
│   │   └── settings.py
│   ├── apps/                    # Django apps
│   │   ├── core/
│   │   ├── tours/
│   │   ├── activities/
│   │   ├── blog/
│   │   ├── transfers/
│   │   ├── reviews/
│   │   ├── bookings/
│   │   └── users/
│   ├── templates/               # Django templates
│   ├── static/                  # Static files
│   └── requirements.txt         # Python dependencies
├── tailwind.config.js           # Tailwind configuration
├── package.json                 # Node.js dependencies
└── README.md                    # This file
```

## 🚀 Getting Started

### Frontend Development

#### Prerequisites
- Node.js 16+ and npm
- Modern web browser

#### Installation

1. **Clone the repository:**
```bash
cd /media/eslames/work/frontend/AusflugÄgypten
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development (watch mode):**
```bash
npm run dev
```

4. **Build for production:**
```bash
npm run build
```

5. **Open in browser:**
```bash
# Open index.html in your browser
# Or use a local server:
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Django Backend Setup

#### Prerequisites
- Python 3.11+
- PostgreSQL (for production) or SQLite (for development)

#### Installation

1. **Create virtual environment:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

Example `.env` file:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for dev, PostgreSQL for production)
DB_NAME=ausflug_egypt
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@ausflugagypten.com

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Collect static files:**
```bash
python manage.py collectstatic
```

7. **Run development server:**
```bash
python manage.py runserver
```

8. **Access admin panel:**
```
http://localhost:8000/admin/
```

## 📄 Pages Implemented

### Homepage (`index.html`)
- ✅ Hero section with rotating backgrounds
- ✅ Trust bar (stats)
- ✅ Featured tours section
- ✅ Destination categories
- ✅ Why choose us section
- ✅ Customer testimonials
- ✅ Blog preview
- ✅ Newsletter signup
- ✅ Footer with all links

### Tours Listing (`pages/excursions/index.html`)
- ✅ Hero banner with breadcrumb
- ✅ Filter sidebar (category, location, price, rating)
- ✅ Tours grid (3 columns responsive)
- ✅ Pagination
- ✅ Sorting options

### Tour Detail (`pages/tours/detail.html`)
- ✅ Image gallery
- ✅ Tour information
- ✅ Quick facts grid
- ✅ Full description
- ✅ Itinerary timeline
- ✅ Included/Excluded lists
- ✅ Customer reviews
- ✅ Booking sidebar with form
- ✅ Sticky booking button

### Contact Page (`pages/contact.html`)
- ✅ Contact form
- ✅ Contact information cards
- ✅ Opening hours
- ✅ Google Maps integration ready

## 🎯 Key Features

### Frontend Features
- ✅ Responsive design (mobile-first)
- ✅ Tailwind CSS with custom configuration
- ✅ Custom components (cards, buttons, forms)
- ✅ Image lazy loading
- ✅ Smooth scroll animations
- ✅ Mobile navigation menu
- ✅ Language switcher (DE/EN)
- ✅ Wishlist functionality
- ✅ Filter system for listings
- ✅ Testimonial carousel
- ✅ WhatsApp floating button
- ✅ Newsletter subscription

### Backend Features
- ✅ Django 4.2+ with modern structure
- ✅ PostgreSQL support
- ✅ Multilingual (DE/EN) setup
- ✅ Complete tour management
- ✅ Blog system
- ✅ Review system (generic)
- ✅ Booking system
- ✅ Stripe payment integration
- ✅ Admin interface customization
- ✅ SEO-friendly URLs (slugs)
- ✅ Image upload handling
- ✅ Email notifications ready

## 📊 Database Models

### Tours App
- **Location** - Tour locations (Hurghada, Luxor, Cairo, etc.)
- **TourCategory** - Categories (Cultural, Snorkeling, Safari, etc.)
- **Tour** - Main tour model with all details
- **TourImage** - Additional tour images
- **Itinerary** - Tour schedule/timeline
- **TourInclusion** - What's included/excluded

### Blog App
- **BlogCategory** - Blog categories
- **BlogPost** - Blog articles with multilingual support

### Reviews App
- **Review** - Generic review model (works with any content)

### Bookings App
- **Booking** - Tour bookings
- **Payment** - Stripe payment tracking

## 🔧 JavaScript Functionality

### Main Features (`js/main.js`)
- Header sticky/scroll behavior
- Mobile menu toggle
- Language switcher with localStorage
- Hero slider with auto-play
- Wishlist system (localStorage)
- Testimonial carousel
- Accordion components
- Animate on scroll (intersection observer)
- Image lazy loading
- Filter system for listings
- Smooth scroll for anchor links
- Form validation
- Modal system
- Newsletter subscription

## 🎨 CSS Components

### Tailwind Utilities
- Custom colors (primary-gold, primary-blue)
- Custom fonts (heading, body, arabic)
- Animation classes (fade-in, slide-up, scale-in)

### Custom Components (`css/components.css`)
- Hero slider
- Tour cards with hover effects
- Category cards
- Testimonial cards
- Filter sections
- Timeline (itinerary)
- Accordion
- Mobile menu
- Pagination
- Modal
- Trust badges
- WhatsApp float button

## 🌐 Multilingual Support

### Frontend
- Language switcher in header (DE/EN)
- LocalStorage for language preference
- Content can be switched dynamically (future implementation)

### Backend
- Django i18n framework
- Separate fields for DE/EN content
- URL patterns: `/de/touren/` and `/en/tours/`
- Language middleware enabled

## 💳 Stripe Integration

### Frontend
Modal-based checkout flow:
1. User fills booking form
2. Click "Buchen" button
3. Stripe Checkout modal opens
4. Payment processed
5. Redirect to confirmation page

### Backend
```python
# bookings/views.py
class CreateCheckoutSessionView(View):
    def post(self, request, tour_id):
        # Create Stripe session
        # Return session ID
        # Frontend redirects to Stripe
```

## 📱 Responsive Breakpoints

- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px
- **Large Desktop:** > 1280px

## 🚦 Next Steps

### Phase 1: Frontend (COMPLETED ✅)
- [x] Tailwind CSS setup
- [x] Homepage with all sections
- [x] Listing pages
- [x] Detail pages
- [x] Contact and support pages
- [x] Responsive design

### Phase 2: Django Backend (COMPLETED ✅)
- [x] Project structure
- [x] Database models
- [x] Admin panel
- [x] Settings configuration

### Phase 3: Integration (TODO)
- [ ] Convert HTML to Django templates
- [ ] Create views (Class-based)
- [ ] URL routing
- [ ] Form handling
- [ ] Stripe webhook implementation
- [ ] Email notifications
- [ ] Image optimization

### Phase 4: Content & Testing (TODO)
- [ ] Seed database with tours
- [ ] Add blog articles
- [ ] Test booking flow
- [ ] Test payment integration
- [ ] Cross-browser testing
- [ ] Performance optimization

### Phase 5: Deployment (TODO)
- [ ] Setup production server
- [ ] Configure PostgreSQL
- [ ] Setup Gunicorn + Nginx
- [ ] SSL certificate
- [ ] Domain configuration
- [ ] CDN for media files

## 🛡️ Security Checklist

- [ ] SECRET_KEY in environment variable
- [ ] DEBUG=False in production
- [ ] HTTPS enforcement
- [ ] CSRF protection enabled
- [ ] SQL injection prevention (ORM)
- [ ] XSS protection
- [ ] Secure cookies
- [ ] Rate limiting
- [ ] Input validation
- [ ] File upload restrictions

## 📈 SEO Optimization

- ✅ Semantic HTML5 structure
- ✅ Meta tags (title, description, keywords)
- ✅ Open Graph tags
- ✅ Clean URL structure (slugs)
- ✅ Image alt texts
- ⏳ Schema.org structured data (TODO)
- ⏳ XML sitemap (TODO)
- ⏳ Robots.txt (TODO)
- ⏳ hreflang tags for multilingual (TODO)

## 🎯 Performance

- ✅ Lazy loading images
- ✅ Minified CSS (production)
- ✅ CSS custom properties
- ✅ Intersection Observer for animations
- ⏳ Image optimization (WebP) (TODO)
- ⏳ CDN integration (TODO)
- ⏳ Browser caching (TODO)
- ⏳ Gzip compression (TODO)

## 📞 Support & Contact

For any questions or issues:
- **Email:** info@ausflugagypten.com
- **Phone:** +20 123 456 7890
- **WhatsApp:** [Click to Chat](https://wa.me/201234567890)

## 📝 License

© 2024 AusflugÄgypten. All rights reserved.

---

**Built with:** HTML5, CSS3, Tailwind CSS, Vanilla JavaScript, Django, PostgreSQL, Stripe  
**Design:** Modern Luxury Tourism Experience  
**Status:** Phase 1 & 2 Complete - Ready for Integration

