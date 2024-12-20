from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Tender, Offer
from django.utils import timezone
from .serializers import TenderSerializer, OfferSerializer
import hashlib
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

abi = [
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "tenders",
      "outputs": [
        {
          "internalType": "bool",
          "name": "exists",
          "type": "bool"
        },
        {
          "internalType": "bytes32",
          "name": "dataHash",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tenderId",
          "type": "uint256"
        },
        {
          "internalType": "bytes32",
          "name": "dataHash",
          "type": "bytes32"
        }
      ],
      "name": "addTender",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tenderId",
          "type": "uint256"
        }
      ],
      "name": "getTenderHash",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
]

contract_address = "0x453F770dCCCF97182f8bA5d7ade3AC4F94f35dB8"

contract = w3.eth.contract(address=contract_address, abi=abi)

w3.eth.default_account = w3.eth.accounts[0]

class TenderCreateView(generics.CreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        if self.request.user.role != 'customer':
            raise PermissionDenied("Only customers can create tenders.")
        instance = serializer.save(created_by=self.request.user, status='active')
        data_str = instance.title + (instance.description or "")
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        data_hash_bytes = bytes.fromhex(data_hash)

        tx = contract.functions.addTender(instance.id, data_hash_bytes).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        instance.blockchain_tx = receipt.transactionHash.hex()
        instance.save()

class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'contractor':
            raise PermissionDenied("Only contractors can create offers.")

        instance = serializer.save(contractor=user)
        # Запись оффера в блокчейн
        # Сформируем хэш данных оффера (title и description берем у тендера, price - из оффера)
        data_str = f"{instance.tender.title}{instance.tender.description}{instance.price}"
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        data_hash_bytes = bytes.fromhex(data_hash)

        price_int = int(instance.price) # или привести к int, если price целочисленная. Если нет, умножить на 100. 
        # В Solidity uint256 - целочисленный. Если храните с точностью до 2 знаков, price * 100.
        
        tx = contract.functions.addOffer(instance.tender.id, data_hash_bytes, price_int).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        instance.blockchain_tx = receipt.transactionHash.hex()
        instance.save()

class TenderListView(generics.ListAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

class TenderProofView(generics.RetrieveAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

    def get(self, request, *args, **kwargs):
        tender = self.get_object()
        chain_hash = contract.functions.getTenderHash(tender.id).call()
        return Response({
            "tender_id": tender.id,
            "title": tender.title,
            "description": tender.description,
            "blockchain_tx": tender.blockchain_tx,
            "chain_hash": chain_hash.hex(),
            "status": tender.status
        })

class CloseTenderView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tender_id):
        try:
            tender = Tender.objects.get(id=tender_id)
        except Tender.DoesNotExist:
            return Response({"detail": "Tender not found"}, status=404)

        if tender.status == 'closed':
            return Response({"detail": "Tender already closed"}, status=400)

        if tender.end_date > timezone.now():
            return Response({"detail": "Tender end date not reached"}, status=400)

        offers = tender.offers.all()
        if not offers:
            winner_index = 0
        else:
            sorted_offers = sorted(offers, key=lambda o: o.price)
            winner_offer = sorted_offers[0]
            winner_index = list(offers).index(winner_offer)

        tx = contract.functions.closeTender(tender.id, winner_index).transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx)

        tender.status = 'closed'
        tender.save()

        return Response({
            "detail": "Tender closed successfully.",
            "winner_offer_id": offers[winner_index].id if offers else None,
            "tx": receipt.transactionHash.hex()
        })