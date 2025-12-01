
from .models import Cart, CartItem, Product
from django.shortcuts import get_object_or_404

SESSION_CART_KEY = 'cart'  
def get_session_cart(request):
    return request.session.get(SESSION_CART_KEY, {})

def save_session_cart(request, cart_dict):
    request.session[SESSION_CART_KEY] = cart_dict
    request.session.modified = True

def add_to_session_cart(request, product_id, qty=1):
    cart = get_session_cart(request)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + qty
    if cart[key] <= 0:
        cart.pop(key)
    save_session_cart(request, cart)
    return cart

def remove_from_session_cart(request, product_id):
    cart = get_session_cart(request)
    cart.pop(str(product_id), None)
    save_session_cart(request, cart)

def clear_session_cart(request):
    if SESSION_CART_KEY in request.session:
        del request.session[SESSION_CART_KEY]
        request.session.modified = True

def sync_session_to_db(request):
    """
    Перенести session cart у Cart для авторизованого користувача при логіні.
    """
    if not request.user.is_authenticated:
        return
    session_cart = get_session_cart(request)
    if not session_cart:
        return
    cart, _ = Cart.objects.get_or_create(user=request.user)
    for pid, qty in session_cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            item.quantity = qty
        else:
            item.quantity = item.quantity + qty
        item.save()
    clear_session_cart(request)
