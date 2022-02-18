from django.urls import path
from .import views


urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    ############################### PAYME ######################################
    path('card/create/', views.CardCreateApiView.as_view(), name='card_create'),
    path('card/verify/', views.CardVerifyApiView.as_view(), name='card_verify'),
    path('payment/', views.PaymentApiView.as_view(), name='payment'),
    ############################################################################
]


