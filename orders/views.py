from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomerProfile
from stores.models import Product
from .models import Cart, CartItem
from django.shortcuts import render


@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    customer, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')


@login_required
def cart_view(request):
    customer, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    cart = Cart.objects.filter(customer=customer).first()

    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.product.price * cart_item.quantity
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price':total_price
    })

@login_required
def remove_from_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )
    cart = get_object_or_404(
        Cart,
        customer=customer
    )
    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product=product
    )
    cart_item.delete()

    return redirect('cart')
    
