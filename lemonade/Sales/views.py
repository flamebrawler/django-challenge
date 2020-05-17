from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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

    if request.method == 'POST':

        lemonade_form = LemonadeEntryForm(request.POST)

        if 'add' in request.POST:
            id = lemonade_form.cleaned_data['Lemonade']
            HttpResponseRedirect('add-%s/'.format(id))
        elif 'remove' in request.POST:
            id = lemonade_form.cleaned_data['Lemonade']
            HttpResponseRedirect('remove-%s/'.format(id))
        elif 'submit' in request.POST:
            form = EntryForm(request.POST)

            name = Staff.objects.get(id=form.cleaned_data['name'])
            lemonade = Lemonade.objects.get(id=form.cleaned_data['Lemonade'])
            date = form.cleaned_data['date']

            sale = Sale(sales_person=name, lemonade=lemonade, date=date)
            sale.save()
            HttpResponseRedirect('')
    else:
        form = EntryForm()
        lemonade_form = LemonadeEntryForm()

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
    removed = Order.objects.get(id=id).set.get(id=item)
    if removed:
        removed.quantity = removed.quanity - 1
        removed.save(update_fields=['quantity'])
    elif removed.quanity == 1:
        removed.delete()
    else:
        request.session['error_message'] = 'Lemonade to be removed was not part of the list'

    HttpResponseRedirect(reverse('form'))


def add_item(request, item):
    id = request.session['id']
    added = Order.objects.get(id=id).set.get(id=item)
    if added:
        added.quantity = added.quanity + 1
        added.save(update_fields=['quantity'])
    else:
        set = LemonadeSet(lemonade=item, quanity=1)
        Order.objects.get(id=id).set.add(set)

    HttpResponseRedirect(reverse('form'))


def report(request):
    return render(request, 'report.html')

