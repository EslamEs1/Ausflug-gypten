# User Authentication System - AusflugÄgypten

## Overview
Complete user authentication and management system for customers to manage their bookings.

## Features Created

### 1. User Models (`apps/users/models.py`)
- **UserProfile**: Extended user profile with:
  - Personal information (phone, country, city, address)
  - Language preference (DE/EN)
  - Newsletter subscription
  - Profile avatar
  - Auto-created when User is created (via signals)

### 2. Authentication Forms (`apps/users/forms.py`)
- **SignUpForm**: User registration with validation
- **LoginForm**: User login with custom styling
- **UserProfileForm**: Profile editing with User fields integration

### 3. Views (`apps/users/views.py`)
- **signup_view**: User registration
- **login_view**: User login with redirect support
- **logout_view**: User logout
- **DashboardView**: User dashboard with booking statistics
- **ProfileView**: User profile viewing and editing
- **BookingHistoryView**: Complete booking history with filtering

### 4. Templates Created
All templates include responsive design with Tailwind CSS:

#### `login.html`
- Login form with username/password
- "Remember me" checkbox
- Password recovery link
- Link to signup page
- Benefits section

#### `signup.html`
- Registration form with:
  - First name, last name
  - Username, email
  - Phone (optional)
  - Password with confirmation
  - Terms & conditions checkbox
- Password requirements display

#### `dashboard.html`
- Statistics cards (total, pending, confirmed, completed bookings)
- Quick action links (profile, booking history, new booking)
- Recent bookings table (last 5)
- Status badges with colors

#### `profile.html`
- Sidebar navigation
- Profile edit form:
  - Personal information (name, email, phone)
  - Address information (country, city, address)
  - Language preference
  - Avatar upload
  - Newsletter subscription
- Profile avatar display

#### `booking_history.html`
- Filter tabs by status (all, pending, confirmed, completed, cancelled)
- Booking cards with:
  - Tour/activity title
  - Booking date and participants
  - Total price
  - Confirmation code
  - Status badge
  - Special requests
  - Action buttons

### 5. URL Configuration (`apps/users/urls.py`)
```
/konto/signup/          - Registration
/konto/login/           - Login
/konto/logout/          - Logout
/konto/dashboard/       - User dashboard
/konto/profile/         - User profile
/konto/bookings/        - Booking history
```

### 6. Admin Integration (`apps/users/admin.py`)
- UserProfile inline with User admin
- Enhanced User admin with profile fields
- UserProfile admin with filters and search

### 7. Booking Model Updates
- Added `user` ForeignKey to Booking model
- Auto-links bookings to authenticated users
- Supports guest bookings (user=null)
- Updated BookingInquiryView to link users

### 8. Header Navigation Updates
- Login button for guests
- User dropdown menu for authenticated users:
  - Dashboard
  - Profile
  - Bookings
  - Logout

## Database Migrations
```bash
python manage.py makemigrations users
python manage.py makemigrations bookings
python manage.py migrate
```

Created migrations:
- `users/0001_initial.py` - UserProfile model
- `bookings/0004_booking_user.py` - Added user field to Booking

## Usage

### For Customers
1. **Register**: Visit `/konto/signup/` to create an account
2. **Login**: Visit `/konto/login/` to access account
3. **Dashboard**: View booking statistics and recent bookings
4. **Profile**: Edit personal information and preferences
5. **Bookings**: View complete booking history with filters

### For Developers
```python
# Check if user is authenticated
if request.user.is_authenticated:
    profile = request.user.profile
    bookings = request.user.bookings.all()

# Get user's booking count
booking_count = request.user.profile.booking_count

# Get user's full name
full_name = request.user.profile.full_name
```

## Security Features
- Password validation (Django default)
- CSRF protection
- Login required decorators
- Secure password hashing
- Session management

## Next Steps (Optional)
1. Email confirmation on registration
2. Password reset functionality
3. Social authentication (Google, Facebook)
4. Email notifications for booking updates
5. Two-factor authentication
6. User preferences for email notifications

## Testing
All views and forms are ready for testing. Use Django's test framework:
```bash
python manage.py test apps.users
```

## Notes
- All bookings created by authenticated users are automatically linked to their account
- Guest bookings (without login) are still supported
- User dashboard shows both user-linked bookings and bookings matching user's email
- All templates follow the existing design system with Tailwind CSS

