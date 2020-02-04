from django.urls import path, include
from rest_framework.routers import DefaultRouter

from staff import views


router = DefaultRouter()
router.register('staffs', views.StaffViewSet)

app_name = 'staff'

urlpatterns = [
    path('', include(router.urls))
]
