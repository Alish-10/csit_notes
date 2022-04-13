from . models import *
from . forms import *
from django.contrib import messages

from django.views import generic

from youtubesearchpython import VideosSearch
import requests
from django.shortcuts import render,HttpResponse, redirect, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout




# Create your views here.
def Home(request):
    con = Contact.objects.all()
    context = {'con':con}
    return render(request,'MaterialRecommender/studyportal.html', context)

def usefullink(request):
    return render(request,'MaterialRecommender/link.html')



def studyportal(request):
    con = Contact.objects.all()
    context = {'con':con}
    return render(request,'MaterialRecommender/studyportal.html', context)

def search(request):
    query = request.GET['query']
    if len(query) > 30:
        allMa = []
        messages.warning(request,'Your query for search is too long ! no search result found')
    if len(query)<2:
        allMa = []
        messages.warning(request,'Your query for search is too short ! no search result found')
    else:
        allMat1 = Material.objects.filter(title__icontains=query)
        allMat2 = Material.objects.filter(categorise__icontains=query)
        allMa = allMat1.union(allMat2)
    params = {'allMa':allMa, 'query':query}
    return render(request,'MaterialRecommender/search.html', params)


def profile(request):
    if request.user.is_authenticated:
        #"select sum(rating) from Rating where user=request.user.id"
        r=Rating.objects.filter(user=request.user.id)
        totalReview=0
        for item in r:
            totalReview+=int(item.rating)
        #select count(*) from Rating where user=request.user.id"
        totalwatchedmaterial=Rating.objects.filter(user=request.user.id).count()
        return render(request,'MaterialRecommender/profile.html',{'totalReview':totalReview,'totalwatchedmaterial':totalwatchedmaterial})
    else:
        return render(request,'MaterialRecommender/studyportal.html')

'''

Note
'''

def Notes(request):
    if request.method=='POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = Note(user = request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f'Notes added by {request.user.username} Successfully!')
        return redirect('notes')
    else:
        form = NoteForm()
    notes = Note.objects.filter(user=request.user)        #retrive all notes created by individual user
    context = {'notes':notes,'form':form}
    return render(request,'MaterialRecommender/notes.html', context)




def Delete_Note(request, pk):
    Note.objects.get(id=pk).delete()
    return redirect('notes')





class NoteDetailView(generic.DetailView):
    model = Note


'''
Youtube
'''
def youtube(request):
    try:
        if request.method=='POST':
            form = DashboardForm(request.POST)
            text = request.POST['text']
            video = VideosSearch(text, limit=5)
            result_lst=[]
            for i in video.result()['result']:
                result_dict={
                    'input':text,
                    'title':i['title'],
                    'duration':i['duration'],
                    'thumbnail':i['thumbnails'][0]['url'],
                    'channel':i['channel']['name'],
                    'link':i['link'],
                    'views':i['viewCount']['short'],
                    'published':i['publishedTime'],
                }
                desc = ''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['description']=desc
                result_lst.append(result_dict)
                context = {'form':form,'results':result_lst,}
            return render(request,'MaterialRecommender/youtube.html',context)
        else:
            form = DashboardForm()
        context = {'form':form}
        return render(request,'MaterialRecommender/youtube.html',context)
    except:
        form = DashboardForm()
        context = {'form':form}
        messages.error(request, 'check your internet connection')
        return render(request,'MaterialRecommender/youtube.html',context)



'''
todo
'''

def ToDo(request):
    if request.method=='POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(user = request.user,title=request.POST['title'],is_finished=finished)
            todos.save()
            messages.success(request, f'ToDo added by {request.user.username} Successfully!')
            return redirect('todo')
    else:
        form  = TodoForm()
    form  = TodoForm()
    todos = Todo.objects.filter(user=request.user)         #retrive all notes created by individual use
    if len(todos)==0:
        todos_done = True
    else:
        todos_done=False
    context = {'todos':todos,'todos_done':todos_done,'form':form}
    return render(request,'MaterialRecommender/todo.html', context)


def update_todo(request,pk):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def Delete_Todo(request, pk):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')




def Books(request):
    try:
        if request.method=='POST':
            form = DashboardForm(request.POST)
            text = request.POST['text']
            url = 'https://www.googleapis.com/books/v1/volumes?q='+text
            r = requests.get(url)
            answer = r.json()
            result_lst=[]
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
                result_lst.append(result_dict)
                context = {'form':form,'results':result_lst,}
            return render(request,'MaterialRecommender/books.html',context)
        else:
            form = DashboardForm()
        context = {'form':form}
        return render(request,'MaterialRecommender/books.html',context)
    except:
        form = DashboardForm()
        context = {'form':form}
        messages.error(request, 'check your internet connection')
        return render(request,'MaterialRecommender/books.html',context)
    
# def addmaterial(request):
#     if request.user.is_authenticated:
#         if request.method=='POST':
#             title=request.POST['title']
#             categorise=request.POST['categorise']
#             image=request.FILES['image']
#             content=request.POST['content']
#             fm = Material(title=title,categorise=categorise,image=image,content=content)
#             fm.save()
#             messages.success(request,'Material Added Successfully!!!')
#         return render(request,'MaterialRecommender/addmaterial.html')
#     else:
#         return HttpResponseRedirect('/login/')
def addmaterial(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=AddMaterialForm(request.POST,request.FILES)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Material Added Successfully!!!')
                return redirect('addmaterial')
        else:
            fm=AddMaterialForm()
        return render(request,'MaterialRecommender/addmaterial.html',{'form':fm})
    else:
        return redirect('studyportal')



def MaterialDetailView(request,pk):
    if request.method=='POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = Note(user = request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f'Notes added by {request.user.username} Successfully!')
        return redirect('notes')
    else:
        form = NoteForm()
    # notes = Note.objects.filter(user=request.user)        #retrive all notes created by individual user
    fm = Material.objects.filter(id=pk)
    context = {'notes':notes,'form':form,'fm':fm}
    return render(request,'MaterialRecommender/material_detail.html',context)
    



def Material_delete(request, pk):
    Material.objects.get(id=pk).delete()
    return redirect('dashboard')


def contact(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        country=request.POST['country']
        subject=request.POST['subject']
        ct = Contact(fname=fname, lname=lname, country=country, subject=subject)
        ct.save()
        messages.success(request, f'Your suggestion has been submitted successfully!')
    else:
        return render(request,'MaterialRecommender/contact.html')
    return render(request,'MaterialRecommender/contact.html')



def delete_suggestion(request,pk):
    Contact.objects.get(id=pk).delete()
    return redirect('studyportal')


def addmember(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=MemberForm(request.POST,request.FILES)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Member Added Successfully!!!')
                return HttpResponseRedirect('addmember')
        else:
            fm=MemberForm()
        return render(request,'MaterialRecommender/addmember.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')


def about(request):
    con = Member.objects.all()
    context = {'con':con}
    return render(request,'MaterialRecommender/member.html', context)


def videolink(request,link):
    return render(request,'MaterialRecommender/video.html',{'link':link})