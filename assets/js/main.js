document.addEventListener("DOMContentLoaded", () => {
  const grid = document.querySelector(".bts-grid");
  if (!grid) return;

  const lightbox = document.createElement("div");
  lightbox.className = "lightbox";
  lightbox.innerHTML = '<span class="close">&times;</span><img alt="">';
  document.body.appendChild(lightbox);
  const lightboxImg = lightbox.querySelector("img");

  grid.querySelectorAll("img").forEach((img) => {
    img.addEventListener("click", () => {
      lightboxImg.src = img.src;
      lightbox.classList.add("open");
    });
  });

  const closeLightbox = () => lightbox.classList.remove("open");
  lightbox.addEventListener("click", closeLightbox);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeLightbox();
  });
});
