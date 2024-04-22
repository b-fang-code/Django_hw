from django.shortcuts import render
from django.http import HttpResponse


def main(request):
    html = """
    <html>
        <body>
            <h1>Это главная страница моего первого Django-сайта</h1>
        </body>
    </html>
    """
    return HttpResponse(html)


def about(request):
    html = html = """
    <html>
        <body>
            <h1>Меня зовут Павел. Я изучаю Django</h1>
        </body>
    </html>
    """
    return HttpResponse(html)
