from django.http import HttpResponse
from django.shortcuts import render, redirect 
from .models import Question

# Create your views here.

def index(request):
    context = {}
    context['questions'] = Question.objects.all()
    return render(request, 'index.html', context)

def askquestion(request):
    if request.method == 'POST':
        try: 
            q = Question(question_title=title, question_text=question, posted_by=posted_by)
            title = request.POST.get('title')
            question = request.POST.get('question')
            posted_by = request.POST.get('posted_by')
            q.save()
            return redirect(viewquestion, q.qid, q.slug)
        except:
            return render(request, 'ask-question.html', {'error': 'something wrong with form'})
    else:
        return render(request, 'ask-question.html', {} )
