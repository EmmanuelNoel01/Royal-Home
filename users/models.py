from django.db import models
from custom_user.models import User
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(default=0)
    program = models.CharField(default='Bachelors',max_length=200)
    year_of_study = models.IntegerField(default=0)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{ self.user.username } Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail=(output_size)
            img.save(self.image.path)
