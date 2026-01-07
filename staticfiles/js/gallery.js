// Gallery Lightbox Functionality

class GalleryLightbox {
  constructor() {
    this.modal = document.getElementById('lightboxModal');
    this.currentIndex = 0;
    this.images = [];
    this.init();
  }

  init() {
    // Collect all gallery items
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach((item, index) => {
      const img = item.querySelector('.gallery-image');
      const title = item.querySelector('.gallery-info h3')?.textContent || '';
      const description = item.querySelector('.gallery-info p')?.textContent || '';
      
      this.images.push({
        src: img.src,
        alt: img.alt,
        title: title,
        description: description
      });

      // Add click event
      item.addEventListener('click', () => {
        this.openLightbox(index);
      });
    });

    // Close button
    const closeBtn = this.modal.querySelector('.lightbox-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.closeLightbox());
    }

    // Overlay click to close
    const overlay = this.modal.querySelector('.lightbox-overlay');
    if (overlay) {
      overlay.addEventListener('click', () => this.closeLightbox());
    }

    // Navigation buttons
    const prevBtn = this.modal.querySelector('.lightbox-prev');
    const nextBtn = this.modal.querySelector('.lightbox-next');
    
    if (prevBtn) prevBtn.addEventListener('click', () => this.prevImage());
    if (nextBtn) nextBtn.addEventListener('click', () => this.nextImage());

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!this.modal.classList.contains('active')) return;
      
      if (e.key === 'Escape') this.closeLightbox();
      if (e.key === 'ArrowLeft') this.prevImage();
      if (e.key === 'ArrowRight') this.nextImage();
    });
  }

  openLightbox(index) {
    this.currentIndex = index;
    this.updateLightbox();
    this.modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  closeLightbox() {
    this.modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  prevImage() {
    this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
    this.updateLightbox();
  }

  nextImage() {
    this.currentIndex = (this.currentIndex + 1) % this.images.length;
    this.updateLightbox();
  }

  updateLightbox() {
    const image = this.images[this.currentIndex];
    const lightboxImage = document.getElementById('lightboxImage');
    const lightboxTitle = document.getElementById('lightboxTitle');
    const lightboxDescription = document.getElementById('lightboxDescription');

    if (lightboxImage) {
      lightboxImage.src = image.src;
      lightboxImage.alt = image.alt;
    }
    if (lightboxTitle) lightboxTitle.textContent = image.title;
    if (lightboxDescription) lightboxDescription.textContent = image.description;
  }
}

// Gallery Filter
class GalleryFilter {
  constructor() {
    this.filterButtons = document.querySelectorAll('.filter-btn[data-filter]');
    this.galleryItems = document.querySelectorAll('.gallery-item');
    this.init();
  }

  init() {
    this.filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        this.filterImages(filter);
        this.updateActiveButton(btn);
      });
    });
  }

  filterImages(filter) {
    this.galleryItems.forEach(item => {
      if (filter === 'all' || item.dataset.category === filter) {
        item.style.display = 'block';
        setTimeout(() => {
          item.style.opacity = '1';
          item.style.transform = 'scale(1)';
        }, 10);
      } else {
        item.style.opacity = '0';
        item.style.transform = 'scale(0.8)';
        setTimeout(() => {
          item.style.display = 'none';
        }, 300);
      }
    });
  }

  updateActiveButton(activeBtn) {
    this.filterButtons.forEach(btn => {
      btn.classList.remove('active');
    });
    activeBtn.classList.add('active');
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.gallery-grid')) {
    new GalleryLightbox();
    new GalleryFilter();
  }
});

