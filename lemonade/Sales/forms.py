from django import forms
from .models import Staff, Lemonade


def iterable(queryset, defaulttext='Select Option'):
    return (('', defaulttext),)+tuple(zip(range(1, len(queryset)+1), queryset))


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class ReportForm(forms.Form):
    name = forms.ChoiceField(label='Employee Name', choices=iterable(Staff.objects.all()), initial='')
    start_date = forms.DateTimeField(widget=DateTimeInput, label="Start Date")
    end_date = forms.DateTimeField(widget=DateTimeInput, label="End Date")


class EntryForm(forms.Form):
    name = forms.ChoiceField(label='Employee Name', choices=iterable(Staff.objects.all()), initial='')
    date = forms.DateTimeField(widget=DateTimeInput, label="Sale Date/Time")


class LemonadeEntryForm(forms.Form):
    Lemonade = forms.ChoiceField(label='Lemonade Sold', choices=iterable(Lemonade.objects.all()), initial='')
    quantity = forms.IntegerField(label="Qty", min_value=1)

