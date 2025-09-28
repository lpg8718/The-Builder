
AOS.init({ duration: 1000, once: true });

var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3, spaceBetween: 30, loop: true,
    autoplay: { delay: 2500, disableOnInteraction: false },
    pagination: { el: ".swiper-pagination", clickable: true },
    navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
    breakpoints: { 0: { slidesPerView: 1 }, 768: { slidesPerView: 2 }, 992: { slidesPerView: 3 } }
});

// Profile dropdown toggle
const profilePic = document.getElementById("profilePic");
const dropdownMenu = document.getElementById("dropdownMenu");
profilePic.addEventListener("click", () => {
    dropdownMenu.style.display = dropdownMenu.style.display === "flex" ? "none" : "flex";
});
window.addEventListener("click", (e) => {
    if (!profilePic.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.style.display = "none";
    }
});

var contractorSwiper = new Swiper(".contractorSwiper", {
    slidesPerView: 5,
    spaceBetween: 20,
    loop: true,
    autoplay: { delay: 2000, disableOnInteraction: false },
    pagination: { el: ".contractorSwiper .swiper-pagination", clickable: true },
    breakpoints: {
        0: { slidesPerView: 2 },
        576: { slidesPerView: 3 },
        992: { slidesPerView: 5 }
    }
});

