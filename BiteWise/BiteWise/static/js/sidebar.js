document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".sidebar-link");
    const sections = document.querySelectorAll(".content-section");

    // Função para ativar a seção correta
    function activateSection(sectionName) {
        // Remove classe 'active' de todos os links
        links.forEach(link => link.classList.remove("active"));

        // Esconde todas as seções
        sections.forEach(section => section.style.display = "none");

        // Encontrar o link e a seção correta
        const activeLink = document.querySelector(`.sidebar-link[data-target="${sectionName}"]`);
        const activeSection = document.getElementById(sectionName);

        // Ativar link e exibir a seção
        if (activeLink && activeSection) {
            activeLink.classList.add("active");
            activeSection.style.display = "block";
        }
    }

    // Obter parâmetro 'section' da URL
    const urlParams = new URLSearchParams(window.location.search);
    const section = urlParams.get('section') || 'profile-content'; // Padrão para 'profile-content'

    // Ativar a seção correta com base no parâmetro da URL
    activateSection(section);

    // Configurar clique nos links da sidebar
    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const targetSection = this.getAttribute("data-target");

            // Atualiza a URL sem recarregar a página
            const newUrl = window.location.pathname + `?section=${targetSection}`;
            window.history.pushState({}, '', newUrl);

            // Ativar a nova seção
            activateSection(targetSection);
        });
    });
});
