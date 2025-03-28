// Single Page Application (SPA) Navigation
document.addEventListener('DOMContentLoaded', () => {
    // Select all navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');

            // Hide all page views
            document.querySelectorAll('.page-view').forEach(view => {
                view.style.display = 'none';
            });

            // Get the page ID
            const pageId = this.getAttribute('data-page');

            // Special handling for home view
            if (pageId === 'home') {
                document.getElementById('home-view').style.display = 'block';
            } else {
                // Hide home view and show specific page view
                document.getElementById('home-view').style.display = 'none';
                document.getElementById(`${pageId}-view`).style.display = 'block';
            }
        });
    });
});