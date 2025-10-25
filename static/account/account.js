document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById('toggleSidebarBtn');
    const closeBtn = document.getElementById('closeSidebarBtn');
    const sidebar = document.getElementById('sidebar');

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.add('show');
    });

    closeBtn.addEventListener('click', () => {
        sidebar.classList.remove('show');
    });
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