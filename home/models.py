from django.db import models

from django.contrib.auth.models import AbstractUser
# for importing auth_user table
# from django.contrib.auth.models import User




# Create your models here.
class User(AbstractUser):
    role=models.CharField(max_length=50,null=True,blank=True)


class Driver(models.Model):
    user_id=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)             
    address=models.CharField(max_length=1024)
    phone=models.CharField(max_length=10)
    license_no=models.CharField(max_length=50)
    age=models.CharField(max_length=50)
    created_datetime=models.DateTimeField(auto_now_add=True)
    # signature=models.FileField(upload_to='driver', max_length=100)

    def __str__(self):
        return self.name
    
   

class Trip_details(models.Model):
    driver_id=models.ForeignKey(Driver,on_delete=models.CASCADE)
    booking_id=models.CharField(max_length=255,null=True,blank=True)
    driver_name=models.CharField(max_length=255)
    guest_name=models.CharField(max_length=255)
    address=models.CharField(max_length=1024)
    vehicle=models.CharField(max_length=255)
    vehicle_number=models.CharField(max_length=50)
    reporting_address=models.CharField(max_length=1024)
    releasing_address=models.CharField(max_length=1024)
    start_date=models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    start_time=models.TimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    start_km=models.IntegerField(null=True,blank=True)
    end_date=models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    end_time=models.TimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    end_km=models.IntegerField(null=True,blank=True)
    remark=models.CharField(max_length=2048)
    # nextdayuse=models.CharField(max_length=2048)
    status=models.CharField(max_length=50,default='pending')

    total_time=models.CharField(max_length=255)
    total_days=models.CharField(max_length=255)

    total_km=models.IntegerField(null=True,blank=True)
    driver_signature=models.FileField(upload_to='driver_signature', max_length=100)
    guest_signature=models.FileField(upload_to='guest_signature', max_length=100)


    def __str__(self):
        return self.guest_name





class route(models.Model):
    driver_id=models.ForeignKey(Driver,on_delete=models.CASCADE)
    trip_id=models.ForeignKey(Trip_details,on_delete=models.CASCADE)
    route=models.CharField(max_length=1024)

    def __str__(self):
        return self.route



# class Instruction(models.Model):
#     title=models.CharField(max_length=255)
#     content=models.CharField(max_length=3000)