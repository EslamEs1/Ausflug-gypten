// AusflugAgypten - Main JavaScript

// ============================================
// HEADER & NAVIGATION
// ============================================

// Sticky Header
const header = document.getElementById('mainHeader');
let lastScroll = 0;

window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;
  
  if (currentScroll > 100) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
  
  lastScroll = currentScroll;
});

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
const closeMobileMenu = document.getElementById('closeMobileMenu');

function openMobileMenu() {
  mobileMenu.classList.add('active');
  mobileMenuOverlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeMobileMenuFunc() {
  mobileMenu.classList.remove('active');
  mobileMenuOverlay.classList.remove('active');
  document.body.style.overflow = '';
}

if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', openMobileMenu);
}

if (closeMobileMenu) {
  closeMobileMenu.addEventListener('click', closeMobileMenuFunc);
}

if (mobileMenuOverlay) {
  mobileMenuOverlay.addEventListener('click', closeMobileMenuFunc);
}

// Mobile Dropdown
document.querySelectorAll('.mobile-dropdown-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const menuItem = btn.closest('.mobile-menu-item');
    const content = menuItem.querySelector('.mobile-dropdown-content');
    const icon = btn.querySelector('svg');
    const isHidden = content.classList.contains('hidden');
    
    // Close all other dropdowns
    document.querySelectorAll('.mobile-dropdown-content').forEach(dropdown => {
      if (dropdown !== content) {
        dropdown.classList.add('hidden');
      }
    });
    
    document.querySelectorAll('.mobile-dropdown-btn svg').forEach(svg => {
      if (svg !== icon) {
        svg.style.transform = 'rotate(0deg)';
      }
    });
    
    // Toggle current dropdown
    if (isHidden) {
      content.classList.remove('hidden');
      icon.style.transform = 'rotate(180deg)';
    } else {
      content.classList.add('hidden');
      icon.style.transform = 'rotate(0deg)';
    }
  });
});

// ============================================
// LANGUAGE SWITCHER
// ============================================

const langButtons = document.querySelectorAll('.lang-btn');

langButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    langButtons.forEach(b => b.classList.remove('active', 'text-primary-gold'));
    langButtons.forEach(b => b.classList.add('text-gray-600'));
    
    btn.classList.add('active', 'text-primary-gold');
    btn.classList.remove('text-gray-600');
    
    const lang = btn.dataset.lang;
    switchLanguage(lang);
  });
});

function switchLanguage(lang) {
  // Store language preference
  localStorage.setItem('preferred-language', lang);
  
  // Update content based on language
  // This will be implemented when content is bilingual
  console.log(`Language switched to: ${lang}`);
}

// Load saved language preference
document.addEventListener('DOMContentLoaded', () => {
  const savedLang = localStorage.getItem('preferred-language') || 'de';
  const langBtn = document.querySelector(`.lang-btn[data-lang="${savedLang}"]`);
  if (langBtn) {
    langBtn.click();
  }
});

// ============================================
// HERO SLIDER
// ============================================

class HeroSlider {
  constructor(container) {
    this.container = container;
    this.slides = container.querySelectorAll('.hero-slide');
    this.currentSlide = 0;
    this.autoPlayInterval = null;
    
    if (this.slides.length > 0) {
      this.init();
    }
  }
  
  init() {
    this.slides[0].classList.add('active');
    this.autoPlay();
  }
  
  goToSlide(index) {
    this.slides[this.currentSlide].classList.remove('active');
    this.currentSlide = index;
    this.slides[this.currentSlide].classList.add('active');
  }
  
  nextSlide() {
    const next = (this.currentSlide + 1) % this.slides.length;
    this.goToSlide(next);
  }
  
  prevSlide() {
    const prev = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
    this.goToSlide(prev);
  }
  
  autoPlay() {
    this.autoPlayInterval = setInterval(() => {
      this.nextSlide();
    }, 5000);
  }
  
  stopAutoPlay() {
    clearInterval(this.autoPlayInterval);
  }
}

// Initialize hero slider if exists
const heroSlider = document.querySelector('.hero-slider');
if (heroSlider) {
  new HeroSlider(heroSlider);
}

// ============================================
// WISHLIST FUNCTIONALITY
// ============================================

class Wishlist {
  constructor() {
    this.items = this.load();
    this.init();
  }
  
  init() {
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
      const itemId = btn.dataset.id;
      if (this.items.includes(itemId)) {
        btn.classList.add('active');
      }
      
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.toggle(itemId, btn);
      });
    });
  }
  
  toggle(itemId, btn) {
    if (this.items.includes(itemId)) {
      this.remove(itemId);
      btn.classList.remove('active');
    } else {
      this.add(itemId);
      btn.classList.add('active');
    }
  }
  
  add(itemId) {
    this.items.push(itemId);
    this.save();
  }
  
  remove(itemId) {
    this.items = this.items.filter(id => id !== itemId);
    this.save();
  }
  
  save() {
    localStorage.setItem('wishlist', JSON.stringify(this.items));
  }
  
  load() {
    const saved = localStorage.getItem('wishlist');
    return saved ? JSON.parse(saved) : [];
  }
}

// Initialize wishlist
const wishlist = new Wishlist();

// ============================================
// GOOGLE REVIEWS - MODERN ANIMATIONS
// ============================================

class GoogleReviews {
  constructor() {
    this.cards = document.querySelectorAll('.google-review-card');
    this.init();
  }
  
  init() {
    // Stagger animation for cards
    this.cards.forEach((card, index) => {
      card.style.animationDelay = `${index * 0.1}s`;
      card.classList.add('animate-fade-scale');
    });
    
    // Add hover effects
    this.cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px) scale(1.02)';
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
      });
    });
  }
}

// Initialize Google Reviews
if (document.querySelector('.google-reviews-grid')) {
  new GoogleReviews();
}

// ============================================
// ACCORDION
// ============================================

document.querySelectorAll('.accordion-header').forEach(header => {
  header.addEventListener('click', () => {
    const item = header.parentElement;
    const isActive = item.classList.contains('active');
    
    // Close all accordions
    document.querySelectorAll('.accordion-item').forEach(acc => {
      acc.classList.remove('active');
    });
    
    // Open clicked accordion if it wasn't active
    if (!isActive) {
      item.classList.add('active');
    }
  });
});

// ============================================
// ANIMATE ON SCROLL
// ============================================

const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});

// ============================================
// LAZY LOADING IMAGES
// ============================================

const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.add('loaded');
      imageObserver.unobserve(img);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => {
  imageObserver.observe(img);
});

// ============================================
// FILTER FUNCTIONALITY
// ============================================

class FilterSystem {
  constructor() {
    this.filters = {
      category: [],
      price: { min: 0, max: 1000 },
      duration: [],
      rating: 0
    };
    
    this.init();
  }
  
  init() {
    // Category filters
    document.querySelectorAll('.filter-category').forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        this.updateFilters();
        this.applyFilters();
      });
    });
    
    // Price range
    const priceMin = document.getElementById('priceMin');
    const priceMax = document.getElementById('priceMax');
    
    if (priceMin) priceMin.addEventListener('input', () => this.applyFilters());
    if (priceMax) priceMax.addEventListener('input', () => this.applyFilters());
    
    // Rating filter
    document.querySelectorAll('.filter-rating').forEach(radio => {
      radio.addEventListener('change', () => this.applyFilters());
    });
  }
  
  updateFilters() {
    // Get selected categories
    this.filters.category = Array.from(document.querySelectorAll('.filter-category:checked'))
      .map(cb => cb.value);
  }
  
  applyFilters() {
    // This will be implemented to filter tour cards
    const cards = document.querySelectorAll('.tour-card');
    
    cards.forEach(card => {
      const price = parseFloat(card.dataset.price || 0);
      const rating = parseFloat(card.dataset.rating || 0);
      const category = card.dataset.category;
      
      let visible = true;
      
      // Apply filters
      if (this.filters.category.length > 0 && !this.filters.category.includes(category)) {
        visible = false;
      }
      
      card.style.display = visible ? 'block' : 'none';
    });
  }
}

// Initialize filter system if on listing page
if (document.querySelector('.filter-section')) {
  new FilterSystem();
}

// Price Range Slider Updates
const priceMin = document.getElementById('priceMin');
const priceMax = document.getElementById('priceMax');
const minPriceDisplay = document.getElementById('minPriceDisplay');
const maxPriceDisplay = document.getElementById('maxPriceDisplay');

if (priceMin && minPriceDisplay) {
  priceMin.addEventListener('input', (e) => {
    minPriceDisplay.textContent = e.target.value;
    if (parseInt(priceMax.value) < parseInt(e.target.value)) {
      priceMax.value = e.target.value;
      maxPriceDisplay.textContent = e.target.value;
    }
  });
}

if (priceMax && maxPriceDisplay) {
  priceMax.addEventListener('input', (e) => {
    maxPriceDisplay.textContent = e.target.value;
    if (parseInt(priceMin.value) > parseInt(e.target.value)) {
      priceMin.value = e.target.value;
      minPriceDisplay.textContent = e.target.value;
    }
  });
}

// ============================================
// SMOOTH SCROLL
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    
    e.preventDefault();
    const target = document.querySelector(href);
    
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// ============================================
// BOOKING FORM VALIDATION
// ============================================

const bookingForm = document.getElementById('bookingForm');

if (bookingForm) {
  bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Basic validation
    const name = bookingForm.querySelector('[name="name"]').value;
    const email = bookingForm.querySelector('[name="email"]').value;
    const phone = bookingForm.querySelector('[name="phone"]').value;
    const date = bookingForm.querySelector('[name="date"]').value;
    
    if (!name || !email || !phone || !date) {
      alert('Bitte füllen Sie alle Pflichtfelder aus.');
      return;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert('Bitte geben Sie eine gültige E-Mail-Adresse ein.');
      return;
    }
    
    // If validation passes, submit form
    console.log('Form submitted', { name, email, phone, date });
    alert('Vielen Dank! Wir werden uns bald bei Ihnen melden.');
    bookingForm.reset();
  });
}

// ============================================
// MODAL SYSTEM
// ============================================

class Modal {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    if (!this.modal) return;
    
    this.closeBtn = this.modal.querySelector('.modal-close');
    this.init();
  }
  
  init() {
    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.close());
    }
    
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) {
        this.close();
      }
    });
  }
  
  open() {
    this.modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  
  close() {
    this.modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// Initialize modals
document.querySelectorAll('[data-modal]').forEach(trigger => {
  trigger.addEventListener('click', () => {
    const modalId = trigger.dataset.modal;
    const modal = new Modal(modalId);
    modal.open();
  });
});

// ============================================
// NEWSLETTER FORM
// ============================================

const newsletterForms = document.querySelectorAll('form[action*="newsletter"]');

newsletterForms.forEach(form => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = form.querySelector('input[type="email"]').value;
    
    if (email) {
      console.log('Newsletter subscription:', email);
      alert('Vielen Dank für Ihre Anmeldung!');
      form.reset();
    }
  });
});

// ============================================
// UTILITIES
// ============================================

// Format currency
function formatCurrency(amount, currency = 'EUR') {
  return new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: currency
  }).format(amount);
}

// Format date
function formatDate(date) {
  return new Intl.DateTimeFormat('de-DE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(new Date(date));
}

// Debounce function
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ============================================
// MODERN ANIMATIONS & EFFECTS
// ============================================

// Parallax Effect for Hero
function initParallax() {
  const hero = document.querySelector('.hero-slider');
  if (!hero) return;
  
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const rate = scrolled * 0.5;
    hero.style.transform = `translateY(${rate}px)`;
  });
}

// Floating Animation
function initFloatingElements() {
  document.querySelectorAll('.float-animation').forEach((el, index) => {
    el.style.animationDelay = `${index * 0.5}s`;
  });
}

// Counter Animation
function animateCounters() {
  const counters = document.querySelectorAll('.stat-number');
  
  counters.forEach(counter => {
    const target = parseInt(counter.textContent.replace(/[^0-9]/g, ''));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
      current += step;
      if (current < target) {
        counter.textContent = Math.floor(current) + (counter.textContent.includes('+') ? '+' : '') + (counter.textContent.includes('★') ? '★' : '');
        requestAnimationFrame(updateCounter);
      } else {
        counter.textContent = counter.textContent.replace(/[0-9]+/, target);
      }
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          updateCounter();
          observer.unobserve(entry.target);
        }
      });
    });
    
    observer.observe(counter);
  });
}

// Smooth Scroll with Offset
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#' || !href) return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      
      if (target) {
        const headerOffset = 100;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

// Cursor Trail Effect (Optional - Modern Touch)
function initCursorTrail() {
  if (window.innerWidth < 768) return; // Only on desktop
  
  const trail = [];
  const trailLength = 5;
  
  for (let i = 0; i < trailLength; i++) {
    const dot = document.createElement('div');
    dot.className = 'cursor-trail';
    dot.style.cssText = `
      position: fixed;
      width: 8px;
      height: 8px;
      background: radial-gradient(circle, #c8a66e, transparent);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      opacity: ${1 - (i / trailLength)};
      transform: scale(${1 - (i / trailLength) * 0.5});
      transition: transform 0.1s ease-out;
    `;
    document.body.appendChild(dot);
    trail.push(dot);
  }
  
  let mouseX = 0, mouseY = 0;
  
  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });
  
  function animateTrail() {
    let x = mouseX;
    let y = mouseY;
    
    trail.forEach((dot, index) => {
      const nextDot = trail[index - 1] || { offsetLeft: x, offsetTop: y };
      const dx = nextDot.offsetLeft - x;
      const dy = nextDot.offsetTop - y;
      
      x += dx * 0.3;
      y += dy * 0.3;
      
      dot.style.left = x + 'px';
      dot.style.top = y + 'px';
    });
    
    requestAnimationFrame(animateTrail);
  }
  
  animateTrail();
}

// Initialize all modern effects
document.addEventListener('DOMContentLoaded', () => {
  initParallax();
  initFloatingElements();
  animateCounters();
  initSmoothScroll();
  // initCursorTrail(); // Uncomment for cursor trail effect
});

// ============================================
// SCROLL PROGRESS INDICATOR
// ============================================

function initScrollProgress() {
  const progressBar = document.createElement('div');
  progressBar.className = 'scroll-progress';
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, #c8a66e, #245d81);
    z-index: 10000;
    transition: width 0.1s ease-out;
  `;
  document.body.appendChild(progressBar);
  
  window.addEventListener('scroll', () => {
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.pageYOffset / windowHeight) * 100;
    progressBar.style.width = scrolled + '%';
  });
}

initScrollProgress();

console.log('AusflugAgypten initialized ✓');
console.log('Modern animations & effects loaded ✨');

