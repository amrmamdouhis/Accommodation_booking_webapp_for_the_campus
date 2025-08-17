

    function toggleSidebar() {
      document.getElementById('sidebar').classList.toggle('active');
      document.getElementById('content').classList.toggle('active');
    }

    document.addEventListener("DOMContentLoaded", function () {
      const currentPath = window.location.pathname.toLowerCase();
      document.querySelectorAll('#sidebar a').forEach(link => {
        const linkPath = link.getAttribute('href').toLowerCase();
        if (currentPath === linkPath) {
          link.classList.add('active');
        }
      });
    });
