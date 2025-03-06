document.addEventListener('DOMContentLoaded', () => {
    // Enhanced Loading Screen
    const loadingScreen = document.querySelector('.loading-screen');
    const content = document.querySelectorAll('.content-reveal, .fade-up, .scale-in');
    
    // Simulate loading time (remove in production)
    setTimeout(() => {
        loadingScreen.classList.add('exit');
        document.body.style.overflow = 'visible';
        
        // Reveal content elements with delay
        content.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('active');
            }, 300 + (index * 100));
        });
    }, 2000);

    // Navbar Scroll Effect with smooth transition
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
            if (currentScroll > lastScroll) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        threshold: 0.1,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all animated elements
    document.querySelectorAll('.content-reveal, .fade-up, .scale-in, .about-content').forEach(el => {
        observer.observe(el);
    });

    // Mobile Menu with smooth transitions
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');
    let menuOpen = false;

    menuBtn.addEventListener('click', () => {
        if (!menuOpen) {
            menuBtn.classList.add('open');
            navLinks.style.display = 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '100%';
            navLinks.style.right = '0';
            navLinks.style.background = 'rgba(26, 26, 26, 0.95)';
            navLinks.style.padding = '2rem';
            navLinks.style.backdropFilter = 'blur(10px)';
            navLinks.style.transform = 'translateX(0)';
            menuOpen = true;
        } else {
            menuBtn.classList.remove('open');
            navLinks.style.transform = 'translateX(100%)';
            setTimeout(() => {
                navLinks.style.display = 'none';
            }, 300);
            menuOpen = false;
        }
    });

    // Enhanced Smooth Scroll with active link highlighting
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                // Close mobile menu if open
                if (menuOpen) {
                    menuBtn.click();
                }

                // Update active link
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');

                // Smooth scroll with easing
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
                const startPosition = window.pageYOffset;
                const distance = targetPosition - startPosition;
                const duration = 1000;
                let start = null;

                function animation(currentTime) {
                    if (start === null) start = currentTime;
                    const timeElapsed = currentTime - start;
                    const run = ease(timeElapsed, startPosition, distance, duration);
                    window.scrollTo(0, run);
                    if (timeElapsed < duration) requestAnimationFrame(animation);
                }

                function ease(t, b, c, d) {
                    t /= d / 2;
                    if (t < 1) return c / 2 * t * t + b;
                    t--;
                    return -c / 2 * (t * (t - 2) - 1) + b;
                }

                requestAnimationFrame(animation);
            }
        });
    });

    // Update active link on scroll
    window.addEventListener('scroll', () => {
        const sections = document.querySelectorAll('section');
        const navLinks = document.querySelectorAll('.nav-links a');
        
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop - 150) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === current) {
                link.classList.add('active');
            }
        });
    });

    // Parallax Effect with smooth performance
    const parallaxBoxes = document.querySelectorAll('.parallax-box');
    let ticking = false;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                parallaxBoxes.forEach(box => {
                    const speed = 0.5;
                    const rect = box.getBoundingClientRect();
                    const visible = rect.top < window.innerHeight && rect.bottom > 0;
                    
                    if (visible) {
                        const yPos = -(rect.top * speed);
                        box.style.transform = `translate3d(0, ${yPos}px, 0)`;
                    }
                });
                ticking = false;
            });
            ticking = true;
        }
    });

    // Form Handling with enhanced feedback
    const form = document.getElementById('reservierung');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loader-small"></span> Wird gesendet...';
            
            try {
                const formData = new FormData(form);
                const response = await fetch('/reservierung', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(Object.fromEntries(formData))
                });

                if (response.ok) {
                    // Success animation
                    submitBtn.innerHTML = '<i class="fas fa-check"></i> Gesendet!';
                    submitBtn.classList.add('success');
                    form.reset();
                    setTimeout(() => {
                        submitBtn.textContent = originalText;
                        submitBtn.classList.remove('success');
                        submitBtn.disabled = false;
                    }, 3000);
                } else {
                    throw new Error('Fehler bei der Übermittlung');
                }
            } catch (error) {
                // Error animation
                submitBtn.innerHTML = '<i class="fas fa-times"></i> Fehler';
                submitBtn.classList.add('error');
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.classList.remove('error');
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    }

    // Navigation Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Mobile Menu schließen nach Klick
                if (menuOpen) {
                    menuBtn.classList.remove('open');
                    navLinks.classList.remove('active');
                    menuOpen = false;
                }
            }
        });
    });

    // Aktive Navigation basierend auf Scroll-Position
    const sections = document.querySelectorAll('section[id]');
    const navItems = document.querySelectorAll('.nav-links a');

    function highlightNavigation() {
        const scrollY = window.scrollY;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionBottom = sectionTop + section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollY >= sectionTop && scrollY < sectionBottom) {
                navItems.forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('href') === `#${sectionId}`) {
                        item.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNavigation);
    highlightNavigation(); // Initial beim Laden
});
