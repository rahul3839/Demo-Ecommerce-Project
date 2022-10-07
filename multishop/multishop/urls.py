"""multishop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Index,name='home'),
    path('shop/',views.Shop ,name='shop'),
    path('detail/',views.Detail,name='detail'),
    path('cart/',views.add_to_card,name='cart'),
    path('showcart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('delete/<int:id>',views.cart_delete,name='cart_del'),
    path('checkout/',views.Checkout,name='checkout'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('contact/',views.Contact,name='contact'),
    path('about/',views.About,name='about'),
    path('regis/',views.RegistrationView,name='regis'),
    path('userlogin/',views.user_login,name='userlogin'),
    path('userlogout/',views.UserLogout,name='userlogout'),
    path('changepassword/',views.ChangePassword,name='changepassword'),
    # path('forgetpass/',views.FogetPassword,name='forgetpass'),
    path('profile/',views.profile,name='profile'),


  
    


     # rest password urls #
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='app/registration/password_reset_form.html'),name='reset_password'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='app/registration/password_rest_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='app/registration/password_reset_complete.html'),name='password_reset_complete'),


 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



