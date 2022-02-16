from django import template

register = template.Library()


@register.simple_tag
def filter_by_price(product_list, lower_price, higher_price):
    list = []
    for product in product_list:
        if product.price >= lower_price and product.price <= higher_price:
            list.append(product)
    return len(list)