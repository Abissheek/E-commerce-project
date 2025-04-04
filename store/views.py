from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from cart.models import CartItem
from cart.views import _cart_id
from .models import Product
from Ecommerce.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None   
    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator=Paginator(products,1)
        page = request.GET.get('page','1') 
        paged_product=paginator.get_page(page)
        product_count=products.count()
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,3)
        page = request.GET.get('page','1') 
        paged_product=paginator.get_page(page)
        product_count=products.count()
    context={
        'products':paged_product,
        'product_count':product_count,
           

    }
    
    return render(request, 'store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        return HttpResponse(in_cart)
    context={
        'single_product':single_product,
        'in_cart':in_cart,
    }

    return render(request, 'productdetail.html',context)



def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('create_date').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            product_count=products.count()

    context={
        'products':products,
        'product_count':product_count
    }

    return render(request, 'store.html',context )



