if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
    var delButtons = document.getElementsByClassName('btn-danger')
    for (var i = 0; i < delButtons.length; i++) {
        var button = delButtons[i]
        button.addEventListener('click', delItem)
    }

    var numinputs = document.getElementsByClassName('cart-quantity-input')
    for (var i = 0; i < numinputs.length; i++) {
        var input = numinputs[i]
        input.addEventListener('change', modifyNum)
    }

    var addButton = document.getElementsByClassName('shop-item-button')
    for (var i = 0; i < addButton.length; i++) {
        var button = addButton[i]
        button.addEventListener('click', addActionCart)
    }

    document.getElementsByClassName('btn-purchase')[0].addEventListener('click', buyCLick)
}

function buyCLick() {
    alert('Thanks for purchase')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    while (cartItems.hasChildNodes()) {
        cartItems.removeChild(cartItems.firstChild)
    }

    var cartCount = document.getElementById('cart-count')
    cartCount.innerText = 0

    updateCartTotal()
}

function delItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()

    var cartCount = document.getElementById('cart-count')
    cartCount.innerText = parseInt(cartCount.innerText) - 1

    updateCartTotal()
}

function modifyNum(event) {
    var input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateCartTotal()
}

function addActionCart(event) {
    var button = event.target
    var shopItem = button.parentElement.parentElement
    var title = shopItem.getElementsByClassName('shop-item-title')[0].innerText
    var price = shopItem.getElementsByClassName('shop-item-price')[0].innerText
    var imageSrc = shopItem.getElementsByClassName('shop-item-image')[0].src
    addCartI(title, price, imageSrc)
    updateCartTotal()
}

function addCartI(title, price, imageSrc) {
    var cartRow = document.createElement('div')
    cartRow.classList.add('cart-row')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    var cartItemNames = cartItems.getElementsByClassName('cart-item-title')
    for (var i = 0; i < cartItemNames.length; i++) {
        if (cartItemNames[i].innerText == title) {
            alert('This item is already added to the cart')
            return
        }
    }

    var cartCount = document.getElementById('cart-count')
    cartCount.innerText = parseInt(cartCount.innerText) + 1

    var cartRowContents = `
        <div class="cart-item cart-column">
            <img class="cart-item-image" src="${imageSrc}" width="100" height="100">
            <span class="cart-item-title">${title}</span>
        </div>
        <span class="cart-price cart-column">${price}</span>
        <div class="cart-quantity cart-column">
            <input class="cart-quantity-input" type="number" value="1">
            <button class="btn btn-danger" type="button">REMOVE</button>
        </div>`
    cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', delItem)
    cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', modifyNum)
}

function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('$', ''))
        var quantity = quantityElement.value
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total
}