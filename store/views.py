from django.shortcuts import render

def StorePage(request):
    context = {'title':'Store'}
    return render(request, 'store.html', context)


def ProductDetailPage(request):
    context = {'title':'Product Detail'}
    return render(request, 'product-detail.html', context)
