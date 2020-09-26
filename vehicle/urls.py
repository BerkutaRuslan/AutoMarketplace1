from django.urls import path

from vehicle.views import *
urlpatterns = [
    path('types', ListVehicleTypes.as_view()),
    path('types/<int:pk>', AllVehiclesOfType.as_view()),
    path('single_vehicle/<int:pk>', GetSingleVehicle.as_view()),
    path('vehicles/by', GetVehiclesByPrice.as_view()),
]