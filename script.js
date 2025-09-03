// Header slide up on scroll
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

// Fade-in sections on scroll
const faders = document.querySelectorAll('.fade-in-section');

const appearOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px"
};

const appearOnScroll = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, appearOptions);

faders.forEach(fader => {
  appearOnScroll.observe(fader);
});
