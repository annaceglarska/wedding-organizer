from django.urls import path
from hello_world import views
from hello_world import api

urlpatterns = [
    path('guests/', views.guest_list, name='guest-list'),
    # path('add-two-numbers/', api.addTwoNumbersView, name='add-two-numbers'),
    path('guests/filter', views.one_guest_with_params, name='guest-with-params'),
    path('guests/<int:guest_id>/', views.one_guest, name='one-guest'),
    path('', views.wedding_organizer_start_name, name='wedding-organizer-start'),
    path('<slug:name>/', views.wedding_organizer_start_name, name='wedding-organizer-start-name'),
]
