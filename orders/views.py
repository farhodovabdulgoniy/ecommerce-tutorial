from django.shortcuts import redirect, render
from carts.models import CartItem
from orders.models import Order
from .forms import OrderForm
import datetime
from orders.models import Transaction
import requests
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.serializers import SubscribeSerializer
from orders.config import *


def payments(request):
    return render(request,'orders/payments.html')


def place_order(request,total=0,quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')
        

class PaymentApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['params']['token']
        result = self.receipts_create(token, serializer.validated_data)
        return Response(result)

    def receipts_create(self, token, validated_data):
        print(validated_data)
        key_2 = validated_data['params']['account'][KEY_2] if KEY_2 else None
        data = dict(
            id=validated_data['id'],
            method='receipts.create',
            params=dict(
                amount=validated_data['params']['amount'],
                account=dict(
                    KEY_1=validated_data['params']['account'][KEY_1],
                    KEY_2=key_2,
                )
            )
        )
        print(AUTHORIZATION_PAY)
        response = requests.post(URL, json=data, headers=AUTHORIZATION_PAY)
        print('response', response)
        result = response.json()
        print(result)

        if 'error' in result:
            return result

        trans_id = result['result']['receipt']['_id']
        trans = Transaction()
        print(result)
        trans.create_transaction(
            trans_id=trans_id,
            request_id=result['id'],
            amount=result['result']['receipt']['amount'],
            account=result['result']['receipt']['account'],
            status=trans.PROCESS,
        )
        result = self.receipts_pay(trans_id, token)
        return result

    def receipts_pay(self, trans_id, token):
        data = dict(
            method='receipts.pay',
            params=dict(
                id=trans_id,
                token=token,
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_PAY)
        result = response.json()
        trans = Transaction()

        if 'error' in result:
            trans.update_transaction(
                trans_id=trans_id,
                status=trans.FAILED,
            )
            return result

        trans.update_transaction(
            trans_id=result['result']['receipt']['_id'],
            status=trans.PAID,
        )

        return result


class CardCreateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_create(serializer.validated_data)
        print('post : ', result)
        return Response(result)

    def card_create(self, validated_data):
        print('cart_create_validate :', validated_data)
        data = dict(
            id=validated_data['id'],
            method='cards.create',
            params=dict(
                card=dict(
                    number=validated_data['params']['card']['number'],
                    expire=validated_data['params']['card']['expire'],
                ),
                # amount=validated_data['params']['amount'],
                save=validated_data['params']['save']
            )
        )
        print('data', data)
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CARD)
        result = response.json()
        if 'error' in result:
            return result

        token = result['result']['card']['token']
        result = self.card_get_verify_code(token)

        return result

    def card_get_verify_code(self, token):
        data = dict(
            method='cards.get_verify_code',
            params=dict(
                token=token
            )
        )

        print('verify code:', data)
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CARD)
        result = response.json()
        if 'error' in result:
            return result

        result.update(token=token)
        print(result)
        return result


class CardVerifyApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_verify(serializer.validated_data)

        return Response(result)

    def card_verify(self, validated_data):
        data = dict(
            id=validated_data['id'],
            method='cards.verify',
            params=dict(
                token=validated_data['params']['token'],
                code=validated_data['params']['code']
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CARD)
        result = response.json()

        return result
