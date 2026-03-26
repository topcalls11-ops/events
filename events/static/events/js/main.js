/* ═══════════════════════════════════════════════
   EVENTSPHERE - Main JS
═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Hamburger Menu ──────────────────────────
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.querySelector('.nav-links');

  if (hamburger) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      hamburger.classList.toggle('open');
    });
  }

  // Close nav on outside click
  document.addEventListener('click', (e) => {
    if (!hamburger?.contains(e.target) && !navLinks?.contains(e.target)) {
      navLinks?.classList.remove('active');
      hamburger?.classList.remove('open');
    }
  });

  // ─── Auto Dismiss Messages ───────────────────
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // ─── Navbar Scroll Effect ────────────────────
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(10,10,26,0.95)';
      navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.3)';
    } else {
      navbar.style.background = 'rgba(10,10,26,0.8)';
      navbar.style.boxShadow = 'none';
    }
  });

  // ─── Card Animation on Scroll ────────────────
  const cards = document.querySelectorAll('.event-card, .step-card, .category-pill');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.animationDelay = `${i * 0.05}s`;
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    observer.observe(card);
  });

  // CSS for animate-in
  const style = document.createElement('style');
  style.textContent = `
    .animate-in {
      animation: fadeUp 0.5s ease forwards;
    }
    @keyframes fadeUp {
      to { opacity: 1; transform: translateY(0); }
    }
  `;
  document.head.appendChild(style);

  // ─── Spots Bar Animation ─────────────────────
  const spotsFills = document.querySelectorAll('.spots-fill, .spots-bar-fill');
  spotsFills.forEach(bar => {
    const targetWidth = bar.style.width;
    bar.style.width = '0';
    setTimeout(() => {
      bar.style.transition = 'width 1s ease';
      bar.style.width = targetWidth;
    }, 300);
  });

  // ─── Active Nav Link ─────────────────────────
  const currentPath = window.location.pathname;
  const navLinkEls  = document.querySelectorAll('.nav-link');
  navLinkEls.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.style.color = '#fff';
      link.classList.add('active-link');
    }
  });

  // ─── Search Input Focus Effect ───────────────
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.addEventListener('focus', () => {
      searchInput.parentElement.style.transform = 'scale(1.01)';
    });
    searchInput.addEventListener('blur', () => {
      searchInput.parentElement.style.transform = 'scale(1)';
    });
  }

  // ─── Smooth Scroll ───────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  console.log('%c EventSphere Loaded ✓ ', 
    'background:#6c63ff;color:white;padding:4px 8px;border-radius:4px;font-weight:bold');
});

// Back to Top Button
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  if (window.scrollY > 400) {
    backToTop?.classList.add('show');
  } else {
    backToTop?.classList.remove('show');
  }
});

backToTop?.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  backToTop.blur();
});