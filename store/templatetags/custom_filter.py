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


@register.filter(name='or_sign')
def or_sign(value):
    value = value.replace('_', '/')
    return value.title()


@register.filter(name='new_line')
def new_line(value):
    value = value.replace(';', '')
    return value


@register.filter(name='desc_new_line')
def desc_new_line(value):
    value = value.replace(';', '\n\n')
    return value


@register.filter(name='split')
def split(value, key):
  return value.split(key)


@register.filter(name='toString')
def toString(value):
  string = str(value)
  return string


@register.filter(name='toInt')
def toInt(value):
  integer = int(value)
  return integer


@register.filter(name='size_lookup')
def size_lookup(dictionary, id):
    for key,value in dictionary:
        if str(key) == str(id):
            size = value['size']
    return size


@register.filter(name='color_lookup')
def color_lookup(dictionary, id):
    for key,value in dictionary:
        if str(key) == str(id):
            color = value['color']
    return color
