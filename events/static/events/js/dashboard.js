/* ═══════════════════════════════════════════════
   DASHBOARD JS
═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Sidebar Toggle ──────────────────────────
  const sidebar        = document.getElementById('sidebar');
  const sidebarToggle  = document.getElementById('sidebarToggle');
  const sidebarClose   = document.getElementById('sidebarClose');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  function openSidebar() {
    sidebar?.classList.add('open');
    sidebarOverlay?.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar?.classList.remove('open');
    sidebarOverlay?.classList.remove('active');
    document.body.style.overflow = '';
  }

  sidebarToggle?.addEventListener('click', openSidebar);
  sidebarClose?.addEventListener('click', closeSidebar);
  sidebarOverlay?.addEventListener('click', closeSidebar);

  // ─── Notification Dropdown ───────────────────
  const notifBtn      = document.getElementById('notifBtn');
  const notifDropdown = document.getElementById('notifDropdown');

  notifBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    notifDropdown?.classList.toggle('show');
    profileDropdown?.classList.remove('show');
  });

  // ─── Profile Dropdown ────────────────────────
  const profileBtn      = document.getElementById('profileBtn');
  const profileDropdown = document.getElementById('profileDropdown');
  const topbarArrow     = document.querySelector('.topbar-arrow');

  profileBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    profileDropdown?.classList.toggle('show');
    notifDropdown?.classList.remove('show');
    if (topbarArrow) {
      topbarArrow.style.transform =
        profileDropdown?.classList.contains('show')
          ? 'rotate(180deg)' : 'rotate(0)';
    }
  });

  // Close dropdowns on outside click
  document.addEventListener('click', () => {
    notifDropdown?.classList.remove('show');
    profileDropdown?.classList.remove('show');
    if (topbarArrow) topbarArrow.style.transform = 'rotate(0)';
  });

  // ─── Auto Dismiss Alerts ─────────────────────
  document.querySelectorAll('.dash-alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      alert.style.transition = 'all 0.3s ease';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });

  // ─── Count Up Animation ──────────────────────
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.getAttribute('data-count')) || 0;
    let count = 0;
    const step = Math.ceil(target / 30);
    const timer = setInterval(() => {
      count = Math.min(count + step, target);
      el.textContent = count;
      if (count >= target) clearInterval(timer);
    }, 40);
  });

  console.log('%c Dashboard Ready ✓ ',
    'background:#6c63ff;color:white;padding:4px 8px;border-radius:4px');
});


/* ═══════════════════════════════════════════════
   DASHBOARD JS
═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Sidebar Toggle ──────────────────────────
  const sidebar        = document.getElementById('sidebar');
  const sidebarToggle  = document.getElementById('sidebarToggle');
  const sidebarClose   = document.getElementById('sidebarClose');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  function openSidebar() {
    sidebar?.classList.add('open');
    sidebarOverlay?.classList.add('active');
    document.body.style.overflow = 'hidden';
    sidebarToggle?.blur(); // <--- YE LINE ADD KARO
  }

  function closeSidebar() {
    sidebar?.classList.remove('open');
    sidebarOverlay?.classList.remove('active');
    document.body.style.overflow = '';
  }

  sidebarToggle?.addEventListener('click', openSidebar);
  sidebarClose?.addEventListener('click', closeSidebar);
  sidebarOverlay?.addEventListener('click', closeSidebar);

  // ─── Notification Dropdown ───────────────────
  const notifBtn      = document.getElementById('notifBtn');
  const notifDropdown = document.getElementById('notifDropdown');

  notifBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    notifDropdown?.classList.toggle('show');
    profileDropdown?.classList.remove('show');
    notifBtn?.blur(); // <--- YE LINE BHI ADD KARO
  });

  // ─── Profile Dropdown ────────────────────────
  const profileBtn      = document.getElementById('profileBtn');
  const profileDropdown = document.getElementById('profileDropdown');
  const topbarArrow     = document.querySelector('.topbar-arrow');

  profileBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    profileDropdown?.classList.toggle('show');
    notifDropdown?.classList.remove('show');
    if (topbarArrow) {
      topbarArrow.style.transform =
        profileDropdown?.classList.contains('show')
          ? 'rotate(180deg)' : 'rotate(0)';
    }
    profileBtn?.blur(); // <--- YE LINE BHI ADD KARO
  });

  // Close dropdowns on outside click
  document.addEventListener('click', (e) => { // e parameter add kiya
    if (!notifBtn?.contains(e.target) && notifDropdown?.classList.contains('show')) {
        notifDropdown.classList.remove('show');
    }
    if (!profileBtn?.contains(e.target) && profileDropdown?.classList.contains('show')) {
        profileDropdown.classList.remove('show');
        if (topbarArrow) topbarArrow.style.transform = 'rotate(0)';
    }
  });

  // ─── Auto Dismiss Alerts ─────────────────────
  document.querySelectorAll('.dash-alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      alert.style.transition = 'all 0.3s ease';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });

  // ─── Count Up Animation ──────────────────────
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.getAttribute('data-count')) || 0;
    let count = 0;
    const step = Math.max(1, Math.ceil(target / 30)); // Ensure step is at least 1
    const timer = setInterval(() => {
      count = Math.min(count + step, target);
      el.textContent = count;
      if (count >= target) clearInterval(timer);
    }, 40);
  });

  console.log('%c Dashboard Ready ✓ ',
    'background:#6c63ff;color:white;padding:4px 8px;border-radius:4px');
});