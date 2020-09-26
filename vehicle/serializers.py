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
                  'color', 'vehicle_purpose', 'condition', 'is_new')


class VehicleListOfTypeSerializer(serializers.ModelSerializer):
    vehicles = SingleVehicleSerializer(source='vehicle', many=True)

    class Meta:
        model = VehicleType
        fields = ('vehicles',)
