document.addEventListener('DOMContentLoaded', function() {
  // Star Rating Widget Interaction
  const starLabels = document.querySelectorAll('.star-rating-label');
  const starWidget = document.querySelector('.star-rating-widget');
  
  // Initialize display for already selected rating
  if (starWidget) {
    const checkedInput = starWidget.querySelector('input[type="radio"]:checked');
    if (checkedInput) {
      const selectedValue = parseInt(checkedInput.value);
      starLabels.forEach((label, index) => {
        if (index + 1 <= selectedValue) {
          label.classList.add('selected');
        }
      });
    }
  }
  
  starLabels.forEach((label, labelIndex) => {
    label.addEventListener('click', function(e) {
      const value = this.getAttribute('data-value');
      const input = this.querySelector('.star-rating-input');
      
      // Check the radio button
      if (input) {
        input.checked = true;
      }
      
      // Update all stars up to this value
      starLabels.forEach((lbl, index) => {
        if (index + 1 <= value) {
          lbl.classList.add('selected');
        } else {
          lbl.classList.remove('selected');
        }
      });
    });
    
    // Highlight on hover
    label.addEventListener('mouseover', function() {
      const value = this.getAttribute('data-value');
      starLabels.forEach((lbl, index) => {
        if (index + 1 <= value) {
          lbl.classList.add('hover');
        } else {
          lbl.classList.remove('hover');
        }
      });
    });
  });
  
  // Remove hover effect when leaving the widget
  if (starWidget) {
    starWidget.addEventListener('mouseleave', function() {
      starLabels.forEach(label => {
        label.classList.remove('hover');
      });
    });
  }
  
  // Like/Dislike Button Placeholder (no backend yet)
  const helpfulBtns = document.querySelectorAll('.helpful-btn');
  const unhelpfulBtns = document.querySelectorAll('.unhelpful-btn');
  
  helpfulBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      alert('Функція буде реалізована пізніше');
    });
  });
  
  unhelpfulBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      alert('Функція буде реалізована пізніше');
    });
  });
  
  
  // Scroll-to-Top Button
  const scrollToTopBtn = document.getElementById('scrollToTopBtn');
  
  if (scrollToTopBtn) {
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 300) {
        scrollToTopBtn.classList.add('show');
      } else {
        scrollToTopBtn.classList.remove('show');
      }
    });
    
    // Smooth scroll to top
    scrollToTopBtn.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
});
