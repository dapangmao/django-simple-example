- URL
```python

from django.conf.urls import url
import views

urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', view.Placeholder.as_view(),
        name='placeholder'),
    url(r'^$', view.index, name='homepage'),
)
```

- Setting

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

- Template

```python
{% load staticfiles %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Django Placeholder Images</title>
    <link rel="stylesheet" href="{% static 'site.css' %}" type="text/css">
</head>
<body>
    <h1>Django Placeholder Images</h1>
    <p>This server can be used for serving placeholder
    images for any web page.</p>
    <p>To request a placeholder image of a given width and height
    simply include an image with the source pointing to
    <b>/image/&lt;width&gt;x&lt;height&gt;/</b>
    on this server such as:</p>
    <pre>
        &lt;img src="{{ example }}" &gt;
    </pre>
    <h2>Examples</h2>
    <ul>
        <li><img src="{% url 'placeholder' width=50 height=50 %}"></li>
        <li><img src="{% url 'placeholder' width=100 height=50 %}"></li>
        <li><img src="{% url 'placeholder' width=50 height=100 %}"></li>
    <ul>
</body>
</html>
```


- View

```python

from django.core.cache import cache
from io import BytesIO
from PIL import Image, ImageDraw
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag
from django.views import View
import hashlib


class Placeholder(View):
    def generate(self, height, width, image_format='PNG'):
        """Generate an image of the given type and return as raw bytes."""
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content is not None:
            return content
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
        cache.set(key, content, 60 * 60)
        return content

    @staticmethod
    def generate_etag(request, width, height):
        content = 'Placeholder: {0} x {1}'.format(width, height)
        return hashlib.sha1(content.encode('utf-8')).hexdigest()

    @etag(self.generate_etag)
    def get(self, request, width, height):
        try:
            w = int(width)
            h = int(height)
        except ValueError:
            return HttpResponseBadRequest('Invalid Image Request [must be digits]')
        if w <= 0 or h <= 0:
            return HttpResponseBadRequest('Invalid Image Request [cannot be below zero]')
        image = self.generate(height=h, width=w)
        return HttpResponse(image, content_type='image/png')

def index(request):
    context = {
        'example': request.build_absolute_uri(reverse('placeholder', kwargs={'width': 50, 'height':50}))
    }
    return render(request, 'home.html', context)
```
