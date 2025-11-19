# shop/context_processors.py
from .models import Cart

def cart_counter(request):
    count = 0
    if request.user.is_authenticated:
        cart = getattr(request.user, 'cart', None)
        if cart:
            count = cart.total_items()
    else:
        c = request.session.get('cart', {})
        count = sum(c.values()) if c else 0
    return {'cart_count': count}
