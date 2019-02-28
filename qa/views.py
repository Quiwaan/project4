from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect 
from qa.models import *
from django.contrib.auth.models import User
from django.contrib import auth
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

def showquestion(request, qslug, qid):
    context = {}
    question = Question.objects.get(qid=qid, slug=qslug)
    print(qid, qslug)

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

def answerquestion(request):
    if request.method == 'POST':
        # try: 
            user = request.user
            answer = request.POST['answer']
            posted_by = request.POST['posted_by']
            qid = request.POST['qid_id']
            slug = request.POST['slug']
            print(answer, posted_by, qid, slug )
            
            a = Answer(answer_text=answer, posted_by=posted_by, user=request.user, qid=Question.objects.get(qid=qid))
            a.save()
            return redirect('showquestion', qid=qid, qslug=slug )
        # except Exception as e:
        #     return render(request, 'show-question.html', {'error': 'something wrong with form'})
    else:
        return render(request, 'show-question.html', {})

def profile(request, username):
    user = User.objects.get(username=username)
    answer = Answer.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'answer': answer})

def login(request):
	context = {'error':False}
	if request.method == 'GET':
		return render(request, 'login.html')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			return HttpResponseRedirect(reverse('polls:index'))
		except:
			context['error'] = 'Invalid Login Credentials'
			return render(request, 'login.html', context)

def signup(request):
	context = {'error':False}
	if request.method == 'GET':
		return render(request, 'polls/signup.html', context)
	if request.method == 'POST':
		print(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = User.objects.create_user(username=username, password=password)
			auth.login(request, user)
			return HttpResponseRedirect(reverse('polls:index'))
		except:
			context['error'] = f"Username '{username}' already exists."
			return render(request, 'polls/signup.html', context)

def login(request):
	context = {'error':False}
	if request.method == 'GET':
		return render(request, 'polls/login.html')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		try:
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			return HttpResponseRedirect(reverse('polls:index'))
		except:
			context['error'] = 'Invalid Login Credentials'
			return render(request, 'polls/login.html', context)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('polls:login'))
                