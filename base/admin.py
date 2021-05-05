from django.contrib import admin

from .models import Item,OrderItem,Order,Comment,BillingAddress,ShippmentOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','ordered')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('product', 'rating', 'body', 'created', 'updated')


@admin.register(BillingAddress)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user','city','phone_number','street_address',
		'apartment_address','pin_code','payment_option',)


admin.site.register(Order, OrderAdmin)


admin.site.register(ShippmentOrder)
admin.site.register(Item)
admin.site.register(OrderItem)



# admin.site.register(Order)
# admin.site.register(BillingAddress)