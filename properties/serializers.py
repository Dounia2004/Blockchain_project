from rest_framework import serializers
from .models import Property, RentalContract

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'blockchain_contract_address')

class RentalContractSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    
    class Meta:
        model = RentalContract
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'blockchain_contract_address', 'blockchain_tx_hash')