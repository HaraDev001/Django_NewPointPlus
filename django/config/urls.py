from django.urls import include, path

import os
import environ
from pathlib import Path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView  # 追加


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


urlpatterns = [
    path('shop/api/v1/', include('v1_shop.urls')),
    path('console/api/v1/', include('v1_console.urls')),
    path('card/api/v1/', include('v1_card.urls')),
    path('terminal/api/v1/', include('v1_terminal.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


if env('DEBUG', bool):
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),                                      # 追加
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # 追加
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),              # 追加
    ]
