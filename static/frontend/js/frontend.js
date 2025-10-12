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
document.addEventListener("DOMContentLoaded", () => {
  const galleryItems = document.querySelectorAll(".gallery-item img");
  const lightbox = document.getElementById("lightbox");
  const swiperWrapper = document.querySelector(".lightbox-swiper .swiper-wrapper");
  const closeLightbox = document.querySelector(".close-lightbox");

  let swiperInstance;

  galleryItems.forEach((img, index) => {
    img.addEventListener("click", () => {
      // Clear previous slides
      swiperWrapper.innerHTML = "";

      // Create slides dynamically
      galleryItems.forEach((item) => {
        const slide = document.createElement("div");
        slide.classList.add("swiper-slide");
        slide.innerHTML = `
          <img src="${item.src}" alt="${item.alt}">
          <div class="lightbox-caption">${item.alt || ""}</div>
        `;
        swiperWrapper.appendChild(slide);
      });

      // Show lightbox
      lightbox.classList.add("active");

      // Initialize Swiper
      swiperInstance = new Swiper(".lightbox-swiper", {
        initialSlide: index,
        loop: true,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        keyboard: true,
        spaceBetween: 30,
        effect: "fade",
        fadeEffect: { crossFade: true },
      });
    });
  });

  // Close on click or ESC
  closeLightbox.addEventListener("click", () => {
    lightbox.classList.remove("active");
    swiperInstance?.destroy();
  });

  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) {
      lightbox.classList.remove("active");
      swiperInstance?.destroy();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      lightbox.classList.remove("active");
      swiperInstance?.destroy();
    }
  });
});
