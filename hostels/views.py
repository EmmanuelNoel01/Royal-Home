from datetime import datetime,timedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse
from .models import Accomodation,Payment,Units,RoomAssignment
from django.db.models import Q
from django.contrib import messages
from .forms import CheckOutForm,HostelUpdateForm,UnitUpdateForm,AssignForm
# Create your views here.

#LANDING PAGE
class IndexView(generic.ListView):
	template_name = 'hostels/home.html'
	model = Accomodation
	paginate_by = 3

#DETAIL VIEW	
class DetailView(generic.DetailView):
	template_name = 'hostels/detail.html'
	model = Accomodation
	context_object_name = "accomodation"
# def DetailView(request,accomodation_id):
# 	return render(request,'hostels/detail.html')

#CHECKOUT PAGE
@login_required
def checkoutview(request,accomodation_id):
	accomodation = get_object_or_404(Accomodation,pk=accomodation_id)

	if request.method == 'POST':
		checkout_form = CheckOutForm(request.POST)
		if checkout_form.is_valid():
			payer = request.user
			phone_number = checkout_form.cleaned_data.get('mobile_money_number')
			unit = request.POST['unit']
			print("My guy"+unit)
			day_of_moving_in = checkout_form.cleaned_data.get('day_of_moving_in')
			duration_of_occupancy = timedelta(weeks = checkout_form.cleaned_data.get('duration'))
			amount = accomodation.units_set.get(unit_type=unit).actual_amount
			currency = checkout_form.cleaned_data.get("currency")

			payment = Payment.objects.create(
				payer=payer,
				accomodation=accomodation,
				amount=amount,
				phone_number=phone_number,
				unit = unit,
				day_of_moving_in = day_of_moving_in,
				duration_of_occupancy = duration_of_occupancy,
				currency=currency,
				)
			assign = RoomAssignment.objects.create(payment=payment)
			print("payment_object_created")
			payment.day_of_moving_out = payment.calculate_exit_date()
			print(payment.day_of_moving_out)
			payment.save()
			print("Payment object saved ")
			execute = payment.collect_money()
			print(execute)
			if execute.get('is_successful'):
				print("Collect money returned true")
				payment.is_complete = True
				payment.status_code = execute.get("status_code")
				payment.save()
				return HttpResponseRedirect(reverse('hostels:thanks', args=([accomodation.id])))
			else:
				form = CheckOutForm(request.POST)
				context = {
					"form":form,
				}
				return HttpResponseRedirect(reverse('hostels:error' ))
	else:
		form = CheckOutForm()
		units = accomodation.units_set.all()
		context = {
			"form":form,
			"accomodation":accomodation,
			"units":units,			
		} 
		return render(request,"hostels/checkout.html",context)

#HOSTEL OWNER DASHBOARD
def hostelDashboardView(request,accomodation_id):
	accomodation = get_object_or_404(Accomodation,pk=accomodation_id)
	payments = accomodation.payment_set.filter(Q(is_complete=True),Q(is_assigned=False))
	assigneds = accomodation.payment_set.filter(Q(is_complete=True),Q(is_assigned=True))
	return render(request,"hostels/dashboard.html",{"payments":payments,"accomodation":accomodation,"assigneds":assigneds})

#SEARCH RESULTS VIEW
def searchview(request):
		query_set = Accomodation.objects.filter(Q(name__icontains=request.POST['q']) | Q(location__icontains=request.POST['q']) | Q(location_nick_name__icontains=request.POST['q']))
		if len(query_set) >= 1:
			results_present = True
			context = {
				'accomodations':query_set,
				'results_present':results_present
				}
			return render(request,'hostels/search.html',context)
		else:
			results_present = False
			context = {
				'error_message':'We did not find anything related to your search. We\'ll try to include that property in our system.',
				'results_present':results_present

			}
			return render(request,'hostels/search.html',context)

def thankyouview(request,accomodation_id):
	accomodation = get_object_or_404(Accomodation,pk=accomodation_id)
	send_mail(
	    'CONFIRMATION OF PAYMENT FOR ACCOMODATION AT '+accomodation.name,
	    'Your payment has been received and an email will be sent to you with reservation details',
	    'elijahokellp@gmail.com',
	    [request.user.email],
	    fail_silently=False,
		)
	return render(request,'hostels/thankyou.html')

def errorview(request):
	error = "Ooops!! Transaction wasn't successful either due to wrong information submitted or due to a technical issue."
	return render(request,"hostels/payment_error.html",{'error_message':error})

class AccomodationUpdateView(generic.UpdateView):
	model = Accomodation
	template_name = "hostels/accomodation_update.html"
	fields = ["name","for_students","location_nick_name","university","image1","image2","image3","image4","image4"]
	context_object_name = "accomodation"

	def form_valid(self,form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

class UnitUpdateView(generic.UpdateView):
	model = Units
	template_name = "hostels/unit_update.html"
	fields = ["unit_type","additional_services","amount_per_month","minimum_number_of_months","actual_amount","capacity","available_number","is_self_contained"]
	context_object_name = "unit"

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

def paymentDetailView(request,payment_id):
	payment = get_object_or_404(Payment,pk=payment_id)
	assignment = payment.roomassignment_set.get(pk=payment_id)
	return render(request,"hostels/payment.html",{"payment":payment,"assignment":assignment})

class RoomAssignView(generic.UpdateView):
	model = RoomAssignment
	template_name = "hostels/room_assign.html"
	fields = ['room_name']
	context_object_name = "assignment"

	def form_valid(self,form):
		assignment = self.get_object()
		send_mail(
		    'RESERVATIOPN DETAILS FOR '+assignment.payment.payer.username+' IN '+assignment.payment.accomodation.name,
		    'Room Name:'+assignment.room_name,
		    'elijahokellp@gmail.com',
		    [assignment.payment.payer.email],
		    fail_silently=True,
			)
		payment = get_object_or_404(Payment,pk=assignment.payment.id)
		payment.is_assigned = True
		payment.save()
		return super().form_valid(form)

def assignmentdetailview(request,assignment_id):
	assignment = get_object_or_404(RoomAssignment,pk=assignment_id)
	return render(request,"hostels/assign.html",{"assignment":assignment})
