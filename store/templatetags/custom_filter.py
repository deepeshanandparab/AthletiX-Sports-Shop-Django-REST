from django import template

register = template.Library()


@register.simple_tag
def filter_by_price(product_list, lower_price, higher_price):
    list = []
    for product in product_list:
        if product.price >= lower_price and product.price <= higher_price:
            list.append(product)
    return len(list)


@register.filter(name='filter_by_category')
def filter_by_category(product_list, type):
    list = []
    for product in product_list:
        if product.type == type:
             list.append(product)
    return len(list)


@register.filter(name='readable_text')
def readable_text(value):
    value = value.replace('_', ' ')
    return value.title()


@register.filter(name='new_line')
def new_line(value):
    value = value.replace(';', '')
    return value


@register.filter(name='split')
def split(value, key):
  return value.split(key)
