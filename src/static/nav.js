const header = document.querySelector("[data-auto-hide]");
const articlePager = document.querySelector("[data-article-pager]");
let lastScrollY = window.scrollY;
let pagerTimer = 0;

function updateHeader() {
  if (!header) return;
  const current = window.scrollY;
  const movingDown = current > lastScrollY && current > 120;
  header.classList.toggle("is-hidden", movingDown);
  lastScrollY = current;
}

function showArticlePager() {
  if (!articlePager) return;
  articlePager.classList.add("is-visible");
  window.clearTimeout(pagerTimer);
  pagerTimer = window.setTimeout(() => {
    articlePager.classList.remove("is-visible");
  }, 1600);
}

function initArticlePager() {
  if (!articlePager) return;
  window.addEventListener(
    "wheel",
    (event) => {
      if (event.deltaY > 0) showArticlePager();
    },
    { passive: true }
  );
  window.addEventListener("touchmove", showArticlePager, { passive: true });
  document.addEventListener("mousemove", (event) => {
    if (window.innerHeight - event.clientY < 120) showArticlePager();
  });
  articlePager.addEventListener("mouseenter", showArticlePager);
}

window.addEventListener("scroll", updateHeader, { passive: true });
initArticlePager();
