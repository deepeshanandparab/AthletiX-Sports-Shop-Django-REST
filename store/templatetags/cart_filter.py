from django import template
from .currency_filter import inrcurrency, currency

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;


@register.filter(name='cart_quantity')
def cart_quantity(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0;


@register.simple_tag
def total_price(product, discount , cart):
    int_price = int(product.price * (1-discount/100)) * cart_quantity(product , cart)
    price = inrcurrency(int_price)
    return currency(price)


@register.filter(name='price_total')
def price_total(product, cart):
    return product.price * cart_quantity(product , cart)


@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    price = inrcurrency(sum)
    return currency(price)


@register.filter(name='checkout_cart_price')
def checkout_cart_price(products , cart):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    return int(sum)


@register.filter(name='checkout_taxes')
def checkout_taxes(products , cart):
    cart_price = checkout_cart_price(products , cart)
    gst = cart_price * 0.12
    cgst = cart_price * 0.12
    taxes = gst + cgst

    return int(taxes)


@register.filter(name='checkout_total')
def checkout_total(products , cart):
    total = checkout_cart_price(products , cart) + checkout_taxes(products , cart)
    return total
    

@register.simple_tag
def checkout_shipping_total(products , cart, shipping):
    total = checkout_cart_price(products , cart) + shipping
    price = inrcurrency(total)
    return currency(price)


@register.filter(name='cart_count')
def cart_count(cart):
    return len(cart)