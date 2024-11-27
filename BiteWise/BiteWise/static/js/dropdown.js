document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggle = document.getElementById('dropdown-toggle');
    if (dropdownToggle) {
      dropdownToggle.addEventListener('click', function() {
        console.log('Dropdown toggle clicked!'); 
        const profileBtn = document.querySelector('.profile-btn');
        const profileImg = document.querySelector('.profile-img');
        const dropdownContent = document.getElementById('dropdown-content');
        const dropdownContainer = document.getElementById('dropdown-container')
  
        if (profileBtn.style.display === 'none') {
          profileBtn.style.display = 'inline';
          profileImg.style.display = 'inline';
          dropdownContent.style.display = 'none';

          dropdownContainer.style.justifyContent = 'space-between';
          dropdownContainer.style.borderRadius = '5px'
          dropdownContainer.style.height = '50px';
          dropdownContainer.style.width = '230px';
          dropdownToggle.style.transform = 'rotate(360deg)';
        } else {
            profileBtn.style.display = 'none';
            profileImg.style.display = 'none';
            dropdownContent.style.display = 'flex';  
            dropdownContent.style.flexDirection = 'column';
            dropdownContainer.style.justifyContent = 'right';
            dropdownContainer.style.borderRadius = '5px 5px 0 0';
            dropdownContainer.style.width = '190px';
            dropdownToggle.style.transform = 'rotate(180deg)';
        }
      });
    } else {
      console.error('Element with ID "dropdown-toggle" not found!');
    }
  });
  