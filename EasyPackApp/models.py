from django.db import models
import pytz
import uuid
from django.utils.timezone import now
from datetime import timedelta

# registrations 

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Store created_at in IST (Asia/Kolkata) timezone"""
        ist = pytz.timezone('Asia/Kolkata')
        self.created_at = now().astimezone(ist)
        super().save(*args, **kwargs)

    def is_valid(self):
        """OTP expires in 5 minutes"""
        ist = pytz.timezone('Asia/Kolkata')
        expiration_time = self.created_at + timedelta(minutes=5)
        return now().astimezone(ist) <= expiration_time

    def __str__(self):
        return f'{self.email} - {self.otp} - {self.created_at.astimezone(pytz.timezone("Asia/Kolkata"))}'


class BoxModel(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    paper_brown_img = models.FileField(upload_to='box_images/', null=True, blank=True)
    paper_white_img = models.FileField(upload_to='box_images/', null=True, blank=True)
    paper_brown_price = models.DecimalField(max_digits=10, decimal_places=2)
    paper_white_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)   
     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class BoxSizeModel(models.Model):
    box = models.ForeignKey(BoxModel, related_name='sizes', on_delete=models.CASCADE)
    size_label = models.CharField(max_length=50)  # e.g., Small, Medium, Large
    size_ratio = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=10, decimal_places=2)  # in cm
    width = models.DecimalField(max_digits=10, decimal_places=2)   # in cm
    height = models.DecimalField(max_digits=10, decimal_places=2)  # in cm
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)  # in kg
    paper_brown_img = models.FileField(upload_to='box_images/', null=True, blank=True)
    paper_white_img = models.FileField(upload_to='box_images/', null=True, blank=True)
    paper_brown_price = models.DecimalField(max_digits=10, decimal_places=2)
    paper_white_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.box.title} - {self.size_label}"


class BoxBookings(models.Model):
    box = models.ForeignKey(BoxModel, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    size = models.ForeignKey(BoxSizeModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    custom_design = models.FileField(upload_to='custom_designs/', null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
