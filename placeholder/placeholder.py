import os
import sys
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django import forms

#  settings.py

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY', 'z%is7)hp93!7lf@)#aojs70f@rg4bf$9a3adplvr$ad=!rq$zt')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleWare',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)


#  forms.py
class ImageForm(forms.Form):
    """Form to validate requested placeholder image"""

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)


#  views.py
def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']
        # TODO: generate image of requested size
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Invalid Image Request')


def index(request):
    return HttpResponse('Hello World!')


#  urls.py
urlpatterns = (
    path("image/<int:width>x<int:height>/", placeholder, name="placeholder"),
    path("", index, name="homepage"),
)


application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
