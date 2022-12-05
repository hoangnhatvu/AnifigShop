from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:description>', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]