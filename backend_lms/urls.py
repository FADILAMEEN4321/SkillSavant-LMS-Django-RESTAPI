from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SkillSavant API",
      default_version='v1',
      description="API documentation of SkillSavant.",
   ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('admin_panel.urls')),
    path('api/', include('course.urls')),
    path('api/', include('home.urls')),
    path('api/', include('enrollment.urls')),
    path('api/', include('enrollment.razorpay.urls')),
    path('api/', include('openai_api.urls')),
    path('api/', include('chat.urls')),
    path('api/documentation/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
