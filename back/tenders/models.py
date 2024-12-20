from django.db import models
from django.conf import settings

class Tender(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tag = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tenders')
    created_at = models.DateTimeField(auto_now_add=True)
    blockchain_tx = models.CharField(max_length=66, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title

class Offer(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='offers')
    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contractor_offers')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    blockchain_tx = models.CharField(max_length=66, blank=True, null=True)

    def __str__(self):
        return f"Offer by {self.contractor} on {self.tender}"