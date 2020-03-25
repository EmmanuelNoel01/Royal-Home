from django.db import models
from custom_user.models import User
from django.urls import reverse
# Create your models here.

class Hostel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel_unique_identifier = models.CharField( default="null", max_length=10, primary_key=True)
    description = models.TextField(default="null")
    hostel_name = models.CharField(max_length=100)
    single_room_price = models.IntegerField(default=100)
    double_room_price = models.IntegerField(default=100)
    booking_price = models.IntegerField(default=100)
    picture = models.ImageField(default='default.jpg')
    location = models.TextField()
    has_canteen = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    room_cleaning_services = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_shuttle = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    number_of_rooms = models.IntegerField()
    image1 = models.ImageField(default='default.jpg', upload_to='pictures')
    image2 = models.ImageField(default='default.jpg', upload_to='pictures')
    image3 = models.ImageField(default='default.jpg', upload_to='pictures')
    image4 = models.ImageField(default='default.jpg', upload_to='pictures')
    image5 = models.ImageField(default='default.jpg', upload_to='pictures')
    image6 = models.ImageField(default='default.jpg', upload_to='pictures')

    def __str__(self):
        return self.hostel_name

    def get_absolute_url(self):
        return reverse('hostel-detail', kwargs={'pk':self.pk})


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    number = models.CharField(default='A1', max_length=50)
    type = models.CharField(default='single', max_length=50)
    room_sizes = models.IntegerField(default='20 x 20')
    bed_sizes = models.IntegerField(default='6 x 6')
    self_contained = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)


class Comment(models.Model):
    users_name = models.CharField(max_length=20)
    user_email = models.EmailField()
    content = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.users_name


'''
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
'''
