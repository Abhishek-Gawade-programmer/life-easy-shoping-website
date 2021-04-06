from django.contrib import admin

from .models import Item,OrderItem,Order,Comment


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','ordered')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('product', 'rating', 'body', 'created', 'updated')

admin.site.register(Order, OrderAdmin)


admin.site.register(Item)
admin.site.register(OrderItem)
# admin.site.register(Order)
# admin.site.register(BillingAddress)