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


function changeShippingCostZero()
{
  cost = document.getElementById('shippingcost')
  cost.innerText = '₹ 0'; 

  subtotal = document.getElementById('subtotal').textContent
  total = document.getElementById('total')
  
  if(subtotal.length > 3 && subtotal.length == 4)
  {
    value = subtotal.substring(0, 1) + "," + subtotal.substring(1, subtotal.length);
    total.innerText = "₹ "+ value
    // 1000 to 1,000
  }
  else if(subtotal.length > 3 && subtotal.length == 5)
  {
    value = subtotal.substring(0, 2) + "," + subtotal.substring(2, subtotal.length);
    total.innerText = "₹ "+ value
    // 10000 to 10,000
  }
  else if(subtotal.length > 5 && subtotal.length == 6)
  {
    value = subtotal.substring(0, 1) + "," + subtotal.substring(1, 3) + "," + subtotal.substring(3, subtotal.length);
    total.innerText = "₹ "+ value
    // 100000 to 1,00,000
  }
  else if(subtotal.length > 5 && subtotal.length == 7)
  {
    value = subtotal.substring(0, 2) + "," + subtotal.substring(2, 4) + "," + subtotal.substring(4, subtotal.length);
    total.innerText = "₹ "+ value
    // 1000000 to 10,00,000
  }
  else{
    total.innerText = "₹ "+ subtotal
    // 100 to 100
  }
  
}

function changeShippingCost()
{
  cost = document.getElementById('shippingcost')
  cost.innerText = '₹ 100';

  subtotal = document.getElementById('subtotal').textContent
  total = document.getElementById('total')
  subtotal = (parseInt(subtotal) + 100).toString()
  if(subtotal.length > 3 && subtotal.length == 4)
  {
    value = subtotal.substring(0, 1) + "," + subtotal.substring(1, subtotal.length);
    total.innerText = "₹ "+ value
    // 1000 to 1,000
  }
  else if(subtotal.length > 3 && subtotal.length == 5)
  {
    value = subtotal.substring(0, 2) + "," + subtotal.substring(2, subtotal.length);
    total.innerText = "₹ "+ value
    // 10000 to 10,000
  }
  else if(subtotal.length > 5 && subtotal.length == 6)
  {
    value = subtotal.substring(0, 1) + "," + subtotal.substring(1, 3) + "," + subtotal.substring(3, subtotal.length);
    total.innerText = "₹ "+ value
    // 100000 to 1,00,000
  }
  else if(subtotal.length > 5 && subtotal.length == 7)
  {
    value = subtotal.substring(0, 2) + "," + subtotal.substring(2, 4) + "," + subtotal.substring(4, subtotal.length);
    total.innerText = "₹ "+ value
    // 1000000 to 10,00,000
  }
  else{
    total.innerText = "₹ "+ subtotal
    // 100 to 100
  }
}