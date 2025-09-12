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

// ===== News Slider Functionality =====
let currentNewsSlide = 0;
const newsSlides = document.querySelectorAll('.news-slide');
const newsSlider = document.getElementById('news-slider');
const totalNewsSlides = newsSlides.length;

function updateNewsSlider() {
  if (newsSlider) {
    // Calculate how many slides to show based on screen width
    const slideWidth = 25; // 25% for desktop
    const mobileSlideWidth = 80; // 80% for mobile
    const isMobile = window.innerWidth <= 768;
    const width = isMobile ? mobileSlideWidth : slideWidth;
    
    const translateX = -currentNewsSlide * (width + 2); // 2% for gap
    newsSlider.style.transform = `translateX(${translateX}%)`;
  }
}

function changeNewsSlide(direction) {
  const isMobile = window.innerWidth <= 768;
  const maxSlides = isMobile ? totalNewsSlides - 1 : totalNewsSlides - 3;
  
  currentNewsSlide += direction;
  
  // Wrap around
  if (currentNewsSlide > maxSlides) {
    currentNewsSlide = 0;
  } else if (currentNewsSlide < 0) {
    currentNewsSlide = maxSlides;
  }
  
  updateNewsSlider();
}

// Auto-advance news slides every 6 seconds
let newsSlideInterval = setInterval(() => {
  changeNewsSlide(1);
}, 6000);

// Pause news slider on hover
const newsSliderContainer = document.querySelector('.news-slider-container');
if (newsSliderContainer) {
  newsSliderContainer.addEventListener('mouseenter', () => {
    clearInterval(newsSlideInterval);
  });

  newsSliderContainer.addEventListener('mouseleave', () => {
    newsSlideInterval = setInterval(() => {
      changeNewsSlide(1);
    }, 6000);
  });
}

// Update slider on window resize
window.addEventListener('resize', updateNewsSlider);

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
window.addEventListener('load', () => { 
  fadeInSections(); 
  updateNewsSlider();
});

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