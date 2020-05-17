from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


def form(request):
    if 'id' not in request.session or not request.session['id']:
        order = Order()
        order.save()
        request.session['id'] = order.id

    if request.method == 'POST' and ('add' in request.POST or 'remove' in request.POST):
        lemonade_form = LemonadeEntryForm(request.POST)

        if 'add' in request.POST:
            if lemonade_form.is_valid():
                id = lemonade_form.cleaned_data['Lemonade']
                print('add-{}/'.format(id))
                return HttpResponseRedirect('add-{}/'.format(id))
        elif 'remove' in request.POST:
            if lemonade_form.is_valid():
                id = lemonade_form.cleaned_data['Lemonade']
                return HttpResponseRedirect('remove-{}/'.format(id))
    else:
        lemonade_form = LemonadeEntryForm()

    if request.method == 'POST' and 'submit' in request.POST:
        form = EntryForm(request.POST)

        if form.is_valid():

            name = Staff.objects.get(id=form.cleaned_data['name'])

            date = form.cleaned_data['date']

            id = request.session['id']
            sale = Sale(sales_person=name, order=Order.objects.get(id=id), date=date)
            sale.save()

            order = Order()
            order.save()
            request.session['id'] = order.id

            return HttpResponseRedirect('')
    else:
        form = EntryForm()

    order = Order.objects.get(id=request.session['id'])
    template = {
        'form': form,
        'lemonade': lemonade_form,
        'order': order.set.all(),
        'total': order.get_price(),
        'home': reverse('index')
    }
    return render(request, 'form.html', template)


def remove_item(request, item):
    id = request.session['id']
    order = Order.objects.get(id=id)
    try:
        removed = order.set.get(lemonade=item)
        if removed.quantity > 1:
            removed.quantity = removed.quantity - 1
            removed.save(update_fields=['quantity'])
        elif removed.quantity == 1:
            removed.delete()
    except ObjectDoesNotExist:
        request.session['error_message'] = 'Lemonade to be removed was not part of the list'

    return HttpResponseRedirect(reverse('form'))


def add_item(request, item):
    id = request.session['id']
    order = Order.objects.get(id=id)
    try:
        added = order.set.get(lemonade=Lemonade.objects.get(id=item))
        added.quantity = added.quantity + 1
        added.save(update_fields=['quantity'])
    except ObjectDoesNotExist:
        set = LemonadeSet(lemonade=Lemonade.objects.get(id=item), quantity=1)
        set.save()
        order.set.add(set)

    return HttpResponseRedirect(reverse('form'))


def report(request):
    return render(request, 'report.html')

