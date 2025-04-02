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


// COURSES MANAGEMENT
class CourseManager {
    constructor() {
        this.courses = [];
        this.initEventListeners();
        this.loadCourses();
    }

    initEventListeners() {
        // Add Course Modal Triggers
        document.querySelector('.add-course-btn').addEventListener('click', () => this.showAddCourseModal());
        document.querySelector('#addCourseModal .close-modal').addEventListener('click', () => this.closeAddCourseModal());
        document.querySelector('#addCourseModal .cancel-btn').addEventListener('click', () => this.closeAddCourseModal());
        
        // Add Course Form Submit
        document.querySelector('.add-course-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addCourse();
        });

        // Search Functionality
        const searchInput = document.querySelector('.search-input');
        searchInput.addEventListener('input', () => this.filterCourses(searchInput.value));

        // Dynamically Generate Hole Par Inputs
        this.generateHolePars();
    }

    generateHolePars() {
        const holeParsGrid = document.querySelector('.hole-pars-grid');
        holeParsGrid.innerHTML = ''; // Clear existing inputs

        for (let i = 1; i <= 18; i++) {
            const holeParDiv = document.createElement('div');
            holeParDiv.classList.add('hole-par-input');
            holeParDiv.innerHTML = `
                <label for="hole${i}Par">Hole ${i}</label>
                <input type="number" id="hole${i}Par" min="3" max="5" value="4" required>
            `;
            holeParsGrid.appendChild(holeParDiv);
        }
    }

    showAddCourseModal() {
        const modal = document.getElementById('addCourseModal');
        modal.style.display = 'block';
    }

    closeAddCourseModal() {
        const modal = document.getElementById('addCourseModal');
        modal.style.display = 'none';
    }

    addCourse() {
        // Collect course details
        const courseName = document.getElementById('courseName').value;
        const courseLocation = document.getElementById('courseLocation').value;
        const courseThumbnail = document.getElementById('courseThumbnail').files[0];

        // Collect hole pars
        const holePars = [];
        for (let i = 1; i <= 18; i++) {
            const parInput = document.getElementById(`hole${i}Par`);
            holePars.push(parseInt(parInput.value));
        }

        // Calculate total par
        const totalPar = holePars.reduce((sum, par) => sum + par, 0);

        // Create course object
        const newCourse = {
            id: Date.now(), // Unique identifier
            name: courseName,
            location: courseLocation,
            totalPar: totalPar,
            holePars: holePars,
            thumbnail: courseThumbnail ? URL.createObjectURL(courseThumbnail) : 'default-course.jpg'
        };

        // Add to courses array
        this.courses.push(newCourse);

        // Update UI
        this.renderCourseTable();
        this.closeAddCourseModal();

        // Reset form
        document.querySelector('.add-course-form').reset();

        // Save to local storage
        this.saveCourses();
    }

    renderCourseTable() {
        const tableBody = document.querySelector('.courses-table tbody');
        tableBody.innerHTML = ''; // Clear existing rows

        this.courses.forEach(course => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="course-image-cell">
                    <img src="${course.thumbnail}" alt="${course.name}" class="course-thumbnail">
                </td>
                <td class="name-cell">${course.name}</td>
                <td class="location-cell">${course.location}</td>
                <td class="par-cell">${course.totalPar}</td>
                <td class="actions-cell">
                    <button class="view-details-btn" data-id="${course.id}">View Details</button>
                    <button class="edit-btn" data-id="${course.id}">Edit</button>
                    <button class="delete-btn" data-id="${course.id}">Delete</button>
                </td>
            `;

            // Add event listeners for action buttons
            row.querySelector('.view-details-btn').addEventListener('click', () => this.showCourseDetails(course));
            row.querySelector('.edit-btn').addEventListener('click', () => this.editCourse(course));
            row.querySelector('.delete-btn').addEventListener('click', () => this.deleteCourse(course.id));

            tableBody.appendChild(row);
        });
    }

    showCourseDetails(course) {
        const modal = document.getElementById('courseDetailsModal');
        const modalTitle = modal.querySelector('.course-details-title');
        const courseImage = modal.querySelector('.course-full-image');
        const courseInfo = modal.querySelector('.course-info');
        const holeParsTableBody = document.getElementById('holeParsTableBody');

        // Set course details
        modalTitle.textContent = course.name;
        courseImage.src = course.thumbnail;
        courseInfo.querySelector('#detailCourseName').textContent = course.name;
        courseInfo.querySelector('#detailCourseLocation').textContent = course.location;
        courseInfo.querySelector('#detailCoursePar').textContent = `Total Par: ${course.totalPar}`;

        // Populate hole pars table
        holeParsTableBody.innerHTML = '';
        course.holePars.forEach((par, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>Hole ${index + 1}</td>
                <td>${par}</td>
            `;
            holeParsTableBody.appendChild(row);
        });

        // Show modal
        modal.style.display = 'block';

        // Close modal event
        modal.querySelector('.close-modal').addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    editCourse(course) {
        // Implement edit functionality
        alert(`Edit functionality for ${course.name} to be implemented`);
    }

    deleteCourse(courseId) {
        // Confirm deletion
        if (!confirm('Are you sure you want to delete this course?')) return;

        // Remove course from array
        this.courses = this.courses.filter(course => course.id !== courseId);

        // Update UI and local storage
        this.renderCourseTable();
        this.saveCourses();
    }

    filterCourses(searchTerm) {
        const filteredCourses = this.courses.filter(course => 
            course.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
            course.location.toLowerCase().includes(searchTerm.toLowerCase())
        );

        // Render filtered courses
        this.renderFilteredCourses(filteredCourses);
    }

    renderFilteredCourses(filteredCourses) {
        const tableBody = document.querySelector('.courses-table tbody');
        tableBody.innerHTML = ''; // Clear existing rows

        filteredCourses.forEach(course => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="course-image-cell">
                    <img src="${course.thumbnail}" alt="${course.name}" class="course-thumbnail">
                </td>
                <td class="name-cell">${course.name}</td>
                <td class="location-cell">${course.location}</td>
                <td class="par-cell">${course.totalPar}</td>
                <td class="actions-cell">
                    <button class="view-details-btn" data-id="${course.id}">View Details</button>
                    <button class="edit-btn" data-id="${course.id}">Edit</button>
                    <button class="delete-btn" data-id="${course.id}">Delete</button>
                </td>
            `;

            // Add event listeners for action buttons
            row.querySelector('.view-details-btn').addEventListener('click', () => this.showCourseDetails(course));
            row.querySelector('.edit-btn').addEventListener('click', () => this.editCourse(course));
            row.querySelector('.delete-btn').addEventListener('click', () => this.deleteCourse(course.id));

            tableBody.appendChild(row);
        });
    }

    saveCourses() {
        // Save courses to local storage
        localStorage.setItem('golfCourses', JSON.stringify(this.courses));
    }

    loadCourses() {
        // Load courses from local storage
        const savedCourses = localStorage.getItem('golfCourses');
        if (savedCourses) {
            this.courses = JSON.parse(savedCourses);
            this.renderCourseTable();
        }
    }
}

// Initialize Course Manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const courseManager = new CourseManager();
});