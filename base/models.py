from django.db import models
from django.conf import settings
from  django.shortcuts import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.text import slugify
from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model

#User Groups
from django.contrib.auth.models import Group

def add_user_to_group(request, user,**kwargs):
    user.groups.add(Group.objects.get(name='customers'))
    
user_signed_up.connect(add_user_to_group,sender=get_user_model())


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

    ('S','Online Payment'),
    ('C','Cash On Delivier '),

)

MAHARASHTRA_DISTRICTS=(
    ('Ah', 'Ahmednagar'), ('Ak', 'Akola'), ('Am', 'Amravati'),
     ('Au', 'Aurangabad'), ('Be', 'Beed'), ('Bh', 'Bhandara'), 
     ('Bu', 'Buldhana'), ('Ch', 'Chandrapur'), ('Dh', 'Dhule'),
      ('Ga', 'Gadchiroli'), ('Go', 'Gondia'), ('Hi', 'Hingoli'),
       ('Ja', 'Jalgaon'), ('Ja', 'Jalna'), ('Ko', 'Kolhapur'),
        ('La', 'Latur'), ('Mu', 'Mumbai'), ('Ng', 'Nagpur'),
         ('Na', 'Nanded'), ('Na', 'Nandurbar'), ('Ns', 'Nashik'), 
         ('Os', 'Osmanabad'), ('Pa', 'Parbhani'), ('Pu', 'Pune'), 
         ('Ra', 'Raigad'), ('Rt', 'Ratnagiri'), ('Sa', 'Sangli'),
          ('St', 'Satara'), ('Si', 'Sindhudurg'), ('So', 'Solapur'), 
          ('Th', 'Thane'), ('Wa', 'Washim'), ('Ya', 'Yavatmal')
)




class Item(models.Model):
    title =models.CharField( max_length=100,unique=True)
    price =models.FloatField()
    discount_price =models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,verbose_name='Availablity Of Product',max_length=2,default='NA')
    label_name= models.CharField(max_length=14,verbose_name='The Word Inside a label',blank=True,null=True)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1,default='P')
    slug=models.SlugField(max_length=150,blank=True,unique=True)
    description=models.TextField(max_length=1000)
    image=models.ImageField()
    image2=models.ImageField(blank=True)
    image3=models.ImageField(blank=True)
    image4=models.ImageField(blank=True)
    image5=models.ImageField(blank=True)
    image6=models.ImageField(blank=True)


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
        for order in  ShippmentOrder.objects.filter(payment_done=True):
            order=order.order
            for order_item in order.items.all():
                if order_item.item == self:
                    total_quantity+= order_item.qauntity
        return total_quantity

    def get_average_rating(self):
        all_messages=Comment.objects.filter(product=self)
        rate_list=[]
        for message in all_messages:
            if message.rating !=0:
                rate_list.append(message.rating)
        return int(round(sum(rate_list)/(len(rate_list) or 1),1))


    def get_no_of_items_of_that_month(self,month,year):
        total_quantity =0
        for order in  ShippmentOrder.objects.filter(payment_done=True,payment_done_date__month=month,payment_done_date__year=year):
            order=order.order
            for order_item in order.items.all():
                if order_item.item == self:
                    total_quantity+= order_item.qauntity
        return total_quantity
        

    def get_no_of_users_buy(self):
        user_list=[]
        for item in OrderItem.objects.filter(item=self):
            if item.user not in user_list:
                user_list.append(item.user)
        return len(user_list)


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

    def __str__(self):
        return '# Order No'+str(self.pk)




class BillingAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    city=models.CharField(choices=MAHARASHTRA_DISTRICTS,max_length=2,default='Mu')
    phone_number=models.CharField(max_length=20)
    street_address=models.CharField(max_length=250)
    apartment_address=models.CharField(max_length=250)
    pin_code=models.CharField(max_length=10)
    payment_option = models.CharField(choices=PAYMENTS_CHOICES,max_length=1,default='S')




    class Meta:
        verbose_name = ("Billing Address")
        verbose_name_plural = ("Billing Adresss")

    

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


class ShippmentOrder(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order=models.ForeignKey('Order',on_delete=models.CASCADE)
    verify_order = models.BooleanField(default=False,blank=True)
    verify_done_date= models.DateTimeField(blank=True,null=True)
    delivered= models.BooleanField(default=False,blank=True)
    delivered_done_date= models.DateTimeField(blank=True,null=True)
    payment_done=models.BooleanField(default=False,blank=True)
    payment_done_date= models.DateTimeField(blank=True,null=True)
    report_spam=models.BooleanField(default=False,blank=True)
    description=models.TextField(max_length=250,blank=True,verbose_name='Some Reason Why You Want To Spam This Order')


    class Meta:
        verbose_name = "ShippmentOrder"
        verbose_name_plural = "ShippmentOrders"

    def get_order_complete(self):
        order_complete=False
        if self.verify_order and self.delivered and self.payment_done:
            order_complete=True

        return order_complete


        

    
    

