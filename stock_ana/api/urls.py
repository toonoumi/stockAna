from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('search/<str:ticker>',views.search,name='search'),
]