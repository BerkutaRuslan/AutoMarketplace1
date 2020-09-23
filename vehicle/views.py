from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from vehicle.models import VehicleType, SingleVehicle
from vehicle.serializers import VehicleTypeSerializer, VehicleListOfTypeSerializer, SingleVehicleSerializer, \
    GetVehiclesByPriceSerializer


class ListVehiclyTypes(generics.ListAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = (AllowAny,)


class AllVehiclesOfType(generics.RetrieveAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleListOfTypeSerializer
    permission_classes = (AllowAny,)


class GetSingleVehicle(generics.RetrieveAPIView):
    queryset = SingleVehicle.objects.all()
    serializer_class = SingleVehicleSerializer
    permission_classes = (AllowAny,)


class GetVehiclesByPrice(APIView):
    serializer_class = GetVehiclesByPriceSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        vehicle_appointment = self.request.query_params.get('vehicle_appointment')
        queryset = SingleVehicle.objects.filter(price__range=[price_from, price_to],
                                                vehicle_appointment=vehicle_appointment)
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
                    "vehicle_appointment": vehicle.vehicle_appointment,
                    "vehicle_condition": vehicle.condition,
                    "is_new": vehicle.is_new,
                })
            return Response({"matching vehicles": matching_vehicle_by_price}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "There are no vehicles in that price range"}, status=status.HTTP_404_NOT_FOUND)
