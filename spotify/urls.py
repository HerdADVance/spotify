
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myauth.urls')),
    path('', include('core.urls')),
    path('podcasts/', include('podcasts.urls')),
    path('', include('search.urls')),
]
