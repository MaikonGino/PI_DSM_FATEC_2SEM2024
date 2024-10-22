document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggle = document.getElementById('dropdown-toggle');
    
    // Verifica se o dropdownToggle existe
    if (dropdownToggle) {
      dropdownToggle.addEventListener('click', function() {
        console.log('Dropdown toggle clicked!');  // Mensagem de teste
  
        // Toggle visibility of the profile button and image
        const profileBtn = document.querySelector('.profile-btn');
        const profileImg = document.querySelector('.profile-img');
        const dropdownContent = document.getElementById('dropdown-content');
        const dropdownContainer = document.getElementById('dropdown-container')
        const dropdownContentHeader = document.getElementById('dropdown-content-header')
  
        // Toggle visibility
        if (profileBtn.style.display === 'none') {

            // Dropdown images
          profileBtn.style.display = 'inline';
          profileImg.style.display = 'inline';

            // Dropdown content
          dropdownContent.style.display = 'none';
            
            // Dropdown container
          dropdownContainer.style.justifyContent = 'space-between';
          dropdownContainer.style.borderRadius = '5px'
          dropdownContainer.style.height = '50px'
          dropdownContainer.style.width = '230px'

          // Arrow image
          dropdownToggle.style.transform = 'rotate(360deg)';
        } else {

            // Dropdown images
            profileBtn.style.display = 'none';
            profileImg.style.display = 'none';

            // Dropdown content header

            // Dropdown content
            dropdownContent.style.display = 'flex';  // Show dropdown
            dropdownContent.style.flexDirection = 'column';
            
          
            // Dropdown container
            dropdownContainer.style.justifyContent = 'right';
            dropdownContainer.style.borderRadius = '5px 5px 0 0';
            dropdownContainer.style.width = '190px';

            // Arrow image
            dropdownToggle.style.transform = 'rotate(180deg)';
        }
      });
    } else {
      console.error('Element with ID "dropdown-toggle" not found!');
    }
  });
  