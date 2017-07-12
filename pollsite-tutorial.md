1. Modle layer
  - Django will create 10 additional tables besides the original two tables
  ![demo](https://github.com/dapangmao/django-simple-example/blob/master/images/Screen%20Shot%202017-07-12%20at%2010.40.17%20AM.png?raw=true)

  - Postgres connection
  ```
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pollsite',
        'USER': "",
        'PASSWORD': "",
        'HOST': 'localhost',
    }
}
```

2. The REPL for Django ORM


3. View layer 
```
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'index.html', {'latest_question_list': latest_question_list})


def result(request, question_id):
    res = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': res})


class DetailView(View):
    @staticmethod
    def get(request, question_id):
        try:
            res = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("No such thing")
        return render(request, 'detail.html', {'question': res})

    @staticmethod
    def post(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(question.id,)))
```

4. Router
```
from django.conf.urls import url
from django.contrib import admin

from polls import views

urlpatterns = [
    url(r'^polls/$', views.index, name='index'),
    url(r'^polls/(?P<question_id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^polls/(?P<question_id>[0-9]+)/results/$', views.result, name='results'),
    url(r'^admin/', admin.site.urls),
]
```
