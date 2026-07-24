const header = document.querySelector("[data-auto-hide]");
let lastScrollY = window.scrollY;

function updateHeader() {
  if (!header) return;
  const current = window.scrollY;
  const movingDown = current > lastScrollY && current > 120;
  header.classList.toggle("is-hidden", movingDown);
  lastScrollY = current;
}

window.addEventListener("scroll", updateHeader, { passive: true });
