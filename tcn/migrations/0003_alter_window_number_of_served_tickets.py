# Generated by Django 5.0.6 on 2024-06-27 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcn', '0002_office_counter_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='window',
            name='number_of_served_tickets',
            field=models.IntegerField(default=0),
        ),
    ]
