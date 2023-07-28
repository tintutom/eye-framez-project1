from django.urls import path
from . import views
urlpatterns = [
    
    path('place_order/',views.place_order,name='place_order'),
    path('order_summary/',views.order_summary,name='order_summary'),
    path('orderview/<int:id>',views.orderview,name='orderview'),
    path('order_cancel/<int:id>',views.order_cancel,name='order_cancel'),
    path('proceed_to_pay/',views.proceed_to_pay,name='proceed_to_pay'),
    path('order_status_change/',views.order_status_change,name='order_status_change'),
    path('return_order/<int:id>/',views.return_order,name='return_order'),
    path('accept_return/<int:id>/',views.accept_return,name='accept_return'),
    path('genericinvoice/<int:id>/',views.generateInvoice.as_view(), name = 'generateinvoice'),    

]