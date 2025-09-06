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

// ===== Header transform on scroll =====
const header = document.getElementById('main-header');
const topHeader = document.getElementById('top-header');
const topHeaderHeight = topHeader.offsetHeight;

header.style.transform = `translateY(${topHeaderHeight}px)`;

window.addEventListener('scroll', () => {
  if (window.scrollY >= topHeaderHeight) {
    header.style.transform = 'translateY(0)';
  } else {
    header.style.transform = `translateY(${topHeaderHeight - window.scrollY}px)`;
  }
});

// ===== Search bar toggle =====
const searchIcon = document.getElementById('search-icon');
const searchInput = document.getElementById('search-input');

searchIcon.addEventListener('click', () => {
  searchInput.classList.toggle('active');
  if (searchInput.classList.contains('active')) searchInput.focus();
});