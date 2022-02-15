from django.shortcuts import render

def HomePage(request):
    context = {'title':'Home'}
    return render(request, 'index.html', context)
