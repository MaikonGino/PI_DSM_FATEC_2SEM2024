document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".sidebar-link");
    const sections = document.querySelectorAll(".content-section");

    
    function activateSection(sectionName) {
        links.forEach(link => link.classList.remove("active"));
        sections.forEach(section => section.style.display = "none");
        const activeLink = document.querySelector(`.sidebar-link[data-target="${sectionName}"]`);
        const activeSection = document.getElementById(sectionName);
        if (activeLink && activeSection) {
            activeLink.classList.add("active");
            activeSection.style.display = "block";
        }
    }

    
    const urlParams = new URLSearchParams(window.location.search);
    const section = urlParams.get('section') || 'profile-content'; 
    activateSection(section);

    
    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetSection = this.getAttribute("data-target");
            const newUrl = window.location.pathname + `?section=${targetSection}`;
            window.history.pushState({}, '', newUrl);
            activateSection(targetSection);
        });
    });
});
