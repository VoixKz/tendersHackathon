from django.urls import path
from .views import (
    TenderListView, 
    TenderCreateView, 
    TenderProofView, 
    OfferListCreateView, 
    CloseTenderView
)

urlpatterns = [
    path('', TenderListView.as_view(), name='tender-list'),
    path('create/', TenderCreateView.as_view(), name='tender-create'),
    path('<int:pk>/proof/', TenderProofView.as_view(), name='tender-proof'),

    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    
    path('<int:tender_id>/close/', CloseTenderView.as_view(), name='tender-close'),
]