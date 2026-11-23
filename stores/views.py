from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import SellerProfile
from stores.forms import ProductForm, StoreForm
from .models import *
from django.contrib import messages

# Create your views here.
@login_required
def seller_panel_view(request):
    seller_profile,_ = SellerProfile.objects.get_or_create(
        user=request.user
    )
    # When a ForeignKey is set up so that one Seller can have multiple stores, 
    # you can retrieve all the stores for a given seller using Seller.store_set.all()
    stores = seller_profile.store_set.all()

    return render(request, 'seller_panel.html', {
        'seller_profile': seller_profile,
        'stores': stores
    })


@login_required
def create_store_view(request):
    if request.method == 'POST':
        form = StoreForm(request.POST) 
        if form.is_valid():
            name= form.cleaned_data['name']
            description= form.cleaned_data['description']
            owner = SellerProfile.objects.get(user=request.user)
            Store.objects.create(name=name,description=description,owner=owner)
            messages.success(request, f'store {name} has created successfully')
            return redirect('seller_panel')
        else:
            messages.error(request, 'fill the fields correctly.')
    else:
        # create an empty form 
        form= StoreForm()         
    return render(request, 'create_store.html', {'form':form})

@login_required
def create_Product_view(request,store_id):
    if request.method == 'POST':
        # send request.FILES in addition to request.POST
        form = ProductForm(request.POST,request.FILES) 
        if form.is_valid():
            name= form.cleaned_data['name']
            description= form.cleaned_data['description']
            price= form.cleaned_data['price']
            image= form.cleaned_data['image']
            seller_profile = SellerProfile.objects.get(user=request.user)
            store = Store.objects.get(
            id=store_id,
            owner=seller_profile
            )

            Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                store=store)
            messages.success(request, f'product {name} has created successfully')
            return redirect('store_detail', store_id=store.id)
        else:
            messages.error(request, 'fill the fields correctly.')
    else:
        # create an empty form 
        form= ProductForm()         
    return render(request, 'create_product.html', {'form':form})

@login_required
def store_detail_view(request,store_id):       
    store = Store.objects.get(id=store_id)
#     This means that each product is connected to one store.

# The stoer ForeignKey is stored in the Product table, not in the Store table.

# But what if we want to get all products of a specific store?

# Django automatically creates a reverse relationship for us.

# We can access all products of a store using:

# store.product_set.all()
    products = store.product_set.all()
    return render(request, 'store_detail.html', {
        'store': store,
        'products': products
    })
