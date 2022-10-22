from django.shortcuts import render
from django.http import HttpResponse
from store.models import Order, Product, Customer
from django.db.models import Value, F, Func, ExpressionWrapper


def say_hello(request):
    discounted_price = ExpressionWrapper(
        F('unit_price') * 0.8, output_field=DecimalField()
    )
    queryset = Customer.objects.annotate(
        discounted_price=discounted_price
    )
    return render(request, 'hello.html', {'name': 'Mosh', 'products': queryset})
