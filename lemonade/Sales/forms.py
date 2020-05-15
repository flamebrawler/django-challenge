from django import forms
from .models import Staff, Lemonade


months = (
    (1, 'Jan'),
    (2, 'Feb'),
    (3, 'Mar'),
    (4, 'Apr'),
    (5, 'May'),
    (6, 'Jun'),
    (7, 'Jul'),
    (8, 'Aug'),
    (9, 'Sep'),
    (10, 'Oct'),
    (11, 'Nov'),
    (12, 'Dec'),
)


def iterable(queryset, defaulttext='Select Option'):
    return (('', defaulttext),)+tuple(zip(range(1, len(queryset)+1), queryset))


class ReportForm(forms.Form):
    name = forms.ChoiceField(label='Employee Name', choices=iterable(Staff.objects.all()), initial='')
    start_date = forms.DateField(label="Start Date")
    end_date = forms.DateField(label="End Date")


class EntryForm(forms.Form):
    name = forms.ChoiceField(label='Employee Name', choices=iterable(Staff.objects.all()), initial='')
    date = forms.DateField(label="Sale Date")


class LemonadeEntryForm(forms.Form):
    Lemonade = forms.ChoiceField(label='Lemonade Sold', choices=iterable(Lemonade.objects.all()), initial='')


