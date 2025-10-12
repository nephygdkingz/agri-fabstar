// swiper-init.js
document.addEventListener('DOMContentLoaded', () => {

  const swiper = new Swiper('.featured-products-swiper', {
    loop: true, // loop enabled for smooth autoplay
    spaceBetween: 20,
    autoplay: {
      delay: 4000, // 3 seconds per slide
      disableOnInteraction: false, // keep autoplay after interactions
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 2,
      },
      768: {
        slidesPerView: 3,
      },
      992: {
        slidesPerView: 4,
      }
    }
  });

  const gallerySwiper = new Swiper(".gallery-swiper", {
    slidesPerView: "auto",
    spaceBetween: 15,
    grabCursor: true,
    loop: true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
    centeredSlides: true,
  });

});


