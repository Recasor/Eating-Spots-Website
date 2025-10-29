from django.shortcuts import render
from django.http import HttpResponse


def canteen(request):
    return render(request, 'main/canteen.html')


def menu(request):
    return render(request, 'main/menu.html')


def reviews(request):
    return render(request, 'main/reviews.html')


def settings(request):
    return render(request, 'main/settings.html')


def profile(request):
    return render(request, 'main/profile.html')


def exit(request):
    return render(request, 'main/exit.html')


def scam(request):
    return render(request, 'main/scam.html')


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



