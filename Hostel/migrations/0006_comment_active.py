# Generated by Django 3.0.2 on 2020-02-20 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hostel', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]