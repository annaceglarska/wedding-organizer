from django.urls import path
from guests_management import views
from guests_management import api

urlpatterns = [
    #  main
    path('', views.wedding_organizer_start_name, name='wedding-organizer-start'),
    # end

    #  start guests
    path('guests/', views.guest_list, name='guest-list'),
    path('guests/filter/', views.one_guest_with_params, name='guest-with-params'),
    path('guests/<int:guest_id>/', views.one_guest, name='one-guest'),
    path('guests/add-new-guest', views.add_new_guest, name='form-add-new-guest'),
    #  end guests

    # start api
    path('api/guests/', api.guest_list_endpoint, name='guest-list-endpoint'),
    path('api/guests/<int:guest_id>/', api.one_guest_endpoint, name='one-guest-endpoint'),
    # end api
]
