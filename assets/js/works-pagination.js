document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const itemsPerPage = 12;  // Maximum 8 items per page
    let galleryItems = document.querySelectorAll('.gallery-item');
    const galleryContainer = document.querySelector('.gallery');
    const filterButtons = document.querySelectorAll('.filter-btn');
    let currentPage = 1;
    let currentFilter = 'all';
    
    // Create pagination container if it doesn't exist
    let paginationContainer = document.querySelector('.works-pagination');
    if (!paginationContainer) {
        paginationContainer = document.createElement('div');
        paginationContainer.className = 'works-pagination';
        // Insert after gallery
        galleryContainer.parentNode.insertBefore(paginationContainer, galleryContainer.nextSibling);
    }
    
    // Initial setup
    initializeFilters();
    updateView();
    
    // Initialize filter functionality
    function initializeFilters() {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Update current filter
                currentFilter = this.getAttribute('data-filter');
                
                // Reset to page 1 when changing filters
                currentPage = 1;
                
                // Update view with new filter
                updateView();
            });
        });
    }
    
    // Main function to update the view based on current filter and page
    function updateView() {
        // Get filtered items
        const filteredItems = Array.from(galleryItems).filter(item => {
            if (currentFilter === 'all') return true;
            return item.getAttribute('data-category').includes(currentFilter);
        });
        
        // Calculate total pages for filtered items
        const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
        
        // Ensure current page is valid
        if (currentPage > totalPages) {
            currentPage = totalPages > 0 ? totalPages : 1;
        }
        
        // Hide all items first
        galleryItems.forEach(item => {
            item.style.display = 'none';
        });
        
        // Calculate which items to show
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, filteredItems.length);
        
        // Show only the filtered items for the current page
        for (let i = startIndex; i < endIndex; i++) {
            filteredItems[i].style.display = 'block';
        }
        
        // Update pagination
        updatePagination(totalPages);
    }
    
    // Function to update pagination controls
    function updatePagination(totalPages) {
        paginationContainer.innerHTML = '';
        
        // Only show pagination if there are multiple pages
        if (totalPages <= 1) {
            return;
        }
        
        // Add prev button if not on first page
        if (currentPage > 1) {
            const prevLink = document.createElement('a');
            prevLink.textContent = '← Prev';
            prevLink.className = 'prev-page';
            prevLink.href = '#';
            prevLink.addEventListener('click', function(e) {
                e.preventDefault();
                currentPage--;
                updateView();
                scrollToGallery();
            });
            paginationContainer.appendChild(prevLink);
        }
        
        // Add page numbers
        for (let i = 1; i <= totalPages; i++) {
            // Limit visible page numbers to improve usability for many pages
            if (totalPages > 7) {
                // Always show first, last, current and pages around current
                if (i !== 1 && i !== totalPages && 
                    Math.abs(i - currentPage) > 1 && 
                    i !== currentPage) {
                    
                    // Add ellipsis for skipped pages (but only once)
                    if (i === 2 || i === totalPages - 1) {
                        const ellipsis = document.createElement('span');
                        ellipsis.textContent = '...';
                        ellipsis.className = 'pagination-ellipsis';
                        paginationContainer.appendChild(ellipsis);
                    }
                    continue;
                }
            }
            
            const pageLink = document.createElement(i === currentPage ? 'span' : 'a');
            pageLink.textContent = i;
            pageLink.className = i === currentPage ? 'current-page' : '';
            
            if (i !== currentPage) {
                pageLink.href = '#';
                pageLink.addEventListener('click', function(e) {
                    e.preventDefault();
                    currentPage = i;
                    updateView();
                    scrollToGallery();
                });
            }
            
            paginationContainer.appendChild(pageLink);
        }
        
        // Add next button if not on last page
        if (currentPage < totalPages) {
            const nextLink = document.createElement('a');
            nextLink.textContent = 'Next →';
            nextLink.className = 'next-page';
            nextLink.href = '#';
            nextLink.addEventListener('click', function(e) {
                e.preventDefault();
                currentPage++;
                updateView();
                scrollToGallery();
            });
            paginationContainer.appendChild(nextLink);
        }
    }
    
    // Helper function to scroll to top of gallery section
    function scrollToGallery() {
        document.querySelector('#works').scrollIntoView({ behavior: 'smooth' });
    }
    
    // URL handling to restore state from URL hash
    function parseUrlHash() {
        const hash = window.location.hash;
        if (hash) {
            // Format: #page/1/filter/installation
            const parts = hash.substring(1).split('/');
            for (let i = 0; i < parts.length; i += 2) {
                if (parts[i] === 'page' && parts[i+1]) {
                    currentPage = parseInt(parts[i+1]) || 1;
                }
                if (parts[i] === 'filter' && parts[i+1]) {
                    currentFilter = parts[i+1];
                    // Update active filter button
                    filterButtons.forEach(btn => {
                        if (btn.getAttribute('data-filter') === currentFilter) {
                            btn.classList.add('active');
                        } else {
                            btn.classList.remove('active');
                        }
                    });
                }
            }
        }
    }
    
    function updateUrlHash() {
        // Update URL hash: #page/1/filter/installation
        window.history.replaceState(null, null, 
            `#page/${currentPage}/filter/${currentFilter}`);
    }
    
    // Check for hash in URL on page load
    parseUrlHash();
    updateView();
    
    // Update hash when page changes
    window.addEventListener('popstate', function() {
        parseUrlHash();
        updateView();
    });
});