const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const navItems = document.querySelectorAll(".nav-links a");
const sections = document.querySelectorAll("main section[id]");
const year = document.querySelector("#year");
const optionalImages = document.querySelectorAll("[data-optional-image]");
const revealTargets = document.querySelectorAll(
  ".hero-copy, .profile-card, .section-heading, #about .narrow, .process-step, .skill-grid .card, .project-card, .contact-card, .portfolio-hero, .portfolio-overview article, .portfolio-section-heading, .portfolio-section > p, .portfolio-card-grid article, .timeline-list article, .problem-flow article, .tech-logo-grid article"
);

if (year) {
  year.textContent = new Date().getFullYear();
}

optionalImages.forEach((image) => {
  const frame = image.closest(".image-frame");

  if (image.complete && image.naturalWidth > 0) {
    frame?.classList.add("has-image");
  }

  image.addEventListener("load", () => {
    frame?.classList.add("has-image");
  });

  image.addEventListener("error", () => {
    frame?.classList.remove("has-image");
    image.removeAttribute("src");
  });
});

navToggle?.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  navToggle.setAttribute("aria-expanded", String(isOpen));
  navToggle.setAttribute("aria-label", isOpen ? "메뉴 닫기" : "메뉴 열기");
});

navItems.forEach((item) => {
  item.addEventListener("click", () => {
    navLinks.classList.remove("open");
    navToggle?.setAttribute("aria-expanded", "false");
    navToggle?.setAttribute("aria-label", "메뉴 열기");
  });
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;

      navItems.forEach((item) => {
        item.classList.toggle("active", item.getAttribute("href") === `#${entry.target.id}`);
      });
    });
  },
  {
    rootMargin: "-40% 0px -50% 0px",
    threshold: 0,
  }
);

sections.forEach((section) => observer.observe(section));

revealTargets.forEach((target, index) => {
  target.classList.add("reveal");
  target.style.setProperty("--reveal-delay", `${Math.min(index % 4, 3) * 80}ms`);
});

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;

      entry.target.classList.add("visible");
      revealObserver.unobserve(entry.target);
    });
  },
  {
    rootMargin: "0px 0px -12% 0px",
    threshold: 0.12,
  }
);

revealTargets.forEach((target) => revealObserver.observe(target));
