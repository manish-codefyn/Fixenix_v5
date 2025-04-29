

//<!--logout alert -->
 
    function confirmFunction() {
        event.preventDefault(); // prevent form submit
        var form = event.target.form; // storing the form
        Swal.fire({
          title: 'Are you sure?',
          text: "Want to logout!",
          type: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes,Logout!'
        }).then((result) => {
            if (result.value) {
                form.submit();
               }
        })
    }

//MObile Footer
var navItems = document.querySelectorAll(".bloc-icon");

navItems.forEach(function(e, i) {
  e.addEventListener("click", function(e) {
    navItems.forEach(function(e2, i2) {
      e2.classList.remove("block-icon-active");
    });
    this.classList.add("block-icon-active");
  });
});


(function () {
    'use strict'
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
      new bootstrap.Tooltip(tooltipTriggerEl)
    })
  })()

  $(document).ready(function() {
    $("#sidebarCollapse").on("click", function() {
      $("#sidebar").addClass("active");
    });
  
    $("#sidebarCollapseX").on("click", function() {
      $("#sidebar").removeClass("active");
    });
  
    $("#sidebarCollapse").on("click", function() {
      if ($("#sidebar").hasClass("active")) {
        $(".overlay").addClass("visible");
        console.log("it's working!");
      }
    });
  
    $("#sidebarCollapseX").on("click", function() {
      $(".overlay").removeClass("visible");
    });
  });
  

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

// for top fix
	document.addEventListener("DOMContentLoaded", function(){
		
		window.addEventListener('scroll', function() {
	       
			if (window.scrollY > 50) {
				document.getElementById('navbar_top').classList.add('is-scrolling');
				// add padding top to show content behind navbar
				navbar_height = document.querySelector('.navbar').offsetHeight;
				document.body.style.paddingTop = navbar_height + 'px';
			} else {
			 	document.getElementById('navbar_top').classList.remove('is-scrolling');
				 // remove padding top from body
				document.body.style.paddingTop = '0';
			} 
		});
	}); 
	// DOMContentLoaded  end


  ( function( window, $, undefined ) {

'use strict';

////////////// Begin jQuery and grab the $ ////////////////////////////////////////

$(document).ready(function() {

  function is_scrolling() {

    var $element = $('.site-header'),
        $nav_height = $element.outerHeight( true );

    if ($(this).scrollTop() >= $nav_height ) { //if scrolling is equal to or greater than the nav height add a class
  
      $element.addClass( 'is-scrolling');

    } else { //is back at the top again, remove the class
   
      $element.removeClass( 'is-scrolling');
    }
    
  }//end is_scrolling();

$( window ).scroll(_.throttle(is_scrolling, 200));
  
  
}); //* end ready


})(this, jQuery);

