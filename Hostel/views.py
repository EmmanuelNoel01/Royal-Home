from abc import ABC
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import http.client, urllib.request, urllib.parse, urllib.error, base64
from .models import Hostel, Comment
from .forms import CommentForm

# Create your views here.


def home(request):
    #comment = get_object_or_404(Comment)
    #hostels = get_object_or_404(Hostel)
    if request.method == 'POST':
        user_comment = CommentForm(request.POST, instance = request.user)
        if user_comment.is_valid():
            user_comment.save()
            messages.success(request,f'Your comment has been sent. We will get back to you shortly')
            return redirect('hostels')
    else:
        user_comment = CommentForm()
    context = {
        'form':user_comment,
        'hostels':Hostel.objects.all(),
        'user_comments': Comment.objects.filter(active=True),
    }
    return render(request, 'Hostel/home.html',context)


class HostelDetailView(DetailView):
    model = Hostel
    template_name = 'Hostel/detail.html'
    context_object_name = 'hostel'


class HostelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = Hostel
    fields = [
        'hostel_name',
        'picture',
        'location',
        'room_sizes',
        'bed_sizes',
        'has_canteen',
        'has_shuttle',
        'has_swimming_pool',
        'has_gym',
        'has_wifi',
        'has_water',
        'has_restaurant',
        'self_contained',
        'room_cleaning_services',
        'cable_tv',
        'capacity',
        'image1',
        'image2',
        'image3',
        'image4',
        'image5',
    ]

    def form_valid(self, form):
        form.instance.owner == self.request.user
        return super().form_valid(form)

    def test_func(self):
        hostel = self.get_object()
        if self.request.user == hostel.owner:
            return True
        return False

def about(request):
    return render(request, 'Hostel/about.html')


def search(request):
    # query = request.GET.get('q')
    # results = Hostel.objects.filter(Q(name__icontains=query) & Q(location__icontains=query) & Q(description__icontains=query))
    # context = {
    #     'Hostel':results
    # }
    return render(request, 'Hostel/search.html', context)

@login_required
def checkout1(request):

    headers = {
        # Request headers
        'Authorization': '',
        'X-Callback-Url': '',
        'X-Reference-Id': '',
        'X-Target-Environment': '',
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '{subscription key}',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return render(request,'Hostel/checkout.html')


@login_required
def confirmation(request):
    return render(request,'Hostel/confirmation.html')
