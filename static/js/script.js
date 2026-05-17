// ─── Hamburger Menu ───────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');
const navOverlay = document.getElementById('nav-overlay');

if (hamburger && navLinks && navOverlay) {
  hamburger.addEventListener('click', (e) => {
    e.stopPropagation();
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('open');
    navOverlay.classList.toggle('active');
  });
  navOverlay.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navLinks.classList.remove('open');
    navOverlay.classList.remove('active');
  });
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      navLinks.classList.remove('open');
      navOverlay.classList.remove('active');
    });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      hamburger.classList.remove('active');
      navLinks.classList.remove('open');
      navOverlay.classList.remove('active');
    }
  });
}


// ─── Carousel (works on ALL screen sizes) ──────────────────────
(function () {
  const track     = document.querySelector('.carousel-track');
  if (!track) return;

  const container = document.querySelector('.carousel-track-container');
  const cards     = Array.from(document.querySelectorAll('.carousel-track .blog-card'));
  const prevBtn   = document.querySelector('.prev-btn');
  const nextBtn   = document.querySelector('.next-btn');
  const dots      = Array.from(document.querySelectorAll('.dot'));

  if (!cards.length) return;

  let currentIndex = 0;
  let autoPlayInterval = null;

  function getVisibleCount() {
    const w = window.innerWidth;
    if (w <= 640)  return 1;
    if (w <= 1024) return 2;
    return 3;
  }

  function maxIndex() {
    return Math.max(0, cards.length - getVisibleCount());
  }

  function getCardWidth() {
    // Use the container width divided by visible count, minus gap
    const gap = 24;
    const visible = getVisibleCount();
    return (container.offsetWidth - gap * (visible - 1)) / visible;
  }

  function setCardWidths() {
    const w = getCardWidth();
    cards.forEach(card => {
      card.style.flex = '0 0 ' + w + 'px';
      card.style.width = w + 'px';
    });
  }

  function updateCarousel(animate) {
    setCardWidths();
    const cardWidth = getCardWidth();
    const gap = 24;
    const offset = currentIndex * (cardWidth + gap);
    if (animate === false) {
      track.style.transition = 'none';
    } else {
      track.style.transition = 'transform 0.5s ease';
    }
    track.style.transform = 'translateX(-' + offset + 'px)';
    dots.forEach((dot, i) => dot.classList.toggle('active', i === currentIndex));
  }

  function clampIndex() {
    currentIndex = Math.max(0, Math.min(currentIndex, maxIndex()));
  }

  function goNext() {
    currentIndex = currentIndex >= maxIndex() ? 0 : currentIndex + 1;
    updateCarousel();
  }

  function goPrev() {
    currentIndex = currentIndex <= 0 ? maxIndex() : currentIndex - 1;
    updateCarousel();
  }

  function startAutoPlay() {
    stopAutoPlay();
    autoPlayInterval = setInterval(goNext, 3500);
  }

  function stopAutoPlay() {
    clearInterval(autoPlayInterval);
    autoPlayInterval = null;
  }

  if (nextBtn) nextBtn.addEventListener('click', () => { goNext(); stopAutoPlay(); startAutoPlay(); });
  if (prevBtn) prevBtn.addEventListener('click', () => { goPrev(); stopAutoPlay(); startAutoPlay(); });

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      currentIndex = i;
      clampIndex();
      updateCarousel();
      stopAutoPlay();
      startAutoPlay();
    });
  });

  // Touch/swipe
  let touchStartX = 0;
  track.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; stopAutoPlay(); }, { passive: true });
  track.addEventListener('touchend', e => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) { diff > 0 ? goNext() : goPrev(); }
    startAutoPlay();
  });

  // Resize — recalculate without animation
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      clampIndex();
      updateCarousel(false);
      // Re-enable transition after forced snap
      setTimeout(() => { track.style.transition = 'transform 0.5s ease'; }, 50);
    }, 100);
  });

  // Init
  updateCarousel(false);
  setTimeout(() => { track.style.transition = 'transform 0.5s ease'; }, 50);
  startAutoPlay();
})();


// ─── Scroll To Top Button ──────────────────────────────────────
(function () {
  const btn = document.getElementById('scrollTopBtn');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();


// ─── Reading Progress Bar ──────────────────────────────────────
(function () {
  const bar = document.getElementById('progress-bar');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const scrollTop  = window.scrollY;
    const docHeight  = document.body.scrollHeight - window.innerHeight;
    const progress   = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    bar.style.width  = progress + '%';
  }, { passive: true });
})();


// ─── Reactions ────────────────────────────────────────────────
(function () {
  const reactionBtns = document.querySelectorAll('.reaction-btn');
  if (!reactionBtns.length) return;

  const pageKey  = 'reactions_' + window.location.pathname;
  const userKey  = 'userReacted_' + window.location.pathname;
  const saved    = JSON.parse(localStorage.getItem(pageKey) || '{}');
  const reacted  = localStorage.getItem(userKey);

  reactionBtns.forEach(btn => {
    const type  = btn.dataset.reaction;
    const count = saved[type] || 0;
    btn.querySelector('.reaction-count').textContent = count;
    if (reacted === type) btn.classList.add('reacted');
  });

  reactionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.dataset.reaction;
      const prev = localStorage.getItem(userKey);

      if (prev === type) {
        saved[type] = Math.max(0, (saved[type] || 0) - 1);
        btn.querySelector('.reaction-count').textContent = saved[type];
        btn.classList.remove('reacted');
        localStorage.removeItem(userKey);
      } else {
        if (prev) {
          saved[prev] = Math.max(0, (saved[prev] || 0) - 1);
          const prevBtn = document.querySelector('[data-reaction="' + prev + '"]');
          if (prevBtn) {
            prevBtn.querySelector('.reaction-count').textContent = saved[prev];
            prevBtn.classList.remove('reacted');
          }
        }
        saved[type] = (saved[type] || 0) + 1;
        btn.querySelector('.reaction-count').textContent = saved[type];
        btn.classList.add('reacted');
        localStorage.setItem(userKey, type);
      }
      localStorage.setItem(pageKey, JSON.stringify(saved));
    });
  });
})();


// ─── Contact Form Validation ───────────────────────────────────
function submitForm() {
  let isValid = true;
  const fields = [
    { id: 'name',    error: 'name-error',    message: 'Please enter your name' },
    { id: 'email',   error: 'email-error',   message: 'Please enter a valid email' },
    { id: 'subject', error: 'subject-error', message: 'Please enter a subject' },
    { id: 'message', error: 'message-error', message: 'Please enter your message' }
  ];
  fields.forEach(field => {
    const el = document.getElementById(field.id);
    const errEl = document.getElementById(field.error);
    if (el) el.classList.remove('error');
    if (errEl) errEl.textContent = '';
  });
  fields.forEach(field => {
    const el = document.getElementById(field.id);
    const errEl = document.getElementById(field.error);
    if (!el) return;
    const value = el.value.trim();
    if (!value) {
      el.classList.add('error');
      if (errEl) errEl.textContent = field.message;
      isValid = false;
    }
    if (field.id === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      el.classList.add('error');
      if (errEl) errEl.textContent = 'Please enter a valid email address';
      isValid = false;
    }
  });
  if (isValid) {
    const form = document.getElementById('contact-form');
    const success = document.getElementById('form-success');
    if (form) form.style.display = 'none';
    if (success) success.style.display = 'block';
  }
}


// ─── Scroll Reveal Animations ──────────────────────────────────
(function () {
  const els = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if (!els.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  els.forEach(el => observer.observe(el));
})();


// ─── Auto-dismiss flash messages ──────────────────────────────
document.querySelectorAll('.flash-message').forEach(msg => {
  setTimeout(() => {
    msg.style.transition = 'opacity 0.5s';
    msg.style.opacity = '0';
    setTimeout(() => msg.remove(), 500);
  }, 4000);
});


// ─── Copy Post Link ───────────────────────────────────────────
function copyPostLink() {
  navigator.clipboard.writeText(window.location.href).then(() => {
    const label = document.getElementById('copy-label');
    if (label) {
      label.textContent = 'Copied!';
      setTimeout(() => { label.textContent = 'Copy Link'; }, 2000);
    }
  });
}
