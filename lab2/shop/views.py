from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST
from django.contrib import messages
from .cart import (
    add_to_session_cart, remove_from_session_cart, get_session_cart,
    save_session_cart, clear_session_cart, sync_session_to_db
)
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required


def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def shop_index(request):
    products = Product.objects.all()[:5]
    return render(request, 'shop/product_list.html', {'products': products})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'shop/product_list.html', {'products': products})

# Пагінація списків
def paginated_product_list(request):
    products = Product.objects.select_related('category').all()
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/product_list.html', {'page_obj': page_obj})

def paginated_category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/category_list.html', {'page_obj': page_obj})

# Detail (Read)
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'shop/category_detail.html', {'category': category})

# Create
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'shop/category_form.html', {'form': form})

# Update
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'shop/category_form.html', {'form': form})

# Delete
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'object': product})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'shop/category_confirm_delete.html', {'object': category})


# Додати товар у корзину (POST)
@require_POST
def add_to_cart(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        item.quantity = item.quantity + qty if not created else qty
        item.save()
    else:
        add_to_session_cart(request, product_id, qty)
    messages.success(request, "Товар додано до корзини")
    return redirect('cart_detail')

# Оновити кількість позиції (POST)
@require_POST
def cart_update_item(request, product_id):
    qty = int(request.POST.get('quantity', 0))
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            try:
                item = CartItem.objects.get(cart=cart, product_id=product_id)
                if qty > 0:
                    item.quantity = qty
                    item.save()
                else:
                    item.delete()
            except CartItem.DoesNotExist:
                if qty > 0:
                    CartItem.objects.create(cart=cart, product_id=product_id, quantity=qty)
    else:
        if qty > 0:
            add_to_session_cart(request, product_id, qty=0)  
            request.session['cart'][str(product_id)] = qty
            save_session_cart(request, request.session['cart'])
        else:
            remove_from_session_cart(request, product_id)
    messages.success(request, "Кількість оновлено")
    return redirect('cart_detail')

# Видалити позицію
@require_POST
def cart_remove(request, product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    else:
        remove_from_session_cart(request, product_id)
    messages.success(request, "Товар видалено з корзини")
    return redirect('cart_detail')

# Очистити корзину
@require_POST
def cart_clear(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
    else:
        clear_session_cart(request)
    messages.success(request, "Корзина очищена")
    return redirect('cart_detail')

# Показати корзину
def cart_detail(request):
    # якщо користувач зареєстрований — синхронізуємо сесію
    if request.user.is_authenticated:
        sync_session_to_db(request)
        cart = Cart.objects.filter(user=request.user).first()
        items = cart.items.select_related('product').all() if cart else []
    else:
        s = get_session_cart(request)
        product_ids = [int(pid) for pid in s.keys()]
        products = Product.objects.filter(pk__in=product_ids)
        prod_map = {p.pk: p for p in products}
        # збираємо тимчасні об’єкти для шаблона
        items = []
        for pid, qty in s.items():
            p = prod_map.get(int(pid))
            if p:
                class Item: pass
                it = Item()
                it.product = p
                it.quantity = qty
                items.append(it)
    total = sum(it.product.price * it.quantity for it in items)
    return render(request, 'shop/cart_detail.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()
    messages.success(request, "Замовлення створено (тестовый режим).")
    return redirect('shop_index')