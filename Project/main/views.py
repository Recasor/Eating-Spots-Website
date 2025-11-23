from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def item(request):
    return render(request, 'main/item.html')


def canteen_1(request):
    return render(request, 'main/Pages_of_canteens/canteen_1.html')


def canteen_2(request):
    return render(request, 'main/Pages_of_canteens/canteen_2.html')


def canteen_3(request):
    return render(request, 'main/Pages_of_canteens/canteen_3.html')


def canteen_4(request):
    return render(request, 'main/Pages_of_canteens/canteen_4.html')



def canteen_5(request):
    return render(request, 'main/Pages_of_canteens/canteen_5.html')




