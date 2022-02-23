$(document).ready(function(){
    $("#add_wishlist_btn").click(function(){
      $('.addtoast').toast('show');
    });
  });

$(document).ready(function(){
    $("#remove_wishlist_btn").click(function(){
      $('.removetoast').toast('show');
    });
  });



function addWishlist() {
    $('.addtoast').toast('show');
  }

function removeWishlist() {
    $('.removetoast').toast('show');
  }
  