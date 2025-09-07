// ===== Hero Slider Functionality =====
let currentSlide = 0;
const slides = document.querySelectorAll('.hero-slide');
const dots = document.querySelectorAll('.hero-dot');
const totalSlides = slides.length;

function showSlide(index) {
  // Remove active class from all slides and dots
  slides.forEach(slide => slide.classList.remove('active'));
  dots.forEach(dot => dot.classList.remove('active'));
  
  // Add active class to current slide and dot
  slides[index].classList.add('active');
  dots[index].classList.add('active');
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % totalSlides;
  showSlide(currentSlide);
}

// Auto-advance slides every 5 seconds
let slideInterval = setInterval(nextSlide, 5000);

// Pause slider on hover
const heroSlider = document.getElementById('hero-slider');
if (heroSlider) {
  heroSlider.addEventListener('mouseenter', () => {
    clearInterval(slideInterval);
  });

  heroSlider.addEventListener('mouseleave', () => {
    slideInterval = setInterval(nextSlide, 5000);
  });
}

// Dot navigation
dots.forEach((dot, index) => {
  dot.addEventListener('click', () => {
    currentSlide = index;
    showSlide(currentSlide);
    // Restart interval after manual selection
    clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 5000);
  });
});

// ===== Fade-in for sections =====
const sections = document.querySelectorAll('main .container section');

function fadeInSections() {
  sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top < window.innerHeight - 50) {
      section.style.opacity = 1;
      section.style.transform = 'translateY(0)';
    }
  });
}

// Initial load
window.addEventListener('load', () => { fadeInSections(); });

// Fade in on scroll
window.addEventListener('scroll', () => { fadeInSections(); });

// ===== Header Control =====
const headerContainer = document.getElementById('header-container');
const headerHeight = headerContainer.offsetHeight;
let lastScrollY = window.scrollY;
let ticking = false;

function updateHeader() {
  const scrollY = window.scrollY;
  const scrollDirection = scrollY > lastScrollY ? 'down' : 'up';
  
  if (scrollY <= headerHeight) {
    // At top of page - show normal header
    headerContainer.classList.remove('hidden', 'show-on-scroll-up');
  } else if (scrollDirection === 'down') {
    // Scrolling down - hide header
    headerContainer.classList.add('hidden');
    headerContainer.classList.remove('show-on-scroll-up');
  } else if (scrollDirection === 'up') {
    // Scrolling up - show header with slide down animation
    headerContainer.classList.remove('hidden');
    headerContainer.classList.add('show-on-scroll-up');
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

window.addEventListener('scroll', requestHeaderUpdate);

// ===== Search bar toggle =====
const searchIcon = document.getElementById('search-icon');
const searchInput = document.getElementById('search-input');

searchIcon.addEventListener('click', () => {
  searchInput.classList.toggle('active');
  if (searchInput.classList.contains('active')) searchInput.focus();
});