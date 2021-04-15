from django.db import models
from django.conf import settings
from  django.shortcuts import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.text import slugify


CATEGORY_CHOICES=(
    ('A','Available'),
    ('NA','Not Available'),

)
LABEL_CHOICES=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)


PAYMENTS_CHOICES =(

    ('S','Stripe'),
    ('C','Cash On Delivier '),
     ('P','PayPal'),

)



class Item(models.Model):
    title =models.CharField( max_length=100)
    price =models.FloatField()
    discount_price =models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label_name= models.CharField(max_length=14,verbose_name='The Word Inside a label',blank=True,null=True)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1)
    slug=models.SlugField(max_length=150,blank=True)
    description=models.TextField()
    image=models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("base:product-view", kwargs={"slug": self.slug})

        

    def get_absolute_admin_url(self):
        return reverse("base:product-view", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("base:add-to-cart", kwargs={"slug": self.slug})


    def get_no_of_comments(self):
        return Comment.objects.filter(product=self).count()

    def get_no_of_items(self):
        total_quantity =0
        for product in OrderItem.objects.filter(item=self):
            total_quantity+=product.qauntity
        return total_quantity

    def get_remove_to_cart_url(self):
        return reverse("base:remove-from-cart", kwargs={"slug": self.slug})

    



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    qauntity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.qauntity} on {self.item.title}"

    def get_total_item_price(self):
        return self.qauntity * self.item.price

    def get_total_discount_price(self):
        return self.qauntity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price()-self.get_total_discount_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    items =models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date =models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    billing_address=models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total +=order_item.get_final_price()
        return total



class BillingAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    city=models.CharField(max_length=20)
    phone_number=models.CharField(max_length=20)
    street_address=models.CharField(max_length=250)
    apartment_address=models.CharField(max_length=250)
    pin_code=models.CharField(max_length=10)
    payment_option = models.CharField(choices=PAYMENTS_CHOICES,max_length=1,default='S')




    class Meta:
        verbose_name = ("Billing Address")
        verbose_name_plural = ("Billind Adresss")

    

class Comment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Item,on_delete=models.CASCADE)
    # as we can rate [1-5] so 0 means no rate yet
    rating = models.IntegerField(default=0,validators=[ 
                MaxValueValidator(5),MinValueValidator(0)
            ])
    body = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    

