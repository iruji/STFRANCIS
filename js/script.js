// ===== Global Variables =====
let currentSlide = 0;
let currentNewsSlide = 0;
let slideInterval;
let newsSlideInterval;
let headerHeight = 0;
let lastScrollY = 0;
let ticking = false;

// ===== Hero Slider =====
function showHeroSlide(index) {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');

  slides.forEach(slide => slide.classList.remove('active'));
  dots.forEach(dot => dot.classList.remove('active'));

  slides[index].classList.add('active');
  dots[index].classList.add('active');
}

function nextHeroSlide() {
  const slides = document.querySelectorAll('.hero-slide');
  currentSlide = (currentSlide + 1) % slides.length;
  showHeroSlide(currentSlide);
}

function initHeroSlider() {
  const heroSlider = document.getElementById('hero-slider');
  const dots = document.querySelectorAll('.hero-dot');
  if (!heroSlider || dots.length === 0) return;

  showHeroSlide(currentSlide);
  slideInterval = setInterval(nextHeroSlide, 5000);

  heroSlider.addEventListener('mouseenter', () => clearInterval(slideInterval));
  heroSlider.addEventListener('mouseleave', () => slideInterval = setInterval(nextHeroSlide, 5000));

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      currentSlide = index;
      showHeroSlide(currentSlide);
      clearInterval(slideInterval);
      slideInterval = setInterval(nextHeroSlide, 5000);
    });
  });
}

// ===== News Slider =====
function initNewsSlider() {
  const newsSlider = document.getElementById('news-slider');
  const newsSlides = document.querySelectorAll('.news-slide');
  const newsPrevBtn = document.getElementById('news-prev');
  const newsNextBtn = document.getElementById('news-next');
  const newsIndicatorsContainer = document.getElementById('news-indicators');
  if (!newsSlider || newsSlides.length === 0) return;

  const slidesToShow = 4;
  const totalNewsSlides = newsSlides.length;
  const maxSlideIndex = Math.max(0, totalNewsSlides - slidesToShow);

  function updateNewsSlider() {
    const slideWidth = newsSlides[0].offsetWidth;
    const gap = 20;
    const translateX = -(currentNewsSlide * (slideWidth + gap));
    newsSlider.style.transform = `translateX(${translateX}px)`;
    updateNewsIndicators();
    updateNewsNavButtons();
  }

  function nextNewsSlide() {
    currentNewsSlide = (currentNewsSlide >= maxSlideIndex) ? 0 : currentNewsSlide + 1;
    updateNewsSlider();
  }

  function prevNewsSlide() {
    currentNewsSlide = (currentNewsSlide <= 0) ? maxSlideIndex : currentNewsSlide - 1;
    updateNewsSlider();
  }

  function updateNewsNavButtons() {
    if (newsPrevBtn) newsPrevBtn.disabled = currentNewsSlide === 0;
    if (newsNextBtn) newsNextBtn.disabled = currentNewsSlide >= maxSlideIndex;
  }

  function createNewsIndicators() {
    if (!newsIndicatorsContainer) return;
    newsIndicatorsContainer.innerHTML = '';
    for (let i = 0; i <= maxSlideIndex; i++) {
      const indicator = document.createElement('button');
      indicator.classList.add('news-indicator');
      indicator.addEventListener('click', () => {
        currentNewsSlide = i;
        updateNewsSlider();
        clearInterval(newsSlideInterval);
        newsSlideInterval = setInterval(nextNewsSlide, 8000);
      });
      newsIndicatorsContainer.appendChild(indicator);
    }
  }

  function updateNewsIndicators() {
    const indicators = document.querySelectorAll('.news-indicator');
    indicators.forEach((indicator, index) => {
      indicator.classList.toggle('active', index === currentNewsSlide);
    });
  }

  createNewsIndicators();
  updateNewsSlider();
  if (newsPrevBtn) newsPrevBtn.addEventListener('click', prevNewsSlide);
  if (newsNextBtn) newsNextBtn.addEventListener('click', nextNewsSlide);

  newsSlideInterval = setInterval(nextNewsSlide, 8000);

  newsSlider.addEventListener('mouseenter', () => clearInterval(newsSlideInterval));
  newsSlider.addEventListener('mouseleave', () => newsSlideInterval = setInterval(nextNewsSlide, 8000));

  // Touch support
  let startX = 0, isDragging = false;
  newsSlider.addEventListener('touchstart', e => { startX = e.touches[0].clientX; isDragging = true; clearInterval(newsSlideInterval); });
  newsSlider.addEventListener('touchend', e => {
    if (!isDragging) return;
    const deltaX = startX - e.changedTouches[0].clientX;
    if (Math.abs(deltaX) > 50) deltaX > 0 ? nextNewsSlide() : prevNewsSlide();
    isDragging = false;
    newsSlideInterval = setInterval(nextNewsSlide, 8000);
  });

  window.addEventListener('resize', updateNewsSlider);
}

// ===== Dropdowns =====
function initDropdownAccessibility() {
  const dropdowns = document.querySelectorAll('.dropdown');

  dropdowns.forEach(dropdown => {
    const button = dropdown.querySelector('.dropbtn');
    const content = dropdown.querySelector('.dropdown-content');
    if (!button || !content) return;

    dropdown.addEventListener('mouseenter', () => {
      content.style.opacity = '1';
      content.style.visibility = 'visible';
      content.style.pointerEvents = 'auto';
    });
    dropdown.addEventListener('mouseleave', () => {
      content.style.opacity = '0';
      content.style.visibility = 'hidden';
      content.style.pointerEvents = 'none';
    });

    button.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const isOpen = content.style.visibility === 'visible';
        content.style.opacity = isOpen ? '0' : '1';
        content.style.visibility = isOpen ? 'hidden' : 'visible';
        content.style.pointerEvents = isOpen ? 'none' : 'auto';
      }
    });
  });

  document.addEventListener('click', e => {
    dropdowns.forEach(dropdown => {
      const content = dropdown.querySelector('.dropdown-content');
      if (!dropdown.contains(e.target)) {
        content.style.opacity = '0';
        content.style.visibility = 'hidden';
        content.style.pointerEvents = 'none';
      }
    });
  });
}

// ===== Header Scroll (Fixed Version) =====
function updateHeader() {
  const header = document.getElementById('header-container');
  if (!header) return;
  
  const scrollY = window.scrollY;
  const scrollDifference = scrollY - lastScrollY;
  
  // If we're at the top, always show header
  if (scrollY <= headerHeight) {
    header.classList.remove('hidden', 'show-on-scroll-up');
  } 
  // If scrolling down and moved more than 5px, hide header
  else if (scrollDifference > 5) {
    header.classList.add('hidden');
    header.classList.remove('show-on-scroll-up');
  } 
  // If scrolling up and moved more than 5px, show header
  else if (scrollDifference < -5) {
    header.classList.remove('hidden');
    header.classList.add('show-on-scroll-up');
  }

  lastScrollY = scrollY;
  ticking = false;
}

// Alternative simpler version if the above doesn't work:
function updateHeaderSimple() {
  const header = document.getElementById('header-container');
  if (!header) return;
  
  const scrollY = window.scrollY;
  
  // At the top, always show
  if (scrollY <= headerHeight) {
    header.classList.remove('hidden', 'show-on-scroll-up');
  }
  // Scrolling down - hide header
  else if (scrollY > lastScrollY && scrollY > headerHeight) {
    header.classList.add('hidden');
    header.classList.remove('show-on-scroll-up');
  }
  // Scrolling up - show header
  else if (scrollY < lastScrollY) {
    header.classList.remove('hidden');
    header.classList.add('show-on-scroll-up');
  }

  lastScrollY = scrollY;
  ticking = false;
}

function requestHeaderUpdate() {
  if (!ticking) {
    requestAnimationFrame(updateHeader);
    ticking = true;
  }
}

// ===== Search Toggle =====
function initSearchToggle() {
  const searchIcon = document.getElementById('search-icon');
  const searchInput = document.getElementById('search-input');
  if (!searchIcon || !searchInput) return;

  searchIcon.addEventListener('click', () => {
    searchInput.classList.toggle('active');
    if (searchInput.classList.contains('active')) searchInput.focus();
    else { searchInput.blur(); searchInput.value = ''; }
  });

  document.addEventListener('click', e => {
    if (!searchIcon.contains(e.target) && !searchInput.contains(e.target)) {
      searchInput.classList.remove('active');
      searchInput.value = '';
    }
  });
}
function animateCounters() {
  const counters = document.querySelectorAll('.stat-number');
  if (!counters.length) return;

  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
        const counter = entry.target;
        const target = parseInt(counter.getAttribute('data-target'), 10);
        const duration = 2000;
        const increment = target / (duration / 16); // 60fps
        let current = 0;

        counter.classList.add('animated');

        const update = () => {
          current += increment;
          if (current < target) {
            counter.textContent = Math.floor(current).toLocaleString();
            requestAnimationFrame(update);
          } else {
            counter.textContent = target.toLocaleString();
          }
        };
        update();
      }
    });
  }, observerOptions);

  counters.forEach(counter => observer.observe(counter));
}

// Ensure this runs after window load to catch layout
window.addEventListener('load', () => {
  animateCounters();
});

// ===== Fade-In Sections =====
function fadeInSections() {
  const sections = document.querySelectorAll('.facebook-section, .departments-showcase, .news-section, .statistics-section');
  sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top < window.innerHeight - 50) {
      section.style.opacity = 1;
      section.style.transform = 'translateY(0)';
    }
  });
}

// ===== DOMContentLoaded Initialization =====
document.addEventListener('DOMContentLoaded', () => {
  headerHeight = document.getElementById('header-container')?.offsetHeight || 0;
  lastScrollY = window.scrollY;

  initHeroSlider();
  initNewsSlider();
  initDropdownAccessibility();
  initSearchToggle();

  // Add your other initialization functions here:
  // initDepartmentPanels();
  // initNewsSection();
  // initSmoothScrolling();
  // initFacebookPosts();
  // initAlumniTestimonials();
  // initFacebookInteractions();
  // initTestimonialQuotes();
  initStatisticsAnimation();
  animateCounters();
});

// ===== Window Events =====
window.addEventListener('scroll', () => {
  fadeInSections();
  requestHeaderUpdate();
});

window.addEventListener('resize', () => {
  const header = document.getElementById('header-container');
  if (header) headerHeight = header.offsetHeight;
  fadeInSections();
});
window.addEventListener('load', fadeInSections);

// Select all elements you want to fade in
const fadeInElements = document.querySelectorAll('.fade-in');

const observerOptions = {
  threshold: 0.5, // Triggers when 50% of the element is visible
  rootMargin: '0px 0px -50px 0px' // Optional: triggers slightly before fully visible
};

const fadeInObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible'); // Trigger CSS animation
      observer.unobserve(entry.target); // Stop observing after fade-in
    }
  });
}, observerOptions);

// Observe all fade-in elements
fadeInElements.forEach(el => fadeInObserver.observe(el));

