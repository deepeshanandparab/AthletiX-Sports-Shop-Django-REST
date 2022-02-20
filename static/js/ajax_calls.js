function addToWishlist(id) {
    let csrf = $("input[name=csrfmiddlewaretoken").val();
    wishlist_data = {id:id, csrfmiddlewaretoken: csrf}

    $.ajax({
        url: "{% url 'addtowishlistajax' %}",
        method: "POST",
        data: wishlist_data,
        success: function (data){
            console.log(data);
        },
    });
  }