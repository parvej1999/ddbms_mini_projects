from django.db import models
from django.contrib.auth import get_user_model
# from accounts.models import User
User = get_user_model()



# Create your models here.
class item(models.Model):
    title = models.CharField(max_length=50)
    discription = models.CharField(max_length=100)
    price = models.FloatField()
    stockQty = models.IntegerField(default=1)
    category = models.CharField(max_length=50)
    prodImage = models.ImageField(upload_to = "static/items")
    addedBY = models.ForeignKey(User, on_delete = models.CASCADE)
    createTime = models.DateTimeField(auto_now_add = True)
    updatedON = models.DateTimeField(auto_now = True)    

    def __str__(self):
        return "Item"+str(self.id) + " "+str(self.title)

class cart(models.Model):
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    total_price = models.FloatField(default=0)
    isOrdered = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.item.title