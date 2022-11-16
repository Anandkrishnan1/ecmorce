from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('coming/',views.coming),
    path('contact/',views.contact),
    path('login/',views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    path('shop/',views.shop),
    path('single/',views.single),
    path('add_tocart/',views.add_tocart),
    path('cart/',views.cart),
    path('additem/',views.additem),
    path('delete/',views.delete),
    path('payment/',views.payment),
    

###############################################################################################################################################
                                                        #admin#
###############################################################################################################################################
    
    path('indexadmin/',views.index_admin),
    path('loginadmin/',views.login_admin),
    path('inbox/',views.inbox),
    path('inboxdetails/',views.inbox_details),
    path('proupdate/',views.proupdate),
    path('adim_signup/',views.adim_signup),
    path('logoutadmin/',views.logout_admin),
    path('forgetpass/',views.passwordforget),
    path('resetpass/',views.restpass),
    path('ajaxview/',views.ajaxview),
    

    
    















   








    
]