from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('chat/<uuid:page_slug>/', home_view, name='home_detail')
]