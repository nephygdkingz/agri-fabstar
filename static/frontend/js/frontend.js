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

// #spin button
document.addEventListener("DOMContentLoaded", function() {
  // Select all submit buttons with the reusable class
  const submitButtons = document.querySelectorAll(".js-submit-btn");

  submitButtons.forEach(button => {
    button.addEventListener("click", function(event) {
      const form = button.closest("form");
      if (!form) return;

      // Prevent double submission
      if (button.classList.contains("is-loading")) {
        event.preventDefault();
        return;
      }
      console.log('i am here')
      // Prevent default submit temporarily to show spinner
      event.preventDefault();

      // Mark as loading
      button.classList.add("is-loading");
      const spinner = button.querySelector(".spinner-border");
      const btnText = button.querySelector(".btn-text");

      if (spinner) spinner.classList.remove("d-none");
      if (btnText) btnText.classList.add("d-none");

      // Disable the button to prevent multiple clicks
      button.disabled = true;

      // Submit the form after a brief delay (for UX smoothness)
      setTimeout(() => {
        form.submit();
      }, 100);
    });
  });
});

