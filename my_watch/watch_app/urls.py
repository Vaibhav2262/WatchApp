from django.contrib import admin
from django.urls import path
from watch_app import views
from django.conf.urls.static import static
from my_watch import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('register',views.register),
    path('login',views.user_login),  
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('pdetails/<pid>',views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('remove_order/<oid>',views.remove_order),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)