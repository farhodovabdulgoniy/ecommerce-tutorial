from django.db import models
from accounts.models import Account


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
    status = models.CharField(max_length=10, default=PROCESS, choices=STATUS)
    create_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)

    def update_transaction(self, trans_id, status):
        trans = Transaction.objects.get(trans_id=trans_id)
        trans.status = status
        trans.save()

    def __str__(self):
        return self.trans_id