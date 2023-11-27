from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.db import transaction
from .models import Account, Transaction
import decimal
from .forms import TransactionForm, NewUserForm
from django.contrib.auth import login


# Form for handling transactions
class TransactionForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=10)
    type = forms.ChoiceField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal')])

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dashboard")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="bank/register.html", context={"register_form": form})

@login_required
def dashboard(request):
    account, created = Account.objects.get_or_create(user=request.user, defaults={'balance': decimal.Decimal('0.00')})
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['type']
            with transaction.atomic():
                if transaction_type == 'DEPOSIT' or (transaction_type == 'WITHDRAWAL' and account.balance >= amount):
                    Transaction.objects.create(account=account, amount=amount, type=transaction_type)
                else:
                    messages.error(request, 'Insufficient balance for withdrawal.')
                    return redirect('dashboard')
            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'bank/dashboard.html', {
        'account': account,
        'transactions': transactions,
        'form': form
    })
