from django.urls import path
from .import views as e_commerce

app_name = "hostels"

urlpatterns = [
	path('',e_commerce.IndexView.as_view(),name='hostel_home'),
	path('detail/<int:pk>/',e_commerce.DetailView.as_view(),name = 'hostel_detail'),
	path('detail/<int:accomodation_id>/reserve/',e_commerce.checkoutview, name = 'checkout'),
	path('<int:accomodation_id>/dashboard/',e_commerce.hostelDashboardView,name = 'dashboard'),
	path('<int:pk>/update/',e_commerce.AccomodationUpdateView.as_view(),name = 'acc_update'),
	path('<int:pk>/update/unit',e_commerce.UnitUpdateView.as_view(),name = 'unit_update'),
	path('<int:payment_id>/payment/',e_commerce.paymentDetailView,name = 'assign'),
	path('<int:pk>/payment/assign_room',e_commerce.RoomAssignView.as_view(),name = 'assign_room'),
	path('<int:assignment_id>/completed',e_commerce.assignmentdetailview,name = 'assign_detail'),
	path('search/',e_commerce.searchview,name="search"),
	path('detail/<int:accomodation_id>/thanks/',e_commerce.thankyouview,name="thanks"),
	path('error/',e_commerce.errorview,name="error")
]