from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accommodation.urls')),
    path('Authentication/', include('accounts.urls')),
    path('students/', include('students.urls')), 
    
]
