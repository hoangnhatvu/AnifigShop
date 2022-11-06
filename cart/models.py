from account.models import Account
from django.db import models

from product.models import Product


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    def sub_total(self):
        if self.product.sale_price > 0:
            return self.quantity * self.product.sale_price
        else:
            return self.quantity * self.product.price

    def __unicode__(self):
        return self.product
