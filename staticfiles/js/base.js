
AOS.init({ duration: 1200, once: true });

// Counter animation
const counters = document.querySelectorAll('.counter');
const speed = 200; // lower = faster

const animateCounters = () => {
counters.forEach(counter => {
    const updateCount = () => {
    const target = +counter.getAttribute('data-target');
    const count = +counter.innerText;
    const inc = Math.ceil(target / speed);

    if (count < target) {
        counter.innerText = count + inc;
        setTimeout(updateCount, 30);
    } else {
        counter.innerText = target;
    }
    };
    updateCount();
});
};

let countersStarted = false;
window.addEventListener('scroll', () => {
const countersSection = document.querySelector('.counters');
const sectionTop = countersSection.offsetTop - window.innerHeight + 100;
if (!countersStarted && window.scrollY > sectionTop) {
    animateCounters();
    countersStarted = true;
}
});