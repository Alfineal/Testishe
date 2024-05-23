from django.contrib import admin

from .models import *


admin.site.register(Category)

admin.site.register(Coupon)



class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name' , 'price']
    inlines = [ProductImageAdmin]


@admin.register(ProviderVariant)
class ProviderVariantAdmin(admin.ModelAdmin):
    list_display = ['provider_name' , 'price']
    model = ProviderVariant


@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name' , 'price']
    model = SizeVariant    

admin.site.register(Product, ProductAdmin)


admin.site.register(ProductImage)
