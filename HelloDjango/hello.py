import sys


from django.conf import settings


settings.configure(
    DEBUG=True,
    SECRET_KEY='thisisasecretkey',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleWare',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)


from django.conf.urls import url
from django.http import HttpResponse


#  views.py
def index(request):
    return HttpResponse('Hello World!')


#  urls.py
urlpatterns = (
    url("", index),
)


if __name__=="__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
