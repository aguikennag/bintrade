
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('company.urls')),
    path('',include('Users.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('wallet/',include('wallet.urls')),
    path('my-admin/',include('myadmin.urls'))
]


if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
