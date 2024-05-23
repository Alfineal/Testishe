from django.urls import path
from accounts.views import login_page,register_page , activate_email, cart, add_to_cart,remove_cart, logout_user,remove_coupon,profile_page,payment_page, search_venues, delivery_page, orders_page
#from products.views import add_to_cart
urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('logout/', logout_user, name="logout"),
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   path('cart/' , cart, name="cart"),
   path('add-to-cart/<uid>/' , add_to_cart, name="add_to_cart"),
   path('remove-cart/<cart_item_uid>/' , remove_cart, name="remove_cart"),
   path('remove-coupon/<cart_id>/', remove_coupon , name = "remove_coupon"),
   path('search-venues/' , search_venues, name="search_venues"),
   path('profile-page/' , profile_page , name="profile_page" ),
   path('payment-page/' , payment_page , name="payment_page" ),
   path('delivery-page/' , delivery_page , name="delivery_page" ),
   path('orders-page/' , orders_page , name="orders_page" ),



]