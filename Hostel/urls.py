from django.urls import path
from .views import HostelDetailView, HostelUpdateView
from .import views as hostel_views

urlpatterns = [
    path('',hostel_views.home, name = 'hostels'),
    path('hostel/<int:pk>/', HostelDetailView.as_view(), name = 'hostel-detail'),
    path('hostel/<int:pk>/dashboard/', HostelUpdateView.as_view(), name = 'dashboard'),
    path('about/',hostel_views.about, name = 'about'),
    path('hostel/<int:pk>/checkout/', hostel_views.checkout1, name = 'checkout'),
    path('hostel/search/', hostel_views.search, name = 'search'),
    path('hostel/<int:pk>/checkout/confirmation', hostel_views.confirmation, name = 'confirmation')
]
