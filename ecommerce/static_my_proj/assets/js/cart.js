var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('action:', action,'article:', productId)
        console.log('Client', user)

        if (user === "AnonymousUser") {
            console.log("Vous n'etes pas connecté")
        } else {
            console.log("Envoi des données")
            updateUserOrder(productId, action)
        }

    })
    
}


function updateUserOrder(productId, action) {

    
    var url = '/cart/update/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body: JSON.stringify({"productId": productId, "action": action})
    })


    .then((response) =>{
        return response.json()
    })

    .then( (data) =>{
        // location.reload();
        // window.location.reload();
        console.log(data)
    })
    .then(response => console.log(JSON.stringify(response)))
}

function getOwnedProduct(productId){
    var actionEndpoint = '/accounts/verify/ownership/'
    var httpMethod = 'GET'
    var data = {
        product_id:productId
    }

    $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data:data,
        success: function(data){
            if(data.owner){
                return true
            }else{
                return false
            }
        },
        error: function(error){
            console.log(error)
        }
    })


}



$(document).ready(function(){
    
    var productForm = $(".form-product-ajax")

    $.each(productForm, function(index, object){
        var $this = $(this)
        var isUser = $this.attr('data-user')
        var submitSpan = $this.find(".submit-span")
        var productInput = $this.find("[name='product_id']")
        var productId = $this.find("value")
        var productIsDigital = productInput.attr("data-is-digital")


        if (productIsDigital && isUser) {

            var isOwned = getOwnedProduct(productId);

            if (isOwned) {
                
                submitSpan.html('<a href="/library/">Dans la bibliothèque</a>')
                
            }
        
        }

        console.log(submitSpan.html())

    })
















    productForm.submit(function(event){
        event.preventDefault();
        console.log("formulaire non envoyé")

        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("data-endpoint");
        
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                console.log("succès !!!")
                console.log(data)
                var submitSpan = thisForm.find(".submit-span")

                console.log(submitSpan.html())
                if (data.added) {
                    submitSpan.html('<button type="submit" class="btn btn-block  btn-lg btn-black-default-hover">Retirer</button>')
                } else {
                    submitSpan.html('<button type="submit"  class="btn btn-block  btn-lg btn-black-default-hover" >Ajouter</button>')
                }

                var navbarCartCount = $(".navbar-cart-count")
                navbarCartCount.text(data.cartItemCount)

                var currentPath = window.location.href

                if(currentPath.indexOf("cart") != -1){
                    refreshCart()
                }
            },




            error: function(errorData){
                console.log(errorData)
            }
        })

    })

    function refreshCart(){

        var carTable = $(".cart-section")
        var carBody = carTable.find(".cart-body")
        var cartsubtotal = $(".cart_subtotal")
        var productsRow = carBody.find(".cart-product")
        var currentUrl = window.location.href

        //cart_amount


        var refreshCartUrl = "api/cart/"
        var refreshCartMethod = "GET";
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data:data,
            success:function(data){
                console.log("operation effectuée avec succès !!!")
                console.log(data)
                if (data.products.length > 0) {
                   
                    cartsubtotal.find(".cart_amount").text(data.total)
                } else {
                    window.location.href = currentUrl
                }
            },
            error:function(errorData) {
                console.log("erreur")
                console.log(errorData)
            }
            
        })
    }

})




$(document).ready(function(){
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval = 1500  // 500 = .5 seconds
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){

        console.log(searchInput.val())

        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)

    })

    searchInput.keydown(function(event){
        clearTimeout(typingTimer)

    })




    function performSearch() {
        searchBtn.addClass("disabled")
        searchBtn.html("En cours...")
        var query = searchInput.val()
        window.location.href ="/search/?q="+query
    }
})