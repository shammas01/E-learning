from django.contrib import admin
from . models import CartItem,UserCart,OrderPlaced,liveEnroll

# Register your models here.
@admin.register(UserCart) # this is for admin side after creating i will change
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('id','user','created_at','modified_at','is_active')


@admin.register(CartItem)
class CartitemsAdmin(admin.ModelAdmin):
    list_display = ('id','cart','course','price')


@admin.register(OrderPlaced)
class CourseOrderdAdmin(admin.ModelAdmin):
    list_display = ('id','user','course','ordered_date')


@admin.register(liveEnroll)
class LiveEnrolledAdmin(admin.ModelAdmin):
    list_display = ('id','user','lives','enrolled_date')
