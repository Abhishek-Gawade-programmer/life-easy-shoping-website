from django.db import models
from django.conf import settings
from  django.shortcuts import reverse
CATEGORY_CHOICES=(
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Outwear'),

)
LABEL_CHOICES=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)






class Item(models.Model):
    title =models.CharField( max_length=100)
    price =models.FloatField()
    discount_price =models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1)
    slug=models.SlugField()
    description=models.TextField()
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("base:product-view", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("base:add-to-cart", kwargs={"slug": self.slug})

    



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    qauntity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.qauntity} on {self.item.title}"




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    items =models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date =models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    def __str__(self):
        return self.user.username

    

