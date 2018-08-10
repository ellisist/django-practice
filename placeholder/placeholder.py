import os
import sys
import hashlib
from io import BytesIO
from PIL import Image, ImageDraw
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.core.cache import cache  # The backend cache system can be changed with CACHES setting
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag
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

    def generate(self, image_format="PNG"):
        """generate an image of the given type and return as raw bytes"""
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(height, width, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255))
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
        return content


#  views.py
def generate_etag(request, width, height):
    content = 'Placeholder: {} x {}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(generate_etag)
def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type="image/png")
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
