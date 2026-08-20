document.addEventListener("DOMContentLoaded", () => {
  const galleries = document.querySelectorAll(".bts-grid, .project-gallery");
  if (!galleries.length) return;

  const lightbox = document.createElement("div");
  lightbox.className = "lightbox";
  lightbox.innerHTML = '<span class="lightbox-arrow prev">&lsaquo;</span><img alt=""><span class="lightbox-arrow next">&rsaquo;</span><span class="close">&times;</span>';
  document.body.appendChild(lightbox);
  const lightboxImg = lightbox.querySelector("img");
  const prevArrow = lightbox.querySelector(".prev");
  const nextArrow = lightbox.querySelector(".next");

  let currentImgs = [];
  let currentIndex = 0;

  const show = (index) => {
    currentIndex = (index + currentImgs.length) % currentImgs.length;
    lightboxImg.src = currentImgs[currentIndex].src;
  };

  galleries.forEach((grid) => {
    const imgs = Array.from(grid.querySelectorAll("img"));
    imgs.forEach((img, i) => {
      img.addEventListener("click", () => {
        currentImgs = imgs;
        const multiple = imgs.length > 1;
        prevArrow.style.display = multiple ? "" : "none";
        nextArrow.style.display = multiple ? "" : "none";
        show(i);
        lightbox.classList.add("open");
      });
    });
  });

  prevArrow.addEventListener("click", (e) => {
    e.stopPropagation();
    show(currentIndex - 1);
  });
  nextArrow.addEventListener("click", (e) => {
    e.stopPropagation();
    show(currentIndex + 1);
  });

  const closeLightbox = () => lightbox.classList.remove("open");
  lightbox.addEventListener("click", closeLightbox);
  document.addEventListener("keydown", (e) => {
    if (!lightbox.classList.contains("open")) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowLeft") show(currentIndex - 1);
    if (e.key === "ArrowRight") show(currentIndex + 1);
  });
});
