from django.urls import path
from . import views
urlpatterns = [


    path('view_address/',views.view_address,name='view_address'),
    path('add_address/',views.add_address,name='add_address'),
    # path('add_address/<str:return_url>/', views.add_address, name='add_address'),
    path('edit_address/<int:id>/',views.edit_address,name='edit_address'),
    path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),

]

