// Hamburger Menu
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');
const navOverlay = document.getElementById('nav-overlay');

if (hamburger && navLinks && navOverlay) {
  // Toggle menu on hamburger click
  hamburger.addEventListener('click', (e) => {
    e.stopPropagation();
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('open');
    navOverlay.classList.toggle('active');
  });

  // Close menu on overlay click
  navOverlay.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navLinks.classList.remove('open');
    navOverlay.classList.remove('active');
  });

  // Close menu on link click
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      navLinks.classList.remove('open');
      navOverlay.classList.remove('active');
    });
  });

  // Close menu on ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      hamburger.classList.remove('active');
      navLinks.classList.remove('open');
      navOverlay.classList.remove('active');
    }
  });
}

// Carousel - only runs if carousel exists on the page
const track = document.querySelector('.carousel-track');

if (track) {
  const cards = document.querySelectorAll('.blog-card');
  const prevBtn = document.querySelector('.prev-btn');
  const nextBtn = document.querySelector('.next-btn');
  const dots = document.querySelectorAll('.dot');

  let currentIndex = 0;
  let autoPlayInterval;

  const visibleCards = () => window.innerWidth <= 768 ? 1 : 3;

  function updateCarousel() {
    const cardWidth = track.parentElement.offsetWidth / visibleCards();
    const gap = 24;
    track.style.transform = `translateX(-${currentIndex * (cardWidth + gap)}px)`;
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === currentIndex);
    });
  }

  function goToNext() {
    const maxIndex = cards.length - visibleCards();
    currentIndex = currentIndex >= maxIndex ? 0 : currentIndex + 1;
    updateCarousel();
  }

  function goToPrev() {
    const maxIndex = cards.length - visibleCards();
    currentIndex = currentIndex <= 0 ? maxIndex : currentIndex - 1;
    updateCarousel();
  }

  function startAutoPlay() {
    autoPlayInterval = setInterval(goToNext, 3000);
  }

  function stopAutoPlay() {
    clearInterval(autoPlayInterval);
  }

  nextBtn.addEventListener('click', () => {
    goToNext();
    stopAutoPlay();
    startAutoPlay();
  });

  prevBtn.addEventListener('click', () => {
    goToPrev();
    stopAutoPlay();
    startAutoPlay();
  });

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      currentIndex = i;
      updateCarousel();
      stopAutoPlay();
      startAutoPlay();
    });
  });

  let touchStartX = 0;
  track.addEventListener('touchstart', e => {
    touchStartX = e.touches[0].clientX;
    stopAutoPlay();
  });

  track.addEventListener('touchend', e => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
      diff > 0 ? goToNext() : goToPrev();
    }
    startAutoPlay();
  });

  window.addEventListener('resize', updateCarousel);

  startAutoPlay();
}

// Reactions
const reactionBtns = document.querySelectorAll('.reaction-btn');

if (reactionBtns.length > 0) {
  // Create unique key per page
  const pageKey = 'reactions_' + window.location.pathname;
  const userKey = 'userReacted_' + window.location.pathname;

  const savedReactions = JSON.parse(localStorage.getItem(pageKey) || '{}');
  const userReacted = localStorage.getItem(userKey);

  reactionBtns.forEach(btn => {
    const type = btn.dataset.reaction;
    const count = savedReactions[type] || 0;
    btn.querySelector('.reaction-count').textContent = count;

    if (userReacted === type) {
      btn.classList.add('reacted');
    }
  });

  reactionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.dataset.reaction;
      const previousReaction = localStorage.getItem(userKey);

      if (previousReaction === type) {
        savedReactions[type] = Math.max(0, (savedReactions[type] || 0) - 1);
        btn.querySelector('.reaction-count').textContent = savedReactions[type];
        btn.classList.remove('reacted');
        localStorage.removeItem(userKey);
      } else {
        if (previousReaction) {
          savedReactions[previousReaction] = Math.max(0, (savedReactions[previousReaction] || 0) - 1);
          document.querySelector(`[data-reaction="${previousReaction}"]`)
            .querySelector('.reaction-count').textContent = savedReactions[previousReaction];
          document.querySelector(`[data-reaction="${previousReaction}"]`)
            .classList.remove('reacted');
        }

        savedReactions[type] = (savedReactions[type] || 0) + 1;
        btn.querySelector('.reaction-count').textContent = savedReactions[type];
        btn.classList.add('reacted');
        localStorage.setItem(userKey, type);
      }

      localStorage.setItem(pageKey, JSON.stringify(savedReactions));
    });
  });
}

// Disqus Comments
if (document.getElementById('disqus_thread')) {
  var disqus_config = function () {
    this.page.url = window.location.href;
    this.page.identifier = window.location.pathname;
  };

  (function() {
    var d = document, s = d.createElement('script');
    s.src = 'https://innerpeacehub.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
  })();
}

// Contact Form Validation
function submitForm() {
  let isValid = true;

  const fields = [
    { id: 'name', error: 'name-error', message: 'Please enter your name' },
    { id: 'email', error: 'email-error', message: 'Please enter a valid email' },
    { id: 'subject', error: 'subject-error', message: 'Please enter a subject' },
    { id: 'message', error: 'message-error', message: 'Please enter your message' }
  ];

  // Clear previous errors
  fields.forEach(field => {
    document.getElementById(field.id).classList.remove('error');
    document.getElementById(field.error).textContent = '';
  });

  // Validate each field
  fields.forEach(field => {
    const input = document.getElementById(field.id);
    const value = input.value.trim();

    if (!value) {
      input.classList.add('error');
      document.getElementById(field.error).textContent = field.message;
      isValid = false;
    }

    // Extra email validation
    if (field.id === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        input.classList.add('error');
        document.getElementById(field.error).textContent = 'Please enter a valid email address';
        isValid = false;
      }
    }
  });

  if (isValid) {
    // Show success message
    document.getElementById('contact-form').style.display = 'none';
    document.getElementById('form-success').style.display = 'block';
  }
}

// Scroll Reveal Animations
const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

if (revealElements.length > 0) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15
  });

  revealElements.forEach(el => revealObserver.observe(el));
}

// Auto-dismiss flash messages
const flashMessages = document.querySelectorAll('.flash-message');
flashMessages.forEach(msg => {
  setTimeout(() => {
    msg.style.opacity = '0';
    msg.style.transition = 'opacity 0.5s';
    setTimeout(() => msg.remove(), 500);
  }, 4000);
});

// Reading Progress Bar
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.body.scrollHeight - window.innerHeight;
  if (docHeight > 0) {
    const progress = (scrollTop / docHeight) * 100;
    const bar = document.getElementById('progress-bar');
    if (bar) bar.style.width = progress + '%';
  }
});

// Scroll to Top Button
const scrollTopBtn = document.getElementById('scrollTopBtn');
window.addEventListener('scroll', () => {
  if (scrollTopBtn) {
    const isVisible = window.scrollY > 300;
    if (isVisible) {
      scrollTopBtn.classList.add('visible');
    } else {
      scrollTopBtn.classList.remove('visible');
    }
  }
});
if (scrollTopBtn) {
  scrollTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}