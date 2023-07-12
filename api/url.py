from django.urls import path
from .views import crawl_url

app_name = 'api'

urlpatterns = [
    path('crawl/', crawl_url, name='crawl_url'),
    # 其他 API URL 配置...
]
