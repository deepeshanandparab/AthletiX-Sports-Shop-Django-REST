// $(window).on("load",function(){
//   $(".loader-wrapper").fadeOut("slow");
//   $('html, body').css({'overflow': 'auto','height': 'auto'})
//   });

  

function scrolldiv() {
    var div = document.getElementById("search-product-filter");
    div.scrollIntoView();
  }


$(function() {
    $(".heart-animation").click(function() {
      $(this).toggleClass("animate");
    });
  });



document.addEventListener('readystatechange', event => { 
    // When window loaded ( external resources are loaded too- `css`,`src`, etc...) 
    if (event.target.readyState === "complete") {
        $('html, body').css({'overflow': 'hidden','height': 'auto'})

        setTimeout(function(){
          $(".loader-wrapper").fadeOut("slow");
          $('html, body').css({'overflow': 'auto','height': 'auto'})
        }, 800);
        
    }
});