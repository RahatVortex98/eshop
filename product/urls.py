
from django.urls import path
from .import views

urlpatterns = [
    path('products/', views.get_product,name="product"),
    path('products/new/', views.new_product,name="new_product"),
    path('products/images/', views.upload_images,name="upload_images"),
    path('products/<str:pk>/', views.get_product_individual,name="product_detail"),
    path('products/<str:pk>/update/',views.update_product,name="update_product"),
    path('products/<str:pk>/delete/',views.delete_product,name="delete_product"),
   

    path('<str:pk>/reviews/',views.create_review,name="create_update_review"),
    path('<str:pk>/reviews/delete/',views.delete_review,name="delete_review"),
    
]
