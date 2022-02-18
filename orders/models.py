from django.db import models
from accounts.models import Account
from store.models import Product,Variation


class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=60)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150,blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100,blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(choices=STATUS,default='New',max_length=50)
    ip = models.CharField(max_length=20,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.user.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation,on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name


######################################### PAYME #############################################


class Transaction(models.Model):
    PROCESS = 0
    PAID = 1
    FAILED = 2
    STATUS = (
        (PROCESS, 'processing'),
        (PAID, 'paid'),
        (FAILED, 'failed'), 
    )

    trans_id = models.CharField(max_length=255)
    request_id = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    account = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, default=PROCESS, choices=STATUS)
    create_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(auto_now=True)

    def create_transaction(self, trans_id, request_id, amount, account, status):
        Transaction.objects.create(
            trans_id=trans_id,
            request_id=request_id,
            amount=amount / 100,
            account=account,
            status=status
        )

    def update_transaction(self, trans_id, status):
        trans = Transaction.objects.get(trans_id=trans_id)
        trans.status = status
        trans.save()