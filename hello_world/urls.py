from django.urls import path
from hello_world import views
from hello_world import api

urlpatterns = [
    path('', views.hello_world_name, name='hello_world'),
    #path('<slug:name>/', views.hello_world_name, name='hello_world_with_name'),
    #path('add-two-numbers/', api.addTwoNumbersView, name='add-two-numbers'),
    #path('<int:value>/', views.calculate, name='calculate'),
    path('guests/', views.guestList, name='guest-list'),
    path('guests/filter', views.oneGuestWithParams, name='guest-with-params'),
    path('guests/<int:guest_id>/', views.oneGuest, name='oneGuest')
]