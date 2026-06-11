// main.js - Common functionality for Yusuf Özcan's portfolio

document.addEventListener('DOMContentLoaded', () => {
    // Mobile navigation toggle
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('show');
            hamburger.textContent = hamburger.textContent === '☰' ? '✕' : '☰';
        });
        
        // Close mobile menu when a link is clicked
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('show');
                hamburger.textContent = '☰';
            });
        });
    }
    
    // Add active class to current navigation item
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(link => {
        const linkHref = link.getAttribute('href').split('/').pop();
        if (linkHref === currentPage) {
            link.classList.add('active');
        }
    });
    
    // Lazy load images
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imgObserver.observe(img);
        });
    } else {
        // Fallback for browsers without IntersectionObserver
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.getAttribute('data-src');
            img.removeAttribute('data-src');
        });
    }
    
    // Handle smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // --- Theme Switcher Functionality ---
    const globalThemeToggle = document.getElementById('globalThemeToggle');
    const htmlElement = document.documentElement;
    const navbarLogo = document.getElementById('navbarLogo');

    if (globalThemeToggle) {
        // Theme constants
        const themeLocalStorageKey = 'page-theme';
        const lightIcon = '☀️';
        const darkIcon = '🌙';
        
        // Determine correct paths for logo based on current page path
        let basePath = '';
        const currentPath = window.location.pathname;
        
        // Determine the depth based on directory structure
        if (currentPath.includes('/blog/essay/') || 
            currentPath.includes('/blog/poem/') || 
            currentPath.includes('/blog/reflection/') || 
            currentPath.includes('/blog/research/')) {
            // 2 levels deep: /blog/essay/, /blog/poem/, etc.
            basePath = '../../';
        } else if (currentPath.includes('/projects/') || 
                   currentPath.includes('/blog/')) {
            // 1 level deep: /projects/ or /blog/
            basePath = '../';
        } else {
            // Root level: index.html, about.html, etc.
            basePath = '';
        }
        
        const lightLogoSrc = `${basePath}assets/icons/logo.png`;
        const darkLogoSrc = `${basePath}assets/icons/logo_light.png`;

        // Function to apply theme and update logo
        const applyTheme = (theme) => {
            htmlElement.setAttribute('data-theme', theme);
            globalThemeToggle.textContent = theme === 'dark' ? lightIcon : darkIcon;

            // Update logo source based on theme
            if (navbarLogo) {
                navbarLogo.src = theme === 'dark' ? darkLogoSrc : lightLogoSrc;
            }

            localStorage.setItem(themeLocalStorageKey, theme);
        };

        // Apply saved theme on load or default based on system preference
        const savedTheme = localStorage.getItem(themeLocalStorageKey);
        const prefersDark = window.matchMedia && 
                            window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(savedTheme || (prefersDark ? 'dark' : 'light'));

        // Global Theme toggle event listener
        globalThemeToggle.addEventListener('click', function() {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }
});