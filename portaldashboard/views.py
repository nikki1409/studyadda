from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .forms import *
from django . contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django .contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method=="POST":
        form=NoteForm(request.POST)
        if form.is_valid():
            notes=Note(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} Successfully!!!")
    else:
        form=NoteForm()
    notes=Note.objects.filter(user=request.user)
    context={'notes': notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def deletenote(request,pk=None):
    Note.objects.get(id=pk).delete()
    messages.success(request,f"Notes deleted from {request.user.username} Successfully!!!")
    return redirect("notes")


#class NoteDetailView(generic.DetailView):
 #   model=Note


def detail(request,pk=None):
    notes=Note.objects.filter(id=pk)
    context={'notes': notes}
    return render(request,'dashboard/notes_detail.html',context)

@login_required
def homework(request):
    if request.method=="POST":
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False

            homework=Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],
                                description=request.POST['description'],due=request.POST['due'],is_finished=finished)

            homework.save()
            messages.success(request,f"Homework added from {request.user.username} Successfully!!!")

    else:
        form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done=True
    else:
        homework_done=False
    context={'homeworks':homework,'homework_done':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context)


@login_required
def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method == "POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']

            }

            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,"dashboard/youtube.html",context)

    else:
        form=DashboardForm()
    context= {'form':form}
    return render(request,"dashboard/youtube.html",context)

@login_required
def todo(request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False

            todo=Todo(user=request.user,title=request.POST['title'],is_finished=finished)

            todo.save()
            messages.success(request,f"Todo added from {request.user.username} Successfully!!!")
    else:
        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done=True
    else:
        todo_done=False
    context={'todos':todo,'form':form,'todo_done':todo_done}
    return render(request,"dashboard/todo.html",context)

@login_required
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')
'''
def books(request):
    form=DashboardForm()
    context={'form':form}
    return render(request,"dashboard/books.html",context)
'''
def books(request):
    if request.method == "POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }


            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,"dashboard/books.html",context)

    else:
        form=DashboardForm()
    context= {'form':form}
    return render(request,"dashboard/books.html",context)


def dictionary(request):

    if request.method == "POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            antonyms = answer[0]['meanings'][0]['definitions'][0]['antonyms']

            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
                'antonyms':antonyms
            }

        except:
            context={
                'form':form,
                'input':''
            }
        return render(request,"dashboard/dictionary.html",context)

    else:
        form=DashboardForm()
    context= {'form':form}
    return render(request,"dashboard/dictionary.html",context)


def wiki(request):
    if request.method == 'POST':
        text=request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"dashboard/wiki.html",context)
    else:
        form=DashboardForm()
    context= {'form':form}
    return render(request,"dashboard/wiki.html",context)


def register(request):
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Account created!!!")
            return redirect('login')
    else:
        form=UserRegistrationForm()
    context={
        'form':form
    }
    return render(request,"dashboard/register.html",context)

@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False

    if len(todos)==0:
        todo_done=True
    else:
        todo_done=False

    context={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todo_done':todo_done
    }
    return render(request,"dashboard/profile.html",context)

def quiz(request):
    courses=Course.objects.all()
    context={'courses':courses}
    return render(request,"dashboard/quiz.html",context)

def api_ques(request,id):
    raw_questions=Question.objects.filter(course=id)[:20]
    questions=[]

    for raw_question in raw_questions:
        question={}
        question['question']=raw_question.question
        question['answer']=raw_question.answer
        options=[]
        options.append(raw_question.opt_one)
        options.append(raw_question.opt_two)
        
        if raw_question.opt_three != '':
            options.append(raw_question.opt_three)
        if raw_question.opt_four != '':
            options.append(raw_question.opt_four)

        question['options']=options
        question['desc']=raw_question.desc
        question['id']=raw_question.id
        questions.append(question)
        

    return JsonResponse(questions,safe=False)

def take_quiz(request,id):
    context={'id':id}
    return render(request,"dashboard/take_quiz.html",context)

