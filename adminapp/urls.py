from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.admin_login,name='adminlogin'),
    path('dashboard/',views.admin_home,name='admin-home'),
    path('logout',views.admin_logout,name='logout'),
    # User Managment
    path('users/',views.show_users,name='users'),
    path('block-user/<int:id>/',views.block_user,name='block-user'),
    # Category Managment
    path('category/',views.category,name='category'),
    path('addcategory/',views.add_category,name='addcategory'),
    path('editcategory/<int:id>/',views.edit_category,name='editcategory'),
    path('deletecategory/<int:id>/',views.delete_category,name='deletecategory'),

    path('subcategory/',views.subcategory,name='subcategory'),
    path('addsubcategory/',views.add_subcategory,name='addsubcategory'),
    path('editsubcategory/<int:id>/',views.edit_subcategory,name='editsubcategory'),
    path('deletesubcategory/<int:id>/',views.delete_subcategory,name='deletesubcategory'),

    path('products/',views.products,name='products'),
    path('addingproduct',views.adding_product,name='addingproduct'),
    path('editproduct/<int:id>/',views.edit_product,name='editproduct'),
    path('addproduct/',views.add_product,name='addproduct'),
    path('subcataddproduct/<int:catid>/',views.load_subcategory,name='load-subcategory'),
    path('editsubcataddproduct/<int:catid>/',views.editload_subcategory,name='editload-subcategory'),
    path('deleteproduct/<int:id>/',views.delete_product,name='deleteproduct'),
    
    # Product Variation
    path('add_color/',views.add_color,name='add_color'),
    path('variations/',views.variations,name='variations'),
    path('add_variations/<int:id>/',views.add_variations,name='add_variations'),
    # path('product-list', views.product_list, name='product_list'),

    # Order Managment
    path('order_items/',views.order_items,name='order_items'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),

    # path('genericinvoice/<int:id>/',views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    # Offer Managment
    path('category_offer',views.category_offer,name='category_offer'),
    path('add_category_offer',views.add_category_offer,name='add_category_offer'),
    path('edit_category_offer/<int:id>/',views.edit_category_offer,name='edit_category_offer'),
    path('delete_category_offer/<int:id>/',views.delete_category_offer,name='delete_category_offer'),
    
    path('subcategory_offer',views.subcategory_offer,name='subcategory_offer'),
    path('add_subcategory_offer',views.add_subcategory_offer,name='add_subcategory_offer'),
    path('edit_subcategory_offer/<int:id>/',views.edit_subcategory_offer,name='edit_subcategory_offer'),
    path('delete_subcategory_offer/<int:id>/',views.delete_subcategory_offer,name='delete_subcategory_offer'),

    path('product_offer',views.product_offer,name='product_offer'),
    path('add_product_offer',views.add_product_offer,name='add_product_offer'),
    path('edit_product_offer/<int:id>/',views.edit_product_offer,name='edit_product_offer'),
    path('delete_product_offer/<int:id>/',views.delete_product_offer,name='delete_product_offer'),

    path('coupons/',views.coupons,name='coupons'),
    path('add_coupons/',views.add_coupons,name='add_coupons'),
    path('edit_coupons/<int:id>/',views.edit_coupons,name='edit_coupons'),
    path('delete_coupons/<int:id>/',views.delete_coupons,name='delete_coupons'),
    # Report
    path('product_report/',views.product_report,name='product_report'),
    path('product_csv/',views.product_csv,name='product_csv'),
    path('generateProductPdf',views.generateProductPdf.as_view(),name='generateProductPdf'),
    path('product_excel',views.product_excel,name='product_excel'),

    path('salesReport/',views.salesReport,name='salesReport'),
    path('by_date/',views.by_date,name='by_date'),
    path('generatesalesReportPdf',views.generatesalesReportPdf.as_view(),name='generatesalesReportPdf'),
    path('by_month/',views.by_month,name='by_month'),
    path('by_year/',views.by_year,name='by_year'),
    path('download_docx',views.download_docx,name='download_docx'),
    
   
]
