from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import *
from .forms import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


def form(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            name = Staff.objects.get(id=form.cleaned_data['name'])
            lemonade = Lemonade.objects.get(id=form.cleaned_data['Lemonade'])
            date = form.cleaned_data['date']
            sale = Sale(sales_person=name, lemonade=lemonade, date=date)
            sale.save()
            HttpResponseRedirect('')
    else:
        form = EntryForm()
    return render(request, 'form.html', {'form': form})


def report(request):
    return render(request, 'report.html')

