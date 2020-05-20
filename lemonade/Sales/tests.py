from django.test import TestCase
from .models import *
from .views import *
import datetime
# Create your tests here.


class ModelTests(TestCase):
    def setUp(self):
        Lemonade.objects.create(name='regular', price='5')
        Lemonade.objects.create(name='new', price='6')
        Staff.objects.create(name='man', position="position", commission_percentage=10)
        Staff.objects.create(name='man2', position="position2", commission_percentage=50)
        LemonadeSet.objects.create(lemonade=Lemonade.objects.get(id=1), quantity=2)
        LemonadeSet.objects.create(lemonade=Lemonade.objects.get(id=2), quantity=3)
        order = Order.objects.create()
        order.set.set(LemonadeSet.objects.all())
        Sale.objects.create(order=Order.objects.get(id=1),
                            date=datetime.datetime(2020,1,1, 0),
                            sales_person=Staff.objects.get(id=1))

    def test_staff_name_label(self):
        staff = Staff.objects.get(id=1)
        name = staff._meta.get_field('commission_percentage').verbose_name
        self.assertEquals(name, 'commission percentage')

    def test_str_lemonade(self):
        lemonade = Lemonade.objects.get(id=1)
        self.assertEquals('regular @ $5.0/cup', str(lemonade))


class FormTests(TestCase):
    def setUp(self):
        Lemonade.objects.create(name='regular', price='5')

    def test_ReportForm(self):
        form = ReportForm()
        self.assertEquals(form.fields['name'].label, 'Employee Name')

    def test_lemonade_minimum(self):
        form = LemonadeEntryForm(data={'Lemonade': 1, 'quantity': -1})
        self.assertFalse(form.is_valid())


class ViewTests(TestCase):
    def test_form_url_template(self):
        response = self.client.get(reverse('form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_index_url_exists(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_url_date_conversion(self):
        date = datetime.datetime(2020, 2, 1, 0)
        self.assertEqual(url_to_date(date_to_url(date)), date)







