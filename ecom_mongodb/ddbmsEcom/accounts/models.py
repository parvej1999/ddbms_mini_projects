from django.db import models
from django.contrib.auth.models import User, AbstractUser
# from items.models import item
# Create your models here.

class User(AbstractUser):
    is_seller = models.BooleanField(default=False)

    def isSeller(self):
        return self.is_seller

class seller(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    # profileImage = models.ImageField(upload_to='static/items')
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=14)
    # items_sells = models.ForeignKey(item, on_delete=models.SET_NULL, null=True)
    IdProofType = models.CharField(max_length=60)
    uniqueIdProof = models.CharField(max_length=50)
    bankAccNum = models.CharField(max_length=25)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.OneToOneField(User, on_delete=models.CASCADE)
    sellerRating = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name + " " + str(self.createdBy)