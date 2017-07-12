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
from django.http import Http404
from django.views import View

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'index.html', {'latest_question_list': latest_question_list})


class DetailView(View):
    template_name = 'detail.html'

    def get(self, request, question_id, is_result=False):
        try:
            res = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("No such thing")
        return render(request, self.template_name, {'question': res, 'is_result': is_result})

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, self.template_name, {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        selected_choice.votes += 1
        selected_choice.save()
        return self.get(request, question_id, True)

        
```

4. Router

```html
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

5. Template layer

```html
{% extends "base.html" %}

{% block content %}
    <h1>{{ question.question_text }}</h1>

    {% if error_message %} <p><strong>{{ error_message }}</strong></p> {% endif %}

    {% if is_result %}
        <ul>
            {% for choice in question.choice_set.all %}
                <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
            {% endfor %}
        </ul>
        <a href="{% url 'detail' question.id %}">Vote again?</a>

    {% else %}
        <form action="{% url 'detail' question.id %}" method="post">
            {% csrf_token %}
            {% for choice in question.choice_set.all %}
                <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}"/>
                <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br/>

            {% endfor %}

            <input type="submit" value="Vote"/>

        </form>
    {% endif %}
{% endblock %}
```
