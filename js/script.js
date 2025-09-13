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

// ===== Statistics Counter Animation =====
function animateCounters() {
  const counters = document.querySelectorAll('.stat-number');
  
  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
        const counter = entry.target;
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps
        let current = 0;
        
        counter.classList.add('animated'); // Prevent re-animation
        
        const updateCounter = () => {
          if (current < target) {
            current += increment;
            counter.textContent = Math.floor(current).toLocaleString();
            requestAnimationFrame(updateCounter);
          } else {
            counter.textContent = target.toLocaleString();
          }
        };
        
        updateCounter();
      }
    });
  }, observerOptions);

  counters.forEach(counter => {
    observer.observe(counter);
  });
}

// ===== Statistics Items Animation =====
function initStatisticsAnimation() {
  const statItems = document.querySelectorAll('.stat-item');
  
  const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -30px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 200);
      }
    });
  }, observerOptions);

  statItems.forEach((item) => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(30px)';
    item.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    observer.observe(item);
  });
}

// ===== Department Panels Animation =====
function initDepartmentPanels() {
  const departmentPanels = document.querySelectorAll('.department-panel');
  
  // Add entrance animation
  const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 200);
      }
    });
  }, observerOptions);

  departmentPanels.forEach((panel) => {
    panel.style.opacity = '0';
    panel.style.transform = 'translateY(30px)';
    panel.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(panel);
  });
}

// ===== Facebook Posts Animation =====
function initFacebookPosts() {
  const facebookPosts = document.querySelectorAll('.facebook-post');
  
  // Add entrance animation
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -30px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 300);
      }
    });
  }, observerOptions);

  facebookPosts.forEach((post) => {
    post.style.opacity = '0';
    post.style.transform = 'translateY(40px)';
    post.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    observer.observe(post);
  });
}

// ===== Alumni Testimonials Staggered Animation =====
function initAlumniTestimonials() {
  const testimonials = document.querySelectorAll('.alumni-testimonial');
  
  const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -20px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateX(0) scale(1)';
        }, index * 150);
      }
    });
  }, observerOptions);

  testimonials.forEach((testimonial, index) => {
    testimonial.style.opacity = '0';
    testimonial.style.transform = `translateX(${index % 2 === 0 ? '-20px' : '20px'}) scale(0.95)`;
    testimonial.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(testimonial);
  });
}

// ===== Enhanced fade-in for sections =====
const sections = document.querySelectorAll('.facebook-section, .departments-showcase, .news-section, .statistics-section');

function fadeInSections() {
  sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top < window.innerHeight - 50) {
      section.style.opacity = 1;
      section.style.transform = 'translateY(0)';
    }
  });
}

// ===== Enhanced Header Control =====
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
  } else if (scrollDirection === 'down' && scrollY > lastScrollY + 5) {
    // Scrolling down - hide header (with threshold to avoid micro-movements)
    headerContainer.classList.add('hidden');
    headerContainer.classList.remove('show-on-scroll-up');
  } else if (scrollDirection === 'up' && lastScrollY > scrollY + 5) {
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

// ===== Enhanced Search bar toggle =====
const searchIcon = document.getElementById('search-icon');
const searchInput = document.getElementById('search-input');

if (searchIcon && searchInput) {
  searchIcon.addEventListener('click', () => {
    searchInput.classList.toggle('active');
    if (searchInput.classList.contains('active')) {
      searchInput.focus();
    } else {
      searchInput.blur();
      searchInput.value = '';
    }
  });

  // Close search when clicking outside
  document.addEventListener('click', (e) => {
    if (!searchIcon.contains(e.target) && !searchInput.contains(e.target)) {
      searchInput.classList.remove('active');
      searchInput.value = '';
    }
  });
}

// ===== Enhanced News Section Interactions =====
function initNewsSection() {
  const newsItems = document.querySelectorAll('.news-item');
  
  newsItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
      // Optional: Pause any auto-scrolling if you add it later
      item.style.zIndex = '10';
    });

    item.addEventListener('mouseleave', () => {
      item.style.zIndex = '1';
    });
  });
}

// ===== Smooth Scrolling for Anchor Links =====
function initSmoothScrolling() {
  const links = document.querySelectorAll('a[href^="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      
      if (target) {
        const offsetTop = target.getBoundingClientRect().top + window.pageYOffset - headerContainer.offsetHeight;
        
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }
    });
  });
}

// ===== Improved Dropdown Accessibility =====
function initDropdownAccessibility() {
  const dropdowns = document.querySelectorAll('.dropdown');
  
  dropdowns.forEach(dropdown => {
    const button = dropdown.querySelector('.dropbtn');
    const content = dropdown.querySelector('.dropdown-content');
    
    if (button && content) {
      // Keyboard navigation
      button.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          content.style.opacity = content.style.opacity === '1' ? '0' : '1';
          content.style.visibility = content.style.visibility === 'visible' ? 'hidden' : 'visible';
          content.style.pointerEvents = content.style.pointerEvents === 'auto' ? 'none' : 'auto';
        }
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
          content.style.opacity = '0';
          content.style.visibility = 'hidden';
          content.style.pointerEvents = 'none';
        }
      });
    }
  });
}

// ===== Facebook Post Interactions =====
function initFacebookInteractions() {
  const facebookPosts = document.querySelectorAll('.facebook-post');
  
  facebookPosts.forEach(post => {
    // Add subtle hover effects
    post.addEventListener('mouseenter', () => {
      const profilePic = post.querySelector('.profile-pic');
      const facebookIcon = post.querySelector('.facebook-icon');
      
      if (profilePic) {
        profilePic.style.transform = 'scale(1.1)';
        profilePic.style.transition = 'transform 0.3s ease';
      }
      
      if (facebookIcon) {
        facebookIcon.style.transform = 'scale(1.2)';
        facebookIcon.style.transition = 'transform 0.3s ease';
      }
    });

    post.addEventListener('mouseleave', () => {
      const profilePic = post.querySelector('.profile-pic');
      const facebookIcon = post.querySelector('.facebook-icon');
      
      if (profilePic) {
        profilePic.style.transform = 'scale(1)';
      }
      
      if (facebookIcon) {
        facebookIcon.style.transform = 'scale(1)';
      }
    });
  });
}

// ===== Testimonial Quote Animation =====
function initTestimonialQuotes() {
  const quoteMarks = document.querySelectorAll('.quote-mark');
  
  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -10px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'quoteGlow 2s ease-in-out';
      }
    });
  }, observerOptions);

  quoteMarks.forEach(quote => {
    observer.observe(quote);
  });

  // Add CSS animation for quote glow
  const style = document.createElement('style');
  style.textContent = `
    @keyframes quoteGlow {
      0%, 100% { color: #ed1b24; text-shadow: none; }
      50% { color: #ff4b20; text-shadow: 0 0 10px rgba(237, 27, 36, 0.3); }
    }
  `;
  document.head.appendChild(style);
}

// ===== Initialize everything when DOM is loaded =====
document.addEventListener('DOMContentLoaded', () => {
  initDepartmentPanels();
  initNewsSection();
  initSmoothScrolling();
  initDropdownAccessibility();
  initFacebookPosts();
  initAlumniTestimonials();
  initFacebookInteractions();
  initTestimonialQuotes();
  initStatisticsAnimation();
  animateCounters();
});

// ===== Initialize on window load =====
window.addEventListener('load', () => { 
  fadeInSections();
});

// ===== Fade in sections on scroll =====
window.addEventListener('scroll', () => { 
  fadeInSections();
});

// ===== Handle window resize =====
window.addEventListener('resize', () => {
  // Recalculate header height on resize
  const newHeaderHeight = headerContainer.offsetHeight;
  if (newHeaderHeight !== headerHeight) {
    headerHeight = newHeaderHeight;
  }
});