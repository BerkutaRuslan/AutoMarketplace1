from rest_framework import serializers

from vehicle.models import VehicleType, SingleVehicle


class VehicleTypeSerializer(serializers.ModelSerializer):
    amount_of_vehicles = serializers.SerializerMethodField()

    class Meta:
        model = VehicleType
        fields = ('id', 'name', 'photo', 'description', 'amount_of_vehicles')

    def get_amount_of_vehicles(self, obj):
        return obj.vehicle.count()


class SingleVehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SingleVehicle
        fields = ('name', 'photo', 'description', 'price', 'year', 'horse_power', 'engine_cc',
                  'color', 'vehicle_appointment', 'condition', 'is_new')


class VehicleListOfTypeSerializer(serializers.ModelSerializer):
    vehicles = SingleVehicleSerializer(source='vehicle', many=True)

    class Meta:
        model = VehicleType
        fields = ('vehicles',)


class GetVehiclesByPriceSerializer(serializers.ModelSerializer):
    vehicle_price_range = serializers.SerializerMethodField()

    class Meta:
        model = SingleVehicle
        fields = ['vehicle_price_range']

    def get_vehicle_price_range(self):
        price_from = int(self.context.get('price_from'))
        price_to = int(self.context.get('price_to'))
        matched_vehicle_by_price = SingleVehicle.objects.filter(price__range=[price_from, price_to])
        return str(matched_vehicle_by_price)


