from django.urls import path
from guests_management import controllers
from guests_management import api

urlpatterns = [
    #  main
    path('', controllers.wedding_organizer_start_name, name='wedding-organizer-start'),
    # end

    #  start guests
    path('guests/', controllers.guest_list, name='guest-list'),
    path('guests/filter/', controllers.one_guest_with_params, name='guest-with-params'),
    path('guests/<int:guest_id>/', controllers.one_guest, name='one-guest'),
    path('guests/add-new-guest/', controllers.add_new_guest, name='form-add-new-guest'),
    path('guests/edit-guest/<int:guest_id>', controllers.edit_guest, name='edit-guest'),
    #  end guests

    # start table
    path('table/', controllers.table_list, name='table-list'),
    path('table/<int:pk>/', controllers.one_table, name='one-table'),
    path('table/add-new-table/', controllers.add_new_table, name='form-add-new-table'),
    path('table/edit-new-table/<int:table_id>', controllers.edit_new_table, name='one-table-form'),

    #end table

    # start seating
    path('seating/add-seating', controllers.create_seating, name='add-seating'),
    path('seating/edit-seating/<int:seating_id>', controllers.edit_seating, name='edit-seating'),
    path('seating/delete-seating/<int:seating_id>', controllers.delete_seating, name='delete-seating'),
    # end seating

    # start api
    path('api/guests/', api.guest_list_endpoint, name='guest-list-endpoint'),
    path('api/guests/<int:guest_id>/', api.one_guest_endpoint, name='one-guest-endpoint'),
    path('api/table/<int:table_id>', api.delete, name='delete-objects'),
    path('api/guest-delete/<int:guest_id>', api.delete_guest, name='delete-guest'),
    path('api/seat/<int:table_id>', api.get_free_seats_in_table, name='get-seats'),
    path('api/seating/<int:seats_id>', api.delete_seating, name='delete-seating-api'),
    path('api/seat/list/<int:table_id>', api.seating_by_one_table,  name='seating'),
    # end api
]
