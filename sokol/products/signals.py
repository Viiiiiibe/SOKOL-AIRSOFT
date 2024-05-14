from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category
from django.core.cache import cache
from django.db.models import Max, Min


@receiver(post_save, sender=Product)
def rebuild_product_cache_after_save(instance, **kwargs):
    cache.set("10_new_products_cache", Product.objects.all().order_by('-pub_date')[:10], None)
    cache.set("all_products_cache", Product.objects.all().order_by('-pub_date'), None)
    cache.set("recommended_products_cache", Product.objects.all().filter(recommend=True).order_by('-pub_date'), None)
    if instance.category is not None:
        for cat in instance.category.all():
            cache.set(f"price_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).aggregate(Max('price'), Min('price')), 10 * 60)
            cache.set(f"product_type_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('product_type').distinct().exclude(
                          product_type=''), 10 * 60)
            cache.set(f"compatibility_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('compatibility').distinct().exclude(
                          compatibility=''), 10 * 60)
            cache.set(f"thread_type_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('thread_type').distinct().exclude(
                          thread_type=''), 10 * 60)
            cache.set(f"mounting_type_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('mounting_type').distinct().exclude(
                          mounting_type=''), 10 * 60)
            cache.set(f"imitation_of_a_shot_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('imitation_of_a_shot').distinct().exclude(
                          imitation_of_a_shot=''), 10 * 60)
            cache.set(f"laser_sight_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('laser_sight').distinct().exclude(
                          laser_sight=''), 10 * 60)
            cache.set(f"weight_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('weight').distinct().exclude(weight=None),
                      10 * 60)
            cache.set(f"principle_of_operation_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values(
                          'principle_of_operation').distinct().exclude(principle_of_operation=''), 10 * 60)
            cache.set(f"length_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).aggregate(Max('length'), Min('length')), 10 * 60)
            cache.set(f"diameter_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('diameter').distinct().exclude(
                          diameter=None), 10 * 60)
            cache.set(f"girbox_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('girbox').distinct().exclude(girbox=''),
                      10 * 60)


@receiver(post_delete, sender=Product)
def rebuild_product_cache_after_delete(instance, **kwargs):
    cache.set("10_new_products_cache", Product.objects.all().order_by('-pub_date')[:10], None)
    cache.set("all_products_cache", Product.objects.all().order_by('-pub_date'), None)
    cache.set("recommended_products_cache", Product.objects.all().filter(recommend=True).order_by('-pub_date'), None)
    if instance.category is not None:
        for cat in instance.category.all():
            cache.set(f"price_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).aggregate(Max('price'), Min('price')), 10 * 60)
            cache.set(f"product_type_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('product_type').distinct().exclude(
                          product_type=''), 10 * 60)
            cache.set(f"compatibility_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('compatibility').distinct().exclude(
                          compatibility=''), 10 * 60)
            cache.set(f"thread_type_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('thread_type').distinct().exclude(
                          thread_type=''), 10 * 60)
            cache.set(f"mounting_type_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('mounting_type').distinct().exclude(
                          mounting_type=''), 10 * 60)
            cache.set(f"imitation_of_a_shot_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('imitation_of_a_shot').distinct().exclude(
                          imitation_of_a_shot=''), 10 * 60)
            cache.set(f"laser_sight_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('laser_sight').distinct().exclude(
                          laser_sight=''), 10 * 60)
            cache.set(f"weight_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('weight').distinct().exclude(weight=None),
                      10 * 60)
            cache.set(f"principle_of_operation_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values(
                          'principle_of_operation').distinct().exclude(principle_of_operation=''), 10 * 60)
            cache.set(f"length_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).aggregate(Max('length'), Min('length')), 10 * 60)
            cache.set(f"diameter_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('diameter').distinct().exclude(
                          diameter=None), 10 * 60)
            cache.set(f"girbox_data_for_filters_in_{cat.slug}_cache",
                      Product.objects.all().filter(category=cat).values('girbox').distinct().exclude(girbox=''),
                      10 * 60)


@receiver(post_save, sender=Category)
def rebuild_category_cache_after_save(instance, **kwargs):
    cache.set("categories_without_parents_cache", Category.objects.all().filter(parent=None).order_by('title'), None)
    if instance.parent is not None:
        cache.set(f"{instance.parent.slug}_subcategories_cache",
                  Category.objects.all().filter(parent=Category.objects.get(slug=instance.parent.slug)), None)
    cache.set("category_cache", Category.objects.all(), None)


@receiver(post_delete, sender=Category)
def rebuild_category_cache_after_delete(instance, **kwargs):
    cache.set("categories_without_parents_cache", Category.objects.all().filter(parent=None).order_by('title'), None)
    if instance.parent is not None:
        cache.set(f"{instance.parent.slug}_subcategories_cache",
                  Category.objects.all().filter(parent=Category.objects.get(slug=instance.parent.slug)), None)
    cache.set("category_cache", Category.objects.all(), None)
