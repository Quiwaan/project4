from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect 
from qa.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json, markdown2, bleach

# Create your views here.

def index(request):
    context = {}
    context['questions'] = Question.objects.all()
    return render(request, 'index.html', context)

def askquestion(request):
    if request.method == 'POST':
        try: 
            user = request.user
            title = request.POST.get('title')
            question = request.POST.get('question')
            posted_by = request.POST.get('posted_by')
            q = Question(question_title=title, question_text=question, posted_by=posted_by, user=request.user)
            print(title, question, posted_by)
            q.save()
            return redirect(showquestion, q.qid, q.slug)
        except Exception as e:
            return render(request, 'ask-question.html', {'error': 'something wrong with form'})
    else:
        return render(request, 'ask-question.html', {})

def showquestion(request, qid, qslug):
    context = {}
    question = Question.objects.get(qid=qid, slug=qslug)

    question_json = json.loads(serializers.serialize('json', [question])) [0] ['fields']
    question_json['qid'] = question.qid
    question_json['date_posted'] = question.date_posted
    question_json['question_text'] = bleach.clean(markdown2.markdown(question_json['question_text']), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
    context['question'] = question_json
    context['answers'] = []
    answers = Answer.objects.filter(qid=qid)
    for answer in answers:
        answer.answer_text = bleach.clean(markdown2.markdown(answer.answer_text), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
        context['answers'].append(answer)
    return render(request, 'show-question.html', context)