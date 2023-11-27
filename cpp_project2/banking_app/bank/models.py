from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db import transaction

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Account"

    def update_balance(self, amount, transaction_type):
        amount = Decimal(amount)
        if transaction_type == 'DEPOSIT':
            self.balance += amount
        elif transaction_type == 'WITHDRAWAL':
            if self.balance >= amount:
               self.balance -= amount
            else:
            # Handle the case where there is not enough balance
            # You can raise an exception or handle it as per your requirement
                print("Not enough balance to perform the withdrawal.")
        self.save()

class Transaction(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.type} of {self.amount} on {self.timestamp}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Check if the object is being created by seeing if it has an ID set
            is_new = self._state.adding 
            if is_new:
                # Save the transaction first
                super(Transaction, self).save(*args, **kwargs)
                # Then update the account balance
                self.account.update_balance(self.amount, self.type)
            else:
                # If the transaction is not new, just save it normally
                super(Transaction, self).save(*args, **kwargs)

# Signal to create an Account automatically when a User is created
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

# Signal to save the Account when the User is saved
# This signal is not necessary if you're just creating the account and not updating it
# directly from the User model. You can remove this if you're not using it.
#@receiver(post_save, sender=User)
#def save_user_account(sender, instance, **kwargs):
#    instance.account.save()
