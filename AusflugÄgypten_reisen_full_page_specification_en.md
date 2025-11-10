# SakkaraReisen — Full Page Specification (EN)
Our website name AusflugÄgypten
**Purpose:** This document contains a complete, developer-ready specification of every page, component, route, data fields, and assets for a multilingual (German primary, English, Arabic) tourism website inspired by `sakkarareisen.de`. Deliver this to the developer as the single source of truth for front-end implementation using Bootstrap, HTML, CSS, JS and a local `assets/` folder (no CDN).

---

## Table of contents
1. Global requirements
2. Project & assets structure
3. Internationalization (i18n) strategy
4. Global UI components (Header, Footer, Language switcher, etc.)
5. Common styles, fonts, and responsive rules
6. Page-by-page specification
   - Home
   - Tours listing (Overview) / Category pages (Hurghada, Marsa Alam, etc.)
   - Tour detail (single tour) — Day trips
   - Multi-day packages (Rundreise)
   - Booking flow (Step-by-step) — Booking confirmation
   - About Us
   - Contact / Contact form / WhatsApp integration
   - Reviews & Testimonials
   - FAQ
   - Blog / News / Article detail
   - Gallery / Media
   - Special pages: Offers, Last minute
   - Legal pages: Impressum, Datenschutzerklärung (Privacy Policy), Terms & Conditions
   - Admin dashboard (light spec for front-end pages used by staff)
7. Forms, validation, error handling
8. SEO, meta, and structured data (schema.org)
9. Accessibility & performance
10. Analytics, tracking and third-party integrations (recommended)
11. Sample translation keys and sample content model
12. Handoff checklist for the developer

---

## 1. Global requirements
- Primary language: **German** (DE). Secondary languages: **English (EN)** and **Arabic (AR)**. Default route uses German content.
- Tech stack: static front-end using **Bootstrap 4/5**, plain **HTML**, **CSS**, **vanilla JS** (or minimal framework if preferred), assets served locally from `/assets/`.
- Responsive: fully mobile-first and accessible (WCAG AA baseline).
- No CDNs — all fonts, icons, images, scripts, and CSS are served from `/assets/`.
- Routing: simple clean URLs (SEO-friendly). Example: `/de/tours/hurghada/boat-trip-pyramids`, `/en/tours/hurghada/boat-trip-pyramids`, `/ar/tours/hurghada/boat-trip-pyramids`.
- Date format & currency: localized per language/region (DE: `DD.MM.YYYY`, EUR if used; EN: `DD MMM YYYY` or `MM/DD/YYYY` depending on choice; AR: Arabic numerals & right-to-left layout). Show prices in **EUR** and optionally **EGP** with a toggle.

---

## 2. Project & assets structure (recommended)
```
project-root/
├─ index.html                # landing redirect (detect language or redirect to /de/)
├─ de/                       # german pages
│  ├─ index.html
│  ├─ tours/
│  └─ ...
├─ en/                       # english pages
├─ ar/                       # arabic pages (rtl)
├─ assets/
│  ├─ css/
│  │  ├─ bootstrap.min.css
│  │  ├─ bootstrap.rtl.min.css
│  │  ├─ main.css
│  ├─ js/
│  │  ├─ bootstrap.min.js
│  │  ├─ main.js
│  ├─ fonts/
│  │  ├─ Titles: Montserrat-Bold.ttf
|  |  ├─ Texts: Lato-Regular.ttf
│  │  ├─ JF-Flat-Regular.ttf/ (for Arabic)
│  ├─ images/
│  │  ├─ hero/
│  │  ├─ tours/
│  │  ├─ logos/
│  ├─ icons/
│  └─ data/
│     ├─ tours.json   # static content example used by front-end
│     └─ translations.json
├─ sitemap.xml
├─ robots.txt
└─ manifest.json (optional)
```

Notes:
- `tours.json` should include Tour ID, slug, language entries (title, short_desc, long_desc, itinerary array), duration, price, images, included/excluded items, pickup areas, start times, availability, featured flag, rating, review count.
- Keep images optimized, WebP copies plus fallback JPEG stored in `/assets/images/tours/`.

---

## 3. Internationalization (i18n) strategy
- Folder-per-language approach: `/de/`, `/en/`, `/ar/` as top-level. Each folder contains mirrored pages. Links must include language prefix.
- Language switcher in header that preserves page context: example: when on `/de/tours/x`, switching to English should go to `/en/tours/x`.
- Right-to-left: Arabic pages must include `dir="rtl"` on `<html>` and load Arabic font(s). UI mirrored where appropriate.
- Use translation keys for static UI phrases and JSON files for dynamic content. Example translations file format:
```json
{
  "en": { "book_now": "Book now", "duration": "Duration" },
  "de": { "book_now": "Jetzt buchen", "duration": "Dauer" },
  "ar": { "book_now": "احجز الآن", "duration": "المدة" }
}
```
- Dates, times, numbers, and currency must be localized.

---

## 4. Global UI components
**Header**
- Logo (left for DE/EN, right for AR when RTL)
- Primary navigation (Tours, Multi-day, Offers, About, Blog, Contact)
- Language selector (DE / EN / AR) — shows country flag + language code
- Contact quick action: phone number and WhatsApp CTA (opens link `https://wa.me/{number}?text={encoded}`)
- Search input (search tours by keyword, location, date) with autocomplete results.

**Footer**
- Columns: Company (Impressum, About, Jobs), Tours (links to categories), Support (FAQ, Contact), Legal (Datenschutz, Terms)
- Social icons (local assets in `/assets/icons/`) linking to FB / TripAdvisor etc.
- Newsletter signup field (email), and copyright notice.

**Sticky elements**
- Sticky CTA button bottom-right on mobile: `Book / WhatsApp`.
- Floating language toggle optional.

**Breadcrumbs**
- Shown on inner pages to improve navigation and SEO.

**Modals**
- Quick booking modal: short form (name, phone, tour, date, pax) that sends request via API or mail.
- Image/gallery modal.

---

## 5. Common styles, fonts, and responsive rules
- Load Bootstrap CSS from `/assets/css/bootstrap.min.css`.
- `main.css` contains custom variables and overrides – color palette (use your brand colors). Example: `--brand-yellow: #F4EA0C;`
- Fonts: include a robust latin font (Inter/Roboto) and an Arabic font (Cairo or Noto Kufi Arabic). Store in `/assets/fonts/`.
- Default base font-size `16px`; use rem units.
- RTL support: include `main-rtl.css` or flip CSS via `html[dir='rtl']` rules.

---

## 6. Page-by-page specification (detailed)
> Each page includes: route, purpose, content blocks (in order), components to reuse, data fields required, SEO meta, and sample CTAs.

### 6.1 Home
- **Routes**: `/de/`, `/en/`, `/ar/`
- **Purpose**: Main landing page that highlights top tours, categories, unique selling points, and trust signals.
- **Hero**: Large image slider (3 slides). Each slide needs: title, 1-line subtitle, primary CTA `Book now` linking to tours listing or a featured tour.
- **Top features**: Icons + short phrases (e.g., "Local Guides", "Safe & Certified", "Free pickup from hotels").
- **Search bar**: Destination / tour keyword, date, pax — leads to `/de/tours/?q=...`.
- **Featured tours**: card list (image, title, short_desc, duration, price, rating, CTA `View tour`).
- **Categories**: small cards linking to Hurghada, Marsa Alam, Cairo day trips, Multi-day tours.
- **Why choose us**: short bullets, trust badges, TripAdvisor / Facebook links.
- **Testimonials carousel**: short quotes with reviewer name and rating.
- **Newsletter sign-up** and contact summary.
- **Footer**
- **SEO**: meta title, desc, canonical, Open Graph tags, JSON-LD for Organization + breadcrumb list.

**Data fields**: featured_tours[], heroSlides[], testimonials[].


### 6.2 Tours Listing / Category page
- **Routes**: `/de/tours/`, `/de/tours/hurghada/`, `/de/tours/marsa-alam/` etc.
- **Purpose**: Show list of tours filtered by category, with filters and sorting.
- **Top**: category title, short description, breadcrumb.
- **Filters**: duration (half-day, full-day, multi-day), price range slider, date picker, activity type (safari, diving, cultural), rating, availability.
- **Sort options**: Popular, Price Low→High, Price High→Low, Newest.
- **List view**: cards (image, title, duration, small icons, price, quick view button, link to detail).
- **Map view (optional)**: small embedded map with pins for tour start locations — static or interactive if desired.
- **Pagination / load more**.

**Data fields**: category name, tours[].


### 6.3 Tour Detail (Single Tour)
- **Route**: `/de/tours/:category/:slug` (example `/de/tours/hurghada/pyramids-day-trip`)
- **Purpose**: Comprehensive page for a single tour.
- **Header**: breadcrumbs, H1 (Tour title), small meta (duration, start times, meeting point, price range).
- **Gallery**: primary hero image + thumbnail strip (open in modal). Use lazy-loading.
- **Short summary**: one-line highlight + price + rating + CTA buttons (`Book now`, `Contact via WhatsApp`, `Add to wishlist`).
- **Key Info (sticky sidebar on desktop)**:
  - Price (per adult/child), Group/Private option
  - Duration
  - Pickup details (hotels / meeting point)
  - Includes / Excludes (bullet list)
  - Languages of guide
  - Cancellation policy
  - Available dates (calendar or next departures)
- **Full description**: paragraph content and selling points.
- **Itinerary**: day-by-day (for multi-day) or time-by-time for day trips (time table: 08:00 pickup → 10:00 arrival → ...).
- **What to bring**: short list (sunblock, passport copy, comfortable shoes).
- **Reviews section**: client reviews, rating breakdown.
- **Related tours**: 3–4 suggested tours.
- **FAQ specific to tour**.
- **Structured Data**: `TouristTrip` or `Trip` schema + `Offer` entries.

**Forms/CTAs**: book widget (in page & modal), contact support.

**Data fields**: id, title, slug, category, short_desc, long_desc, itinerary[], images[], price:{adult, child, currency}, included[], excluded[], duration, start_times[], language[], pickupZones[], reviews[].


### 6.4 Multi-day Packages (Rundreise)
- **Route**: `/de/multi-day/` or `/de/tours/rundreise/` and per-package `/de/multi-day/7-day-siwa-marsa-matrouh/`
- **Content**:
  - Program overview with daily break-down
  - Accommodation level (3*, 4*, 5*), transport type, meals included
  - Map with route
  - Price table (per person for double occupancy, single supplement)
  - Booking steps & terms


### 6.5 Booking flow (step-by-step)
- **Routes**: `/de/book/:tourId/step-1` etc. Or single-step modal that opens an external booking system.
- **Approach**: Two options for implementation:
  1. Front-end form posts to back-end API (preferred): create temporary booking request -> staff confirm -> customer receives confirmation & invoice link.
  2. Simple form that sends email + WhatsApp request.

**Booking Steps (recommended):**
- Step 1: Select date, number of adults/children, extras (lunch, hotel pickup), optional room type for multi-day.
- Step 2: Traveler details (first name, last name, email, phone, nationality, passport number if required) + payment method selection.
- Step 3: Review & Confirm (show breakdown) + accept T&Cs and privacy policy.
- After booking: Confirmation page and downloadable invoice / booking summary + booking ID. Send automated email.

**Security/validation**: required fields, server-side validation, CSRF token when posting.


### 6.6 Contact page
- **Route**: `/de/contact/` and localized equivalents.
- **Content**:
  - Company contact info: German phone number (e.g. +49...), company email, office hours.
  - Contact form: name, email, phone, subject, message, preferred language, tour (optional dropdown), consent checkbox (privacy policy).
  - WhatsApp quick link and phone CTA.
  - Google Map embed for local office (optional) — if privacy/policy prevents embedding, provide address and directions.

**Validation**: reCAPTCHA or simple honeypot to reduce spam.


### 6.7 Reviews & Testimonials page
- **Route**: `/de/reviews/`
- **Content**: aggregated reviews, TripAdvisor widget (if available), ability to filter by tour.


### 6.8 FAQ
- **Route**: `/de/faq/`
- **Content**: categorized Q&A (Booking, Payment, Pickup, Cancellation, Safety, Insurance).


### 6.9 Blog / Articles
- **Routes**: `/de/blog/`, `/de/blog/:slug`
- **Content**: list of articles with tag filtering, each article with author, published date, reading time, related tours.


### 6.10 Gallery / Media
- **Route**: `/de/gallery/`
- **Content**: filterable gallery (destination, activity). Lightbox modal for viewing with captions & credits.


### 6.11 Special pages: Offers / Last-minute
- **Route**: `/de/offers/` and `/de/offers/:slug`
- **Content**: discounted tours, limited time banners, countdown timers.


### 6.12 Legal pages (required for Germany)
- **Impressum**: `/de/impressum/` — Company name, legal form, address, contact, VAT ID, representative, registration number, responsible for content. **This is legally required.**
- **Datenschutzerklärung (Privacy Policy)**: `/de/datenschutzerklaerung/` with GDPR-compliant text: what data collected, cookies, analytics, contact form data handling, data retention, user rights.
- **Terms & Conditions**: cancellation rules, liability, booking process.

Each legal page must be translated and available in the three languages.


### 6.13 Admin front-end (light)
- **Routes**: `/de/admin/` (or separate management subdomain) — staff can view booking requests, mark them confirmed, export CSV. This can be minimal and implemented later.

---

## 7. Forms, validation, error handling
- Use inline validation for forms with clear error messages.
- Required fields must be indicated and validated client-side and server-side.
- Error page template for 404 and 500 including search box and language-specific message.
- For bookings: show friendly messages on success and a unique booking reference.

---

## 8. SEO, meta, and structured data
- Each page must include `<title>`, `<meta name="description">`, canonical tag, Open Graph tags and Twitter Card tags.
- Implement `sitemap.xml` and `robots.txt`.
- Use `schema.org`:
  - Organization (global site)
  - LocalBusiness / TravelAgency with address, phone, priceRange
  - For tour pages use `TouristTrip`, `Offer`, and `Review` where applicable.
- Use language and hreflang tags in the `<head>`:
```html
<link rel="alternate" hreflang="de" href="https://example.com/de/tours/..." />
<link rel="alternate" hreflang="en" href="https://example.com/en/tours/..." />
<link rel="alternate" hreflang="ar" href="https://example.com/ar/tours/..." />
```

---

## 9. Accessibility & performance
- Images must have `alt` text.
- Keyboard navigable modals and forms.
- Color contrast must meet AA.
- Lazy-load images, compress images and minify CSS/JS. Use `preload` for hero fonts and critical CSS.

---

## 10. Analytics & integrations
- Analytics (e.g., Google Analytics or Matomo) with GDPR consent banner.
- TripAdvisor / Facebook links & widgets.
- Optional: payment provider integration instructions (if implementing online payments) — provide secure server-side integration; front-end only submits to backend.

---

## 11. Sample translation keys & sample content model
**Translation keys example** (partial):
```json
{
  "header": { "book_now": { "de": "Jetzt buchen", "en": "Book now", "ar": "احجز الآن" },
              "contact": { "de": "Kontakt", "en": "Contact", "ar": "اتصل" }
  },
  "tour": { "duration": { "de": "Dauer", "en": "Duration", "ar": "المدة" } }
}
```

**Tour object example (JSON)**:
```json
{
  "id": "TR-0001",
  "slug": "pyramids-day-trip",
  "category": "hurghada",
  "languages": { "de": { "title": "Pyramiden Tagesausflug", "short_desc": "Besuchen Sie die Pyramiden von Gizeh..." },
                 "en": { "title": "Pyramids Day Trip", "short_desc": "Visit the Giza Pyramids..." },
                 "ar": { "title": "رحلة يومية للأهرامات", "short_desc": "زيارة أهرامات الجيزة..." }
  },
  "duration": "12h",
  "price": { "currency": "EUR", "adult": 89, "child": 59 },
  "images": ["/assets/images/tours/pyramids-1.webp"],
  "itinerary": [ {"time":"08:00","text":"Hotel pickup"}, {"time":"10:00","text":"Arrival at Giza"} ]
}
```

---

## 12. Handoff checklist for the developer
- [ ] All pages created under `/de/`, `/en/`, `/ar/` and language switcher tested.
- [ ] Assets placed in `/assets/` as described and referenced with relative URLs.
- [ ] Sitemap.xml and robots.txt created.
- [ ] Impressum and Datenschutzerklärung present and translated.
- [ ] Booking form works and posts to API endpoint `/api/bookings` (or sends email) with required fields.
- [ ] Structured data present on tour pages.
- [ ] Performance check: Lighthouse score >= 80 mobile, >= 90 desktop (aim).
- [ ] Accessibility audit passed for core pages.


---

## Appendix — Developer notes & recommended priorities
**Phase 1 (MVP)**
1. Home (DE/EN/AR), Tours listing, Tour detail, Contact, Impressum, Datenschutzerklärung.
2. Booking request form (email + WhatsApp fallback).
3. Language switcher + route mirrors.

**Phase 2 (Enhancements)**
1. Calendar availability, payment integration.
2. Reviews import, TripAdvisor widget.
3. Admin interface for bookings.

**Quick tips**
- For Arabic, test layout thoroughly with RTL; also localize numbers to Arabic-Indic numerals if desired.
- Keep tour content in a single source JSON or CMS so translations and updates are centralized.

---

If you want, I can also export `tours.json` sample with 10 example tours + translations, or provide a CSV sitemap for developer import. Tell me if you want the document converted to a downloadable file format (Word, PDF) or want additional pieces (sample booking API contract, sample email templates).

