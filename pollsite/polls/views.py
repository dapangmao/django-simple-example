from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.cache import cache_page

from django.http import HttpResponseRedirect
from .models import Question


@cache_page(60)
def index(request):
    last_five_questions = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_question_list': last_five_questions})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_id = request.POST.get('choice')
    if choice_id is None:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    selected_choice = question.choice_set.get(pk=choice_id)
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
