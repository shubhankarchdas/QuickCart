from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from QuickCart.service import get_available_products, get_products_by_category
from category.service import get_category_by_slug, get_product_by_category_and_slug, search_products
from orders.models import OrderProduct
from store.models import ProductGallery, ReviewRating
from store.service import create_review, get_existing_review, is_product_in_cart, update_review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def store(request, category_slug=None):
    if category_slug:
        category = get_category_by_slug(category_slug)
        products = get_products_by_category(category)
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        paged_product = paginator.get_page(page_number)
        product_count = products.count()
    else:
        products = get_available_products()
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        paged_product = paginator.get_page(page_number)
        product_count = products.count()

    context = {
        'products': paged_product,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = get_product_by_category_and_slug(category_slug, product_slug)
        in_cart = is_product_in_cart(request, single_product) 
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None


    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'category': single_product.category,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }

    return render(request, 'store/product_detail.html', context)



def search(request):
    keyword = request.GET.get('keyword', '')
    products = search_products(keyword)
    context = {
        'products': products,
        'product_count': products.count(),
    }

    return render(request, 'store/store.html', context)




def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        user_id = request.user.id
        ip = request.META.get('REMOTE_ADDR')
        form_data = request.POST
        
        existing_review = get_existing_review(user_id, product_id)
        
        if existing_review:
            success = update_review(existing_review, form_data)
            if success:
                messages.success(request, 'Thank you! Your review has been updated.')
            else:
                messages.error(request, 'There was an error updating your review.')
        else:
            success = create_review(form_data, user_id, product_id, ip)
            if success:
                messages.success(request, 'Thank you! Your review has been submitted.')
            else:
                messages.error(request, 'There was an error submitting your review.')
        
        return redirect(url)