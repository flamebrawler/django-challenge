from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import datetime

from .models import *
from .forms import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


# initializes session
def get_session(request):
    if 'id' not in request.session or not request.session['id']:
        order = Order()
        order.save()
        request.session['id'] = order.id

    return request.session['id']


# converts date-time object into url compatible string
def date_to_url(date):
    info = date.tzinfo
    if info is None:
        info = 'UTC'
    return '{}+{}+{}'.format(
        date.date(),
        date.time(),
        info)


# converts url compatible date into date-time object
def url_to_date(url):
    return datetime.datetime.strptime(url, '%Y-%m-%d+%H:%M:%S+%Z')


def form(request):
    # expire in 10 minutes
    request.session.set_expiry(600)
    # initialize order in session
    id = get_session(request)

    if 'error_message' not in request.session:
        request.session['error_message'] = ""

    if request.method == 'POST' and 'clear' in request.POST:
        order = Order.objects.get(id=id)
        order.set.all().delete()
        HttpResponseRedirect('')

    # handle posts from lemonade form
    if request.method == 'POST' and ('add' in request.POST or 'remove' in request.POST):
        lemonade_form = LemonadeEntryForm(request.POST)

        if lemonade_form.is_valid():
            id = lemonade_form.cleaned_data['Lemonade']
            quantity = lemonade_form.cleaned_data['quantity']

            if 'add' in request.POST:
                return add_item(request, id, quantity)
            elif 'remove' in request.POST:
                return remove_item(request, id, quantity)
    else:
        lemonade_form = LemonadeEntryForm()
    # handle posts from form submission
    if request.method == 'POST' and 'submit' in request.POST:
        if Order.objects.get(id=request.session['id']).set.count() > 0:
            form = EntryForm(request.POST)

            if form.is_valid():

                name = Staff.objects.get(id=form.cleaned_data['name'])

                date = form.cleaned_data['date']

                c_order = Order.objects.get(id=request.session['id'])
                sale = Sale(
                    sales_person=name,
                    order=c_order,
                    date=date
                )
                sale.save()
                # make a new order
                order = Order()
                order.save()
                request.session['id'] = order.id

                request.session['submit'] = True

                return HttpResponseRedirect('')
        else:
            request.session['error_message'] = "In order to submit, add items to the list"
            form = EntryForm()

    else:
        form = EntryForm()

    order = Order.objects.get(id=request.session['id'])

    # handle submission message
    if 'submit' not in request.session or request.session['submit'] is False:
        submitted = False
    else:
        submitted = True

    request.session['submit'] = False

    template = {
        'submit': submitted,
        'form': form,
        'lemonade': lemonade_form,
        'order': order.set.all(),
        'total': order.get_price(),
        'error_message': request.session['error_message']
    }
    request.session['error_message'] = ""

    return render(request, 'form.html', template)


def remove_item(request, item, quantity):
    id = get_session(request)
    order = Order.objects.get(id=id)
    try:
        removed = order.set.get(lemonade=item)
        if removed.quantity > quantity:
            removed.quantity -= quantity
            removed.save(update_fields=['quantity'])
        else:
            removed.delete()
    except ObjectDoesNotExist:
        request.session['error_message'] = 'Lemonade to be removed was not part of the list'

    return HttpResponseRedirect('')


def add_item(request, item, quantity):
    id = get_session(request)
    order = Order.objects.get(id=id)
    try:
        added = order.set.get(lemonade=Lemonade.objects.get(id=item))
        added.quantity += quantity
        added.save(update_fields=['quantity'])
    except ObjectDoesNotExist:
        set = LemonadeSet(lemonade=Lemonade.objects.get(id=item), quantity=quantity)
        set.save()
        order.set.add(set)

    return HttpResponseRedirect('')


def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['name']
            start = date_to_url(form.cleaned_data['start_date'])
            end = date_to_url(form.cleaned_data['end_date'])
            return HttpResponseRedirect('{}/start={}/end={}'.format(employee, start, end))

    else:
        form = ReportForm()

    template = {
        'table': False,
        'form': form
    }

    return render(request, 'report.html', template)


def report_table(request, employee, start, end):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['name']
            start = date_to_url(form.cleaned_data['start_time'])
            end = date_to_url(form.cleaned_data['end_date'])
            return HttpResponseRedirect(reverse('report')+'{}/start={}/end={}'.format(employee, start, end))

    else:
        form = ReportForm()

    # filtering values for table
    sales = Sale.objects.filter(sales_person__exact=Staff.objects.get(id=employee))
    sales = sales.filter(date__gte=url_to_date(start))
    sales = sales.filter(date__lte=url_to_date(end))

    # computing values for table
    total_price = 0
    commission_earned = 0
    price = []
    commission = []
    for sale in sales:
        com = round(sale.get_commission(), 2)
        pr = round(sale.order.get_price(), 2)

        price.append(pr)
        commission.append(com)
        total_price += pr
        commission_earned += com

    template = {
        'table': True,
        'form': form,
        'total_price': total_price,
        'commission_earned': commission_earned,
        'sales': zip(sales, price, commission)
    }

    return render(request, 'report.html', template)
