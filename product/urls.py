from django.urls import path
from . import views
urlpatterns = [
    path('search/<str:description>', views.search, name='search'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
