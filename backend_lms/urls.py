from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('admin_panel.urls')),
    path('api/', include('course.urls')),
    path('api/', include('home.urls')),
    path('api/', include('enrollment.urls')),
    path('api/', include('enrollment.razorpay.urls')),
    path('api/', include('openai_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
