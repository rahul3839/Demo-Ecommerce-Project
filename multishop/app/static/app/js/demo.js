                <div class="my-3">
                <label for="quantity">Quantity:</label>
                <a class="minus-cart btn" pid="{{cart.product.id}}"><i class="fas fa-minus-square fa-lg"></i></a>
                <span id="quantity">{{cart.quantity}}</span>
                <a class="plus-cart btn" pid="{{cart.product.id}}"><i class="fas fa-plus-square fa-lg"></i></a>
              </div>




$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString(); 
    var eml = this.parentNode.children[2]
    console.log(id)

 
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data: {
            prod_id : id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText =   data.amount
            document.getElementById("totalamount").innerText = data.totalamount

        }

    })
})

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString(); 
    var eml = this.parentNode.children[2]
    console.log(id)

 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data: {
            prod_id : id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText =   data.amount
            document.getElementById("totalamount").innerText = data.totalamount

        }

    })
})

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString(); 
    var eml = this
    console.log(id)

 
    $.ajax({
        type:"GET",
        url:"/removecart",
        data: {
            prod_id : id
        },
        success: function (data) {
            console.log("   ")
            document.getElementById("amount").innerText =   data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove() 

        }

    })
})