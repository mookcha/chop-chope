from django import forms

from models import *
import datetime
import pytz
from django.forms import ModelChoiceField
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

from django.forms import ModelForm


from datetimewidget.widgets import DateTimeWidget

class TableForm(ModelForm):
    class Meta:
        model = Table
        exclude = ('table_id',)


class BookingForm (forms.Form):
    table = forms.ModelChoiceField(queryset=Table.objects.all())
    start_time = forms.DateTimeField(
        widget=DateTimeWidget(usel10n=True, bootstrap_version=3, attrs={'class': 'form-control'}), required=True)
    end_time = forms.DateTimeField(
        widget=DateTimeWidget(usel10n=True, bootstrap_version=3, attrs={'class': 'form-control'}), required=True)


    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')

        if start_time != None and end_time != None:
            if end_time < start_time:
                raise forms.ValidationError("Invalid date entered: End date must be after start date")
        return cleaned_data

    def clean_start_date(self):
        utc = pytz.UTC
        start_time = self.cleaned_data.get('start_time')
        #start_time_utc = start_date.replace(tzinfo=utc)
        if start_time < datetime.datetime.now().replace(tzinfo=utc):
            raise forms.ValidationError("Please enter a date in future")
        return start_time

    def clean_end_date(self):
        utc = pytz.UTC
        end_time = self.cleaned_data.get('end_time')
        #end_time_utc = end_date.replace(tzinfo=utc)
        if end_time < datetime.datetime.now().replace(tzinfo=utc):
            raise forms.ValidationError("Please enter date in future")
        return end_time