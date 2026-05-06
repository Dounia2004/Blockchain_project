from django.db import models
from django.contrib.auth.models import User
import uuid

class Property(models.Model):
    PROPERTY_TYPES = [
        ('APARTMENT', 'Appartement'),
        ('HOUSE', 'Maison'),
        ('COMMERCIAL', 'Local commercial'),
        ('LAND', 'Terrain'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('RENTED', 'Loué'),
        ('MAINTENANCE', 'En maintenance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='France')
    surface_area = models.FloatField(help_text="Surface en m²")
    rooms = models.IntegerField()
    bedrooms = models.IntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    blockchain_contract_address = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Properties"

class RentalContract(models.Model):
    CONTRACT_STATUS = [
        ('DRAFT', 'Brouillon'),
        ('PENDING', 'En attente signature'),
        ('ACTIVE', 'Actif'),
        ('COMPLETED', 'Terminé'),
        ('TERMINATED', 'Résilié'),
        ('DISPUTED', 'En litige'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='contracts')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_contracts')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS, default='DRAFT')
    
    # Informations blockchain
    blockchain_contract_address = models.CharField(max_length=200, blank=True, null=True)
    blockchain_tx_hash = models.CharField(max_length=200, blank=True, null=True)
    
    # Documents
    contract_pdf = models.FileField(upload_to='contracts/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    signed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Contrat {self.property.title} - {self.tenant.username}"