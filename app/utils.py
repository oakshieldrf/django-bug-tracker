from django.shortcuts import render 


def error404View(request, exception):

    return render(request, "page-404.html", status=404)