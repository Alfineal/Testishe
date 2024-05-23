from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Product, ProviderVariant, SizeVariant,Coupon
from random import random


class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')
    bio = models.TextField(null=True)



    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False, cart__user = self.user).count()
    

    def __str__(self):
        return self.user.email


    class Meta:
        verbose_name = "Профиль" 
        verbose_name_plural = "Профиль"


    


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []

        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.provider_variant:
                provider_variant_price = cart_item.provider_variant.price
                price.append(provider_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                price.append(size_variant_price)

        if self.coupon:
            print(self.coupon.minimum_amount)
            print(sum(price))
            if self.coupon.minimum_amount < sum(price):
                return sum(price) - self.coupon.discount_price


        return sum(price)


    class Meta:
        verbose_name = "Корзина" 
        verbose_name_plural = "Корзина"

    def __str__(self) -> str:
        return self.user



class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    provider_variant = models.ForeignKey(ProviderVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.product
    
    def get_product_price(self):
        price = [self.product.price]

        if self.provider_variant:
            provider_variant_price = self.provider_variant.price
            price.append(provider_variant_price)

        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        return sum(price)




    class Meta:
        verbose_name = "Предметы в корзине" 
        verbose_name_plural = "Предметы в корзине"

    


@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)

