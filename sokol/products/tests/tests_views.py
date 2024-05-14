from django.test import Client, TestCase
from django.urls import reverse
from ..models import Product, Category


class ContextTestsForPagesWithProducts(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим категории 1, 2
        for i in range(1, 3):
            Category.objects.create(
                pk=i,
                title=f'Категория номер {i}',
                slug=f'category{i}',
            )
        # Создадим категории 3, 4 дочерние для 1
        for i in range(3, 5):
            Category.objects.create(
                pk=i,
                title=f'Категория номер {i}',
                slug=f'category{i}',
                parent=Category.objects.get(slug='category1'),
            )
        # Создадим товары 1 до 11
        for i in range(1, 12):
            prod = Product.objects.create(
                pk=i,
                product_name=f'Товар номер {i}',
                price=i,
            )
            prod.category.set(Category.objects.filter(pk=4))
        rec1 = Product.objects.get(pk=1)
        rec1.recommend = True
        rec1.save(update_fields=["recommend"])
        rec2 = Product.objects.get(pk=2)
        rec2.recommend = True
        rec2.save(update_fields=["recommend"])

    def setUp(self):
        self.guest_client = Client()

    def test_index_show_correct_context(self):
        response = self.guest_client.get(reverse('index'))
        # вывод новинок
        pr_dict = dict()
        for i in range(0, 10):
            pr_dict['product%s' % i] = response.context['products'][i].product_name
        pr_num = 11
        for i in range(0, 10):
            self.assertEqual(pr_dict['product%s' % i], f'Товар номер {pr_num}')
            pr_num -= 1
        # вывод рекомендуемого
        recommend1 = response.context['recommended_products'][0].product_name
        recommend2 = response.context['recommended_products'][1].product_name
        self.assertEqual(recommend1, f'Товар номер {2}')
        self.assertEqual(recommend2, f'Товар номер {1}')

    def test_all_products_show_correct_context(self):
        response = self.guest_client.get(reverse('all_products'))
        # вывод новинок
        pr_dict = dict()
        for i in range(0, 10):
            pr_dict['product%s' % i] = response.context['page_obj'][i].product_name
        pr_num = 11
        for i in range(0, 10):
            self.assertEqual(pr_dict['product%s' % i], f'Товар номер {pr_num}')
            pr_num -= 1
        # вывод рекомендуемого
        recommend1 = response.context['recommended_products'][0].product_name
        recommend2 = response.context['recommended_products'][1].product_name
        self.assertEqual(recommend1, f'Товар номер {2}')
        self.assertEqual(recommend2, f'Товар номер {1}')

    def test_all_products_with_keyword_show_correct_context(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('all_products'),
            filter='q', value='11'
        )
        response = self.guest_client.get(url)

        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 11')
        # вывод рекомендуемого
        recommend1 = response.context['recommended_products'][0].product_name
        recommend2 = response.context['recommended_products'][1].product_name
        self.assertEqual(recommend1, f'Товар номер {2}')
        self.assertEqual(recommend2, f'Товар номер {1}')

    def test_categories_show_correct_context(self):
        response = self.guest_client.get(reverse('categories'))
        cat1 = response.context['categories'][0].title
        cat2 = response.context['categories'][1].title
        self.assertEqual(cat1, 'Категория номер 1')
        self.assertEqual(cat2, 'Категория номер 2')

    def test_subcategories_show_correct_context(self):
        response = self.guest_client.get(reverse('subcategories', kwargs={'slug': 'category1'}))
        subcat1 = response.context['subcategories'][0].title
        subcat2 = response.context['subcategories'][1].title
        self.assertEqual(subcat1, 'Категория номер 3')
        self.assertEqual(subcat2, 'Категория номер 4')

    def test_category_products_show_correct_context(self):
        response = self.guest_client.get(reverse('category_products', kwargs={'slug': 'category4'}))
        pr_dict = dict()
        for i in range(0, 11):
            pr_dict['product%s' % i] = response.context['page_obj'][i].product_name
        pr_num = 11
        for i in range(0, 11):
            self.assertEqual(pr_dict['product%s' % i], f'Товар номер {pr_num}')
            pr_num -= 1
        # вывод рекомендуемого
        recommend1 = response.context['recommended_products'][0].product_name
        recommend2 = response.context['recommended_products'][1].product_name
        self.assertEqual(recommend1, f'Товар номер {2}')
        self.assertEqual(recommend2, f'Товар номер {1}')

    def test_product_detail_show_correct_context(self):
        response = self.guest_client.get(reverse('product_detail', kwargs={'product_id': 1}))
        product_name = response.context['product'].product_name
        product_price = response.context['product'].price
        self.assertEqual(product_name, 'Товар номер 1')
        self.assertEqual(product_price, 1)
        # вывод рекомендуемого
        recommend1 = response.context['recommended_products'][0].product_name
        recommend2 = response.context['recommended_products'][1].product_name
        self.assertEqual(recommend1, f'Товар номер {2}')
        self.assertEqual(recommend2, f'Товар номер {1}')


class ProductFiltersInCategoryProductsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Category.objects.create(
            pk=1,
            title='Категория номер 1',
            slug='category1',
        )
        # Создадим товары 1 до 12
        for i in range(1, 13):
            prod = Product.objects.create(
                pk=i,
                product_name=f'Товар номер {i}',
                price=i,
            )
            prod.category.set(Category.objects.filter(pk=1))

        Product.objects.filter(pk=1).update(product_type="тип 1")
        Product.objects.filter(pk=2).update(compatibility="Ak-47")
        Product.objects.filter(pk=3).update(thread_type="4x4")
        Product.objects.filter(pk=4).update(mounting_type="на скотч")
        Product.objects.filter(pk=5).update(imitation_of_a_shot=True)
        Product.objects.filter(pk=6).update(laser_sight=True)
        Product.objects.filter(pk=7).update(weight=4.4)
        Product.objects.filter(pk=8).update(principle_of_operation="c Бoжьeй пoмoщью")
        Product.objects.filter(pk=9).update(length=4)
        Product.objects.filter(pk=10).update(diameter=7.7)
        Product.objects.filter(pk=11).update(girbox='Abc123')
        Product.objects.filter(pk=12).update(available=False)

    def setUp(self):
        self.guest_client = Client()

    def test_price_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='max_price', value='11'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 11')

    def test_available_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='available', value='True'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 11')

    def test_product_type_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='product_type', value='тип 1'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 1')

    def test_compatibility_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='compatibility', value='Ak-47'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 2')

    def test_thread_type_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='thread_type', value='4x4'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 3')

    def test_mounting_type_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='mounting_type', value='на скотч'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 4')

    def test_imitation_of_a_shot_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='imitation_of_a_shot', value='True'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 5')

    def test_laser_sight_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='laser_sight', value='True'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 6')

    def test_weight_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='weight', value='4.4'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 7')

    def test_principle_of_operation_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='principle_of_operation', value='c Бoжьeй пoмoщью'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 8')

    def test_length_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='min_length', value='4'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 9')

    def test_diameter_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='diameter', value='7.7'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 10')

    def test_girbox_filter(self):
        url = '{url}?{filter}={value}'.format(
            url=reverse('category_products', kwargs={'slug': 'category1'}),
            filter='girbox', value='Abc123'
        )
        response = self.guest_client.get(url)
        product = response.context['page_obj'][0].product_name
        self.assertEqual(product, 'Товар номер 11')
