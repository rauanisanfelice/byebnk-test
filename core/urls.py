from django.urls import path, include
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title = "Django API Cockpit",
        default_version = '1.0.0',
        description = "Django REST Framework API Cockpit Teste Byebnk.",
        contact = openapi.Contact(email="rauan.sanfelice@gmail.com"),
        license = openapi.License(name="BSD License"),
    ),
    public = True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('21232f297a57a5a743894a0e4a801fc3/', admin.site.urls),
    path('api/', include('cockpit.urls')),    
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]