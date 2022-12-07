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
    path('guests/add-new-guest/', views.add_new_guest, name='form-add-new-guest'),
    #  end guests

    # start table
    path('table/', views.table_list, name='table-list'),
    path('table/<int:pk>/', views.one_table, name='one-table'),
    path('table/add-new-table/', views.add_new_table, name='form-add-new-table'),
    path('table/edit-new-table/<int:table_id>', views.edit_new_table, name='one-table-form'),

    #end table

    # start api
    path('api/guests/', api.guest_list_endpoint, name='guest-list-endpoint'),
    path('api/guests/<int:guest_id>/', api.one_guest_endpoint, name='one-guest-endpoint'),
    path('api/table/<int:table_id>', api.delete, name='delete-objects'),
    # end api
]
