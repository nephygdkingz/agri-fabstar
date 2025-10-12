document.addEventListener('DOMContentLoaded', () => {

  // navbar and sidenar
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const closeSidebar = document.getElementById('closeSidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (!sidebarToggle || !sidebar || !closeSidebar || !sidebarOverlay) {
    console.error('Sidebar elements not found. Check your HTML IDs.');
    return;
  }

  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.add('open');
    sidebarOverlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  });

  function closeSidebarMenu() {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('show');
    document.body.style.overflow = '';
  }

  closeSidebar.addEventListener('click', closeSidebarMenu);
  sidebarOverlay.addEventListener('click', closeSidebarMenu);

  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // CATEGORY CLICK ANIMATION
  document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.add('clicked');
      setTimeout(() => card.classList.remove('clicked'), 400);
    });
  });

  // ===== SCROLL REVEAL ANIMATION =====
  const revealElements = document.querySelectorAll('.fade-up');

  const revealOnScroll = () => {
    const triggerBottom = window.innerHeight * 1.1;
    revealElements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < triggerBottom) {
        el.classList.add('show');
      }
    });
  };

  window.addEventListener('scroll', revealOnScroll);
  window.addEventListener('load', revealOnScroll);


  // Auto-update footer year
  document.getElementById("year").textContent = new Date().getFullYear();

});

// ===== GALLERY LIGHTBOX =====
document.addEventListener('DOMContentLoaded', () => {
  const galleryItems = document.querySelectorAll('.gallery-item img, .swiper-slide img');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = lightbox.querySelector('img');
  const caption = document.querySelector('.lightbox-caption');
  const closeBtn = document.querySelector('.lightbox-close');
  const prevBtn = document.querySelector('.lightbox-prev');
  const nextBtn = document.querySelector('.lightbox-next');
  const viewFullGalleryBtn = document.getElementById('viewFullGallery');

  let currentIndex = 0;
  const images = Array.from(galleryItems).map(img => ({
    src: img.src,
    alt: img.alt
  }));

  function openLightbox(index) {
    currentIndex = index;
    lightboxImg.src = images[currentIndex].src;
    caption.textContent = images[currentIndex].alt;
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  function showNext() {
    currentIndex = (currentIndex + 1) % images.length;
    openLightbox(currentIndex);
  }

  function showPrev() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    openLightbox(currentIndex);
  }

  // Bind image clicks
  galleryItems.forEach((img, i) => {
    img.addEventListener('click', () => openLightbox(i));
  });

  // Buttons and keys
  closeBtn.addEventListener('click', closeLightbox);
  nextBtn.addEventListener('click', showNext);
  prevBtn.addEventListener('click', showPrev);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') showNext();
    if (e.key === 'ArrowLeft') showPrev();
  });

  // 🌿 View Full Gallery button (mobile)
  // if (viewFullGalleryBtn) {
  //   viewFullGalleryBtn.addEventListener('click', () => openLightbox(0));
  // }

  // Swiper init (for mobile)
  new Swiper('.myGallerySwiper', {
    slidesPerView: 1.2,
    spaceBetween: 15,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    breakpoints: {
      480: { slidesPerView: 2 },
      768: { slidesPerView: 3 },
    }
  });
});

