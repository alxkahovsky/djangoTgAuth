from django.shortcuts import render


def auth_page(request):
    if not request.user.is_authenticated:
        return render(request, 'auth_telegram/auth_start.html')
    else:
        return render(request, 'auth_telegram/auth_start2.html', {'user': request.user})

