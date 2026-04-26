document.addEventListener('DOMContentLoaded', () => {
    console.log('PBA UIN Jakarta Website Loaded');

    // 1. Header Sticky Logic
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // 2. Scroll Reveal Observer
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // 3. Generic Slider System
    function initSlider({ containerId, slidesClass, prevBtnId, nextBtnId, dotsClass, interval = 5000 }) {
        const slides = document.querySelectorAll(slidesClass);
        const prevBtn = document.getElementById(prevBtnId);
        const nextBtn = document.getElementById(nextBtnId);
        const dots = dotsClass ? document.querySelectorAll(dotsClass) : null;
        
        if (slides.length === 0) return;

        let currentIdx = 0;
        let timer;

        function showSlide(n) {
            slides.forEach(s => s.classList.remove('active'));
            if (dots) dots.forEach(d => d.classList.remove('active'));
            
            currentIdx = (n + slides.length) % slides.length;
            slides[currentIdx].classList.add('active');
            if (dots) dots[currentIdx].classList.add('active');
            
            resetTimer();
        }

        function resetTimer() {
            clearInterval(timer);
            timer = setInterval(() => showSlide(currentIdx + 1), interval);
        }

        // Event Listeners
        if (nextBtn) nextBtn.addEventListener('click', () => showSlide(currentIdx + 1));
        if (prevBtn) prevBtn.addEventListener('click', () => showSlide(currentIdx - 1));
        
        if (dots) {
            dots.forEach((dot, i) => {
                dot.addEventListener('click', () => showSlide(i));
            });
        }

        // Initialize
        showSlide(0);
    }

    // Initialize Sliders
    initSlider({ 
        slidesClass: '.slide', 
        dotsClass: '.dot', 
        interval: 6000 
    }); // Hero Slider

    initSlider({ 
        slidesClass: '.alumni-slide', 
        prevBtnId: 'prevAlumni', 
        nextBtnId: 'nextAlumni', 
        interval: 15000 
    }); // Alumni Slider

    initSlider({ 
        slidesClass: '.event-card', 
        prevBtnId: 'prevEvent', 
        nextBtnId: 'nextEvent', 
        interval: 8000 
    }); // Event Slider

    // 4. Search Logic
    const searchContainer = document.querySelector('.search-container');
    const searchToggle = document.getElementById('searchToggle');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    if (searchToggle && searchContainer) {
        searchToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            searchContainer.classList.toggle('active');
            if (searchContainer.classList.contains('active')) {
                searchInput.focus();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') searchContainer.classList.remove('active');
        });

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            if (query.length < 2) {
                searchResults.classList.remove('active');
                return;
            }

            const tags = ['h1', 'h2', 'h3', 'h4', 'p', 'a'];
            const results = [];
            const seen = new Set();

            tags.forEach(tag => {
                document.querySelectorAll(tag).forEach(el => {
                    const text = el.innerText.trim();
                    if (text && text.toLowerCase().includes(query) && !seen.has(text)) {
                        if (el.closest('.search-container')) return;
                        results.push(text);
                        seen.add(text);
                    }
                });
            });

            if (results.length > 0) {
                searchResults.innerHTML = results.slice(0, 8).map(res => {
                    const index = res.toLowerCase().indexOf(query);
                    const highlighted = res.substring(0, index) + 
                        `<mark>${res.substring(index, index + query.length)}</mark>` + 
                        res.substring(index + query.length);
                    return `<div class="search-item">${highlighted}</div>`;
                }).join('');
                searchResults.classList.add('active');
            } else {
                searchResults.innerHTML = '<div class="search-item">Tidak ditemukan hasil...</div>';
                searchResults.classList.add('active');
            }
        });

        document.addEventListener('click', (e) => {
            if (!searchContainer.contains(e.target)) {
                searchContainer.classList.remove('active');
                searchResults.classList.remove('active');
            }
        });
    }
});
