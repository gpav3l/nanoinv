import os
from django.db import models
from django.dispatch import receiver

# Model for describe database Items
class Items(models.Model):
    inventory_number = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, blank=True)
    amount = models.PositiveIntegerField(default=1)
    unit_of_meas = models.CharField(max_length=5, blank=True)
    price = models.FloatField(default=0.0)
    point_man = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)
    date_start_use = models.DateField()
    date_end_use = models.DateField()
    last_update = models.DateField(auto_now=True)

    class Meta:
        db_table = "Items"


class Item_images(models.Model):
    parent = models.ForeignKey('Items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/item/')
    class Meta:
        db_table = "Item_images"


# Model for describe database Users
class Users(models.Model):
    fio = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = "Users"


# Model for describe database Locations
class Locations(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "Locations"


# Model for describe database Include_items
class Include_items(models.Model):
    parrent_id = models.ForeignKey('Items', on_delete=models.CASCADE)
    inventory_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, blank=True)
    amount = models.PositiveIntegerField(default=1)
    unit_of_meas = models.CharField(max_length=5, blank=True)
    price = models.FloatField(default=0.0)
    point_man = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)
    date_start_use = models.DateField()
    date_end_use = models.DateField()
    last_update = models.DateField(auto_now=True)

    class Meta:
        db_table = "Include_items"


class Include_item_images(models.Model):
    parent = models.ForeignKey('Include_items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/subitem/')
    class Meta:
        db_table = "Include_item_images"


# Model for Update_hitory
class Update_hitory(models.Model):
    last_update = models.DateTimeField(auto_now=True)
    item_id = models.PositiveBigIntegerField()
    tbl_name = models.CharField(max_length=255)
    prev_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)

    class Meta:
        db_table = "Update_hitory"


@receiver(models.signals.post_delete, sender=Include_item_images)
@receiver(models.signals.post_delete, sender=Item_images)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print("Call handler")
    if instance.image:
        print(f"Try remove file {instance.image.path}")
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)