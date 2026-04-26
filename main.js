document.addEventListener('DOMContentLoaded', () => {
    console.log('PBA UIN Jakarta Website Loaded');

    // Sticky header shadow with smooth transition
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.05)';
            header.style.padding = '0.5rem 0';
        } else {
            header.style.boxShadow = 'none';
            header.style.padding = '1rem 0';
        }
    });

    // Reveal elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                revealObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => {
        revealObserver.observe(el);
    });

    // News Slider Logic
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    let currentSlide = 0;
    const slideInterval = 5000; // 5 seconds

    function showSlide(n) {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        currentSlide = (n + slides.length) % slides.length;
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    // Auto slide
    let timer = setInterval(nextSlide, slideInterval);

    // Search Logic
    const searchContainer = document.querySelector('.search-container');
    const searchToggle = document.getElementById('searchToggle');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    searchToggle.addEventListener('click', () => {
        searchContainer.classList.toggle('active');
        if (searchContainer.classList.contains('active')) {
            searchInput.focus();
        }
    });

    // Close search on escape or click outside
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') searchContainer.classList.remove('active');
    });

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }

        // Search through all relevant content tags
        const tags = ['h1', 'h2', 'h3', 'h4', 'p', 'a'];
        const results = [];
        const seen = new Set();

        tags.forEach(tag => {
            document.querySelectorAll(tag).forEach(el => {
                const text = el.innerText.trim();
                if (text && text.toLowerCase().includes(query) && !seen.has(text)) {
                    if (el.closest('.search-container')) return; // Don't search the search bar itself
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

    // Close results when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchContainer.contains(e.target)) {
            searchContainer.classList.remove('active');
            searchResults.classList.remove('active');
        }
    });
});
