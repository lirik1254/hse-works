from django.shortcuts import render


def main(request):
    return render(request, 'static_pages/main.html')
