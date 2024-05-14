from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Max, Min
from cart.cart import Cart
from django.core.cache import cache


def index(request):
    products = cache.get_or_set("10_new_products_cache", Product.objects.all().order_by('-pub_date')[:10], None)
    context = {
        'products': products,
    }
    return render(request, 'products/index.html', context)


def all_products(request):
    keyword = request.GET.get("q", None)
    if keyword:
        products = Product.objects.all().filter(product_name__icontains=keyword).order_by('-pub_date')
    else:
        products = cache.get_or_set("all_products_cache", Product.objects.all().order_by('-pub_date'), None)
    # Показывать по 24 записи на странице по умолчанию.
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "keyword": keyword
    }
    return render(request, 'products/all_products.html', context)


def categories(request):
    cat = cache.get_or_set("categories_without_parents_cache",
                           Category.objects.all().filter(parent=None).order_by('title'), None)
    context = {
        'categories': cat,
    }
    return render(request, 'products/categories.html', context)


def subcategories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcat = cache.get_or_set(f"{slug}_subcategories_cache", Category.objects.all().filter(parent=category), None)
    context = {
        'subcategories': subcat,
        'category': category
    }
    return render(request, 'products/subcategories.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # данные для отображенивя в фильтрах
    price_data_for_filters = cache.get_or_set(f"price_data_for_filters_in_{slug}_cache",
                                              Product.objects.all().filter(category=category).aggregate(Max('price'),
                                                                                                        Min('price')),
                                              10 * 60)
    product_type_data_for_filters = cache.get_or_set(f"product_type_data_for_filters_in_{slug}_cache",
                                                     Product.objects.all().filter(category=category).values(
                                                         'product_type').distinct().exclude(product_type=''), 10 * 60)
    compatibility_data_for_filters = cache.get_or_set(f"compatibility_data_for_filters_in_{slug}_cache",
                                                      Product.objects.all().filter(category=category).values(
                                                          'compatibility').distinct().exclude(compatibility=''),
                                                      10 * 60)
    thread_type_data_for_filters = cache.get_or_set(f"thread_type_data_for_filters_in_{slug}_cache",
                                                    Product.objects.all().filter(category=category).values(
                                                        'thread_type').distinct().exclude(thread_type=''), 10 * 60)
    mounting_type_data_for_filters = cache.get_or_set(f"mounting_type_data_for_filters_in_{slug}_cache",
                                                      Product.objects.all().filter(category=category).values(
                                                          'mounting_type').distinct().exclude(mounting_type=''),
                                                      10 * 60)
    imitation_of_a_shot_data_for_filters = cache.get_or_set(f"imitation_of_a_shot_data_for_filters_in_{slug}_cache",
                                                            Product.objects.all().filter(category=category).values(
                                                                'imitation_of_a_shot').distinct().exclude(
                                                                imitation_of_a_shot=''), 10 * 60)
    laser_sight_data_for_filters = cache.get_or_set(f"laser_sight_data_for_filters_in_{slug}_cache",
                                                    Product.objects.all().filter(category=category).values(
                                                        'laser_sight').distinct().exclude(laser_sight=''), 10 * 60)
    weight_data_for_filters = cache.get_or_set(f"weight_data_for_filters_in_{slug}_cache",
                                               Product.objects.all().filter(category=category).values(
                                                   'weight').distinct().exclude(weight=None), 10 * 60)
    principle_of_operation_data_for_filters = cache.get_or_set(
        f"principle_of_operation_data_for_filters_in_{slug}_cache",
        Product.objects.all().filter(category=category).values('principle_of_operation').distinct().exclude(
            principle_of_operation=''), 10 * 60)
    length_data_for_filters = cache.get_or_set(f"length_data_for_filters_in_{slug}_cache",
                                               Product.objects.all().filter(category=category).aggregate(Max('length'),
                                                                                                         Min('length')),
                                               10 * 60)
    diameter_data_for_filters = cache.get_or_set(f"diameter_data_for_filters_in_{slug}_cache",
                                                 Product.objects.all().filter(category=category).values(
                                                     'diameter').distinct().exclude(diameter=None), 10 * 60)
    girbox_data_for_filters = cache.get_or_set(f"girbox_data_for_filters_in_{slug}_cache",
                                               Product.objects.all().filter(category=category).values(
                                                   'girbox').distinct().exclude(girbox=''), 10 * 60)

    # фильтры
    queryset = Q()
    queryset.add(Q(category=category), Q.AND)
    min_price_get = request.GET.get("min_price", '')
    max_price_get = request.GET.get("max_price", '')
    if (min_price_get != '') or (max_price_get != ''):
        if min_price_get == '':
            min_price_get = price_data_for_filters['price__min']
        if max_price_get == '':
            max_price_get = price_data_for_filters['price__max']
        queryset.add(Q(price__range=(min_price_get, max_price_get)), Q.AND)
    available_get = request.GET.get("available", None)
    if available_get is not None:
        queryset.add(Q(available=available_get), Q.AND)
    product_type_get = request.GET.getlist("product_type")
    if product_type_get:
        queryset.add(Q(product_type__in=product_type_get), Q.AND)
    compatibility_get = request.GET.getlist("compatibility")
    if compatibility_get:
        queryset.add(Q(compatibility__in=compatibility_get), Q.AND)
    thread_type_get = request.GET.getlist("thread_type")
    if thread_type_get:
        queryset.add(Q(thread_type__in=thread_type_get), Q.AND)
    mounting_type_get = request.GET.getlist("mounting_type")
    if mounting_type_get:
        queryset.add(Q(mounting_type__in=mounting_type_get), Q.AND)
    imitation_of_a_shot_get = request.GET.getlist("imitation_of_a_shot")
    if imitation_of_a_shot_get:
        queryset.add(Q(imitation_of_a_shot__in=imitation_of_a_shot_get), Q.AND)
    laser_sight_get = request.GET.getlist("laser_sight")
    if laser_sight_get:
        queryset.add(Q(laser_sight__in=laser_sight_get), Q.AND)
    weight_get = request.GET.getlist("weight")
    if weight_get:
        queryset.add(Q(weight__in=weight_get), Q.AND)
    principle_of_operation_get = request.GET.getlist("principle_of_operation")
    if principle_of_operation_get:
        queryset.add(Q(principle_of_operation__in=principle_of_operation_get), Q.AND)
    min_length_get = request.GET.get("min_length", '')
    max_length_get = request.GET.get("max_length", '')
    if (min_length_get != '') or (max_length_get != ''):
        if min_length_get == '':
            min_length_get = length_data_for_filters['length__min']
        if max_price_get == '':
            max_price_get = length_data_for_filters['length__max']
        queryset.add(Q(length__range=(min_length_get, max_price_get)), Q.AND)
    diameter_get = request.GET.getlist("diameter")
    if diameter_get:
        queryset.add(Q(diameter__in=diameter_get), Q.AND)
    girbox_get = request.GET.getlist("girbox")
    if girbox_get:
        queryset.add(Q(girbox__in=girbox_get), Q.AND)

    sort_parameter = request.GET.get("sort_by", '-pub_date')
    products = Product.objects.all().filter(queryset).order_by(sort_parameter)

    # Показывать по .. записей на странице.
    prod_count = request.GET.get("prod_count", '24')
    paginator = Paginator(products, prod_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
        'prod_count': prod_count,
        'sort_parameter': sort_parameter,

        'price_data_for_filters': price_data_for_filters,
        'product_type_data_for_filters': product_type_data_for_filters,
        'compatibility_data_for_filters': compatibility_data_for_filters,
        'thread_type_data_for_filters': thread_type_data_for_filters,
        'mounting_type_data_for_filters': mounting_type_data_for_filters,
        'imitation_of_a_shot_data_for_filters': imitation_of_a_shot_data_for_filters,
        'laser_sight_data_for_filters': laser_sight_data_for_filters,
        'weight_data_for_filters': weight_data_for_filters,
        'principle_of_operation_data_for_filters': principle_of_operation_data_for_filters,
        'length_data_for_filters': length_data_for_filters,
        'diameter_data_for_filters': diameter_data_for_filters,
        'girbox_data_for_filters': girbox_data_for_filters,

        'product_type_get': product_type_get,
        'compatibility_get': compatibility_get,
        'thread_type_get': thread_type_get,
        'mounting_type_get': mounting_type_get,
        'imitation_of_a_shot_get': imitation_of_a_shot_get,
        'laser_sight_get': laser_sight_get,
        'weight_get': weight_get,
        'principle_of_operation_get': principle_of_operation_get,
        'diameter_get': diameter_get,
        'girbox_get': girbox_get,
    }
    return render(request, 'products/category_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    if str(product_id) in cart.cart:
        in_cart = True
    else:
        in_cart = False
    context = {
        'product': product,
        'in_cart': in_cart
    }
    return render(request, 'products/product_detail.html', context)
