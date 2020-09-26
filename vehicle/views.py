from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from vehicle.models import VehicleType, SingleVehicle
from vehicle.serializers import VehicleTypeSerializer, VehicleListOfTypeSerializer, SingleVehicleSerializer


class ListVehicleTypes(generics.ListAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        """
        Url for retrieving all vehicle types
        """
        return super().get(request, args, kwargs)


class AllVehiclesOfType(generics.RetrieveAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleListOfTypeSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        """
        Url for retrieving all vehicles, in vehicle type
        """
        return super().get(request, args, kwargs)


class GetSingleVehicle(generics.RetrieveAPIView):
    queryset = SingleVehicle.objects.all()
    serializer_class = SingleVehicleSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        """
        Url for retrieving single vehicle
        """
        return super().get(request, args, kwargs)


class GetVehiclesByPrice(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_id="Get Vehicle by price",
        operation_description="Accepts query params, ?price_from=, ?price_to=,"
                              "vehicle_purpose(Road/Water/Air), you can combine price+purpose or filter only by price",
        security=[],
        tags=['vehicle']
    )
    def get(self, request):
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        vehicle_purpose = self.request.query_params.get('vehicle_purpose')
        if vehicle_purpose:
            queryset = SingleVehicle.objects.filter(price__range=[price_from, price_to],
                                                    vehicle_purpose=vehicle_purpose)
        else:
            queryset = SingleVehicle.objects.filter(price__range=[price_from, price_to])

        matching_vehicle_by_price = []
        if queryset:
            for vehicle in queryset:
                matching_vehicle_by_price.append({
                    "name": vehicle.name,
                    "price": vehicle.price,
                    "year": vehicle.year,
                    "horse_power": vehicle.horse_power,
                    "engine_cc": vehicle.engine_cc,
                    "color": vehicle.color,
                    "vehicle_purpose": vehicle.vehicle_purpose,
                    "vehicle_condition": vehicle.condition,
                    "is_new": vehicle.is_new,
                })
            return Response({"vehicles": matching_vehicle_by_price}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "There are no vehicles in that price range"}, status=status.HTTP_404_NOT_FOUND)
