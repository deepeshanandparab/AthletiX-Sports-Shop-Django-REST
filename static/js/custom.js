function scrolldiv() {
    var div = document.getElementById("search-product-filter");
    div.scrollIntoView();
  }


$(function() {
    $(".heart-animation").click(function() {
      $(this).toggleClass("animate");
    });
  });