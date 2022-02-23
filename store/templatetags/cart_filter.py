import re
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


#-------------------------- Cart Price with Coupon Code -----------------------#
@register.simple_tag
def checkout_cart_total(products , cart, coupon_code):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    invalid = 'Invalid Coupon Code or already expired code.'
    if coupon_code:
        if invalid in coupon_code.values():
            cart_total = inrcurrency(int(sum))
            return currency(cart_total)
        elif coupon_code:
                sum = sum * (1 - coupon_code[0].discount/100)
                cart_total = inrcurrency(int(sum))
                return currency(cart_total)
    else: 
        cart_total = inrcurrency(int(sum))
        return currency(cart_total)


@register.simple_tag
def checkout_coupon_cart_total(products , cart, coupon_code):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    invalid = 'Invalid Coupon Code or already expired code.'
    if coupon_code:
        if invalid in coupon_code.values():
            return int(sum)
        elif coupon_code:
                sum = sum * (1 - coupon_code[0].discount/100)
                return int(sum)
    else: 
        return int(sum)

#-------------------------------------------------------------------#

@register.simple_tag
def total_discount(products , cart, coupon_code):
    sum = 0
    discount = 0
    for p in products:
        sum += price_total(p , cart)
    
    total_cost = sum

    invalid = 'Invalid Coupon Code or already expired code.'
    if coupon_code:
        if invalid in coupon_code.values():
            saved = total_cost - sum
            discount = inrcurrency(int(saved))
            return currency(discount)
        elif coupon_code:
                sum = sum * (1 - coupon_code[0].discount/100)
                saved = total_cost - sum
                discount = inrcurrency(int(saved))
                return currency(discount)
    else: 
        saved = total_cost - sum
        discount = inrcurrency(int(saved))
        return currency(discount)

        


    


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
def checkout_shipping_total(products , cart, coupon_code, shipping):
    total = checkout_coupon_cart_total(products , cart, coupon_code) + shipping
    price = inrcurrency(total)
    return currency(price)


@register.filter(name='cart_count')
def cart_count(cart):
    return len(cart)