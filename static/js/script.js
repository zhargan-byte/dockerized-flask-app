"use strict";

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function setupNavigation() {
    const toggle = document.querySelector(".menu-toggle");
    const links = document.querySelector(".nav-links");
    if (!toggle || !links) return;

    toggle.addEventListener("click", () => {
        const isOpen = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!isOpen));
        links.classList.toggle("is-open", !isOpen);
    });

    links.addEventListener("click", (event) => {
        if (event.target.closest("a")) {
            toggle.setAttribute("aria-expanded", "false");
            links.classList.remove("is-open");
        }
    });
}

async function updateHealthStatus() {
    const status = document.querySelector("[data-health-status]");
    const label = document.querySelector("[data-health-label]");
    if (!status || !label) return;

    try {
        const response = await fetch("/health", {
            headers: { Accept: "application/json" },
            cache: "no-store",
        });
        const data = await response.json();
        if (!response.ok || data.status !== "healthy") {
            throw new Error("Unhealthy response");
        }
        status.dataset.state = "healthy";
        label.textContent = "Service healthy";
    } catch (error) {
        status.dataset.state = "unavailable";
        label.textContent = "Service unavailable";
    }
}

function setupRevealAnimations() {
    const items = document.querySelectorAll(".reveal");
    if (reducedMotion || !("IntersectionObserver" in window)) {
        items.forEach((item) => item.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.14 }
    );
    items.forEach((item) => observer.observe(item));
}

function setupTiltEffect() {
    const card = document.querySelector("[data-tilt]");
    if (!card || reducedMotion || !window.matchMedia("(pointer: fine)").matches) return;

    card.addEventListener("pointermove", (event) => {
        const bounds = card.getBoundingClientRect();
        const rotateX = ((event.clientY - bounds.top) / bounds.height - 0.5) * -7;
        const rotateY = ((event.clientX - bounds.left) / bounds.width - 0.5) * 7;
        card.style.setProperty("--rotate-x", `${rotateX.toFixed(2)}deg`);
        card.style.setProperty("--rotate-y", `${rotateY.toFixed(2)}deg`);
    });

    card.addEventListener("pointerleave", () => {
        card.style.setProperty("--rotate-x", "0deg");
        card.style.setProperty("--rotate-y", "0deg");
    });
}

setupNavigation();
updateHealthStatus();
setupRevealAnimations();
setupTiltEffect();
