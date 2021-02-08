from django import forms
from django.core.validators import MinValueValidator
from .models import Accomodation,Units,RoomAssignment

class CheckOutForm(forms.Form):
	mobile_money_number = forms.CharField(max_length=10,help_text="Only MTN numbers allowed")
	day_of_moving_in = forms.DateField(initial="25 October 2006",input_formats=["%d %B %Y"],widget=forms.DateInput)
	duration = forms.IntegerField(initial=16,help_text="Enter the duration of stay in weeks",validators=[MinValueValidator(16)])
	currency = forms.ChoiceField(choices=[("EUR","EUR")])

class HostelUpdateForm(forms.ModelForm):
	class Meta:
		model = Accomodation
		fields = ('name','location','for_students','location_nick_name','university','image1','image2','image3','image4','image5')

class UnitUpdateForm(forms.ModelForm):
	class Meta:
		model = Units
		fields = ('unit_type','additional_services','amount_per_month','minimum_number_of_months','actual_amount','capacity','available_number','is_self_contained')


class AssignForm(forms.ModelForm):
	class Meta:
		model = RoomAssignment
		fields = ('room_name',)