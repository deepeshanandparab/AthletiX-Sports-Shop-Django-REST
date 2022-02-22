from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)


def stringToList(string):
    list=[]
    list[:0]=string
    return list

def listToString(s): 
    string= "" 
    for ele in s: 
        string += ele  
    return string 


@register.filter(name='inrcurrency')
def inrcurrency(number):
    num = str(number)
    list = stringToList(num)
    if len(list) <= 3:
        value = listToString(list)
        return value
    elif len(list) > 3 and len(list) < 5:
        list.insert(1, ",")
        value = listToString(list) # value = 1,000
        return value
    elif len(list) == 5:
        list.insert(2, ",")
        value = listToString(list) # value = 1,000
        return value  
    elif len(list) > 5 and len(list) <= 7:
        list.insert(1, ",")
        list.insert(4,",")
        value = listToString(list) # value = 1,00,000
        return value
    elif len(list) > 7 and len(list) <= 9:
        list.insert(1, ",")
        list.insert(4,",")
        list.insert(7,",")
        value = listToString(list) # value = 1,00,00,000
        return value
    else:
        value = listToString(list)
        return value
      

@register.filter(name='overall_rating')
def overall_rating(rating_list, product):
    sum = 0
    ratings_count = 0
    for r in rating_list:
        if r.product.id == product.id:
            sum += r.rating
            ratings_count += 1

    if ratings_count > 0:
        ovr_rating = float(sum)/ratings_count
        rating = round(ovr_rating * 2) / 2
    else:
        ovr_rating = float(sum)
        rating = round(ovr_rating * 2) / 2
    return rating


@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1


@register.filter(name='discountedprice')
def discountedprice(price , discount):
    return int(price * (1 - discount/100))


