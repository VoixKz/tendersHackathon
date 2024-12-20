from rest_framework import serializers
from .models import Tender, Offer

class OfferSerializer(serializers.ModelSerializer):
    contractor = serializers.ReadOnlyField(source='contractor.username')

    class Meta:
        model = Offer
        fields = ['id', 'tender', 'contractor', 'price', 'comment', 'created_at', 'blockchain_tx']
        read_only_fields = ['id', 'contractor', 'created_at', 'blockchain_tx']

class TenderSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Tender
        fields = ('id', 'title', 'description', 'price', 'start_date', 'end_date', 'created_by', 'created_at', 'blockchain_tx', 'status', 'offers', 'tag', 'type')
        read_only_fields = ('id', 'created_by', 'created_at', 'blockchain_tx', 'status', 'offers')