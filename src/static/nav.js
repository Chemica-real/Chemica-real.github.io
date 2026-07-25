const header = document.querySelector("[data-auto-hide]");
const audio = document.querySelector("#site-audio");
const audioToggle = document.querySelector("[data-audio-toggle]");
const articlePager = document.querySelector("[data-article-pager]");
let lastScrollY = window.scrollY;
const AUDIO_KEY = "chemica-audio-state";
let pagerTimer = 0;

function updateHeader() {
  if (!header) return;
  const current = window.scrollY;
  const movingDown = current > lastScrollY && current > 120;
  header.classList.toggle("is-hidden", movingDown);
  lastScrollY = current;
}

window.addEventListener("scroll", updateHeader, { passive: true });

function readAudioState() {
  try {
    return JSON.parse(localStorage.getItem(AUDIO_KEY) || "{}");
  } catch {
    return {};
  }
}

function writeAudioState({ playing, userPaused }) {
  if (!audio) return;
  localStorage.setItem(
    AUDIO_KEY,
    JSON.stringify({
      playing,
      userPaused,
      time: Number.isFinite(audio.currentTime) ? audio.currentTime : 0,
      updatedAt: Date.now(),
    })
  );
}

function setProgress() {
  if (!audioToggle || !audio || !Number.isFinite(audio.duration) || audio.duration <= 0) {
    audioToggle?.style.setProperty("--progress", "0deg");
    return;
  }
  const progress = (audio.currentTime / audio.duration) * 360;
  audioToggle.style.setProperty("--progress", `${progress}deg`);
}

async function playAudio() {
  if (!audio) return;
  try {
    await audio.play();
    audioToggle?.classList.add("is-playing");
    audioToggle?.classList.remove("needs-gesture");
    writeAudioState({ playing: true, userPaused: false });
  } catch {
    audioToggle?.classList.remove("is-playing");
    audioToggle?.classList.add("needs-gesture");
    writeAudioState({ playing: false, userPaused: false });
  }
}

function pauseAudio() {
  if (!audio) return;
  audio.pause();
  audioToggle?.classList.remove("is-playing");
  audioToggle?.classList.remove("needs-gesture");
  writeAudioState({ playing: false, userPaused: true });
}

function initAudio() {
  if (!audio || !audioToggle) return;
  audio.volume = 0.42;
  const state = readAudioState();
  if (Number.isFinite(state.time)) {
    audio.currentTime = state.time;
  }

  audio.addEventListener("timeupdate", () => {
    setProgress();
    if (!audio.paused) writeAudioState({ playing: true, userPaused: false });
  });
  audio.addEventListener("loadedmetadata", setProgress);
  audioToggle.addEventListener("click", () => {
    if (audio.paused) {
      playAudio();
    } else {
      pauseAudio();
    }
  });
  window.addEventListener("pagehide", () => {
    writeAudioState({
      playing: !audio.paused,
      userPaused: audio.paused,
    });
  });
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
  window.addEventListener(
    "touchmove",
    () => {
      showArticlePager();
    },
    { passive: true }
  );
  document.addEventListener("mousemove", (event) => {
    if (window.innerHeight - event.clientY < 120) showArticlePager();
  });
  articlePager.addEventListener("mouseenter", showArticlePager);
}

initAudio();
initArticlePager();
