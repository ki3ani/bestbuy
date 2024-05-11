from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include  # or whatever else you're including

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('store.urls')),
]