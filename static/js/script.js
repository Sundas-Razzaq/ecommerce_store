function updateActiveNavLink() {
  const currentPath = window.location.pathname;

  document.querySelectorAll('#navbar li a').forEach(link => {
    link.classList.remove('real-active');
    const linkPath = link.getAttribute('href');

    if (linkPath === currentPath ||
        (currentPath === '/' && linkPath.includes('home'))) {
      link.classList.add('real-active');
    }

    if (link.closest('.dropdown-menu')) {
      const parentLink = link.closest('.dropdown').querySelector('.dropdown-toggle');
      if (parentLink) {
        parentLink.classList.toggle('active-child', link.classList.contains('real-active'));
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  updateActiveNavLink();

  const navbarToggle = document.querySelector('.navbar-toggler');
  const navbar = document.getElementById('navbar');

  // Toggle mobile navbar
  if (navbarToggle && navbar) {
    navbarToggle.addEventListener('click', function () {
      navbar.classList.toggle('active');
    });
  }
  document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();

      const dropdown = this.closest('.dropdown');

      // Close all other dropdowns first
      document.querySelectorAll('.dropdown').forEach(d => {
        if (d !== dropdown) d.classList.remove('open');
      });

      dropdown.classList.toggle('open');
    });
  });

  // Close navbar on mobile when a link is clicked
  document.querySelectorAll('#navbar a').forEach(link => {
    link.addEventListener('click', function () {
      setTimeout(updateActiveNavLink, 50);

      // Close navbar only on mobile
      if (window.innerWidth <= 991) {
        navbar.classList.remove('active');
      }
    });
  });

  // Optional: Smooth scroll for internal anchor links
  document.querySelectorAll('[data-smooth-scroll]').forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Re-run active state when back/forward navigation happens
  window.addEventListener('popstate', updateActiveNavLink);
});

// ====== GLOBAL CLICK LISTENER TO CLOSE DROPDOWNS ====== //
document.addEventListener('click', function (e) {
  if (!e.target.closest('.dropdown')) {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
      dropdown.classList.remove('open');
    });
  }
});
