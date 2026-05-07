from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Property, RentalContract
from .serializers import PropertySerializer, RentalContractSerializer
from contracts.blockchain_service import BlockchainService
from django.utils import timezone

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def deploy_to_blockchain(self, request, pk=None):
        """Déployer un contrat blockchain pour cette propriété"""
        property_obj = self.get_object()
        blockchain = BlockchainService()
        
        # Vérifier si le contrat existe déjà
        if property_obj.blockchain_contract_address:
            return Response(
                {'error': 'Contrat blockchain déjà déployé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Déployer le contrat
        try:
            result = blockchain.deploy_contract(
                landlord_address=request.user.userprofile.eth_address,
                tenant_address=request.data.get('tenant_address'),
                monthly_rent=float(property_obj.price_per_month),
                deposit=float(property_obj.security_deposit),
                duration_months=request.data.get('duration_months', 12)
            )
            
            property_obj.blockchain_contract_address = result['contract_address']
            property_obj.save()
            
            return Response({
                'contract_address': result['contract_address'],
                'transaction_hash': result['tx_hash']
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RentalContractViewSet(viewsets.ModelViewSet):
    queryset = RentalContract.objects.all()
    serializer_class = RentalContractSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def sign_on_blockchain(self, request, pk=None):
        """Signer le contrat sur la blockchain"""
        contract = self.get_object()
        blockchain = BlockchainService()
        
        try:
            tx_hash = blockchain.sign_contract(
                contract_address=contract.blockchain_contract_address,
                tenant_private_key=request.user.userprofile.eth_private_key,
                deposit_amount=float(contract.security_deposit)
            )
            
            contract.status = 'ACTIVE'
            contract.signed_at = timezone.now()
            contract.blockchain_tx_hash = tx_hash
            contract.save()
            
            return Response({'transaction_hash': tx_hash})
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def pay_rent_blockchain(self, request, pk=None):
        """Payer le loyer via blockchain"""
        contract = self.get_object()
        blockchain = BlockchainService()
        
        try:
            tx_hash = blockchain.pay_rent(
                contract_address=contract.blockchain_contract_address,
                tenant_private_key=request.user.userprofile.eth_private_key,
                rent_amount=float(contract.monthly_rent)
            )
            
            return Response({'transaction_hash': tx_hash})
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )