from django.shortcuts import redirect, render,HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User,Group
from .forms import *
from .models import *
from django.contrib import messages
import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import random
from .function import Material_delete,MaterialDetailView
# Create your views here.
from .function import *

def Mat():
    allMat=Material.objects.all()
    params={'allMat':allMat }
    return params


def generateRecommendation(request):
    material=Material.objects.all()
    rating=Rating.objects.all()
    x=[] 
    y=[]
    A=[]
    B=[]
    C=[]
    D=[]
    #Material Data Frames
    for item in material:
        x=[item.id,item.title,item.content,item.image.url,item.categorise] 
        y+=[x]
    materials_df = pd.DataFrame(y,columns=['materialId','title','content','image','categorise'])
    print("Materials DataFrame")
    print(materials_df)
    print(materials_df.dtypes)
    #Rating Data Frames
    print(rating)
    for item in rating:
        A=[item.user.id,item.material,item.rating]
        B+=[A]
    rating_df=pd.DataFrame(B,columns=['userId','materialId','rating'])
    print("Rating data Frame")
    rating_df['userId']=rating_df['userId'].astype(str).astype(np.int64)
    rating_df['materialId']=rating_df['materialId'].astype(str).astype(np.int64)
    rating_df['rating']=rating_df['rating'].astype(str).astype(np.float)
    print(rating_df)
    print(rating_df.dtypes)
    if request.user.is_authenticated:
        userid=request.user.id
        #select related is join statement in django.It looks for foreign key and join the table
        userInput=Rating.objects.select_related('material').filter(user=userid)
        if userInput.count()== 0:
            recommenderQuery=None
            userInput=None
        else:
            for item in userInput:
                C=[item.material.title,item.rating]
                D+=[C]
            inputMaterials=pd.DataFrame(D,columns=['title','rating'])
            print("Watched Materials by user dataframe")
            inputMaterials['rating']=inputMaterials['rating'].astype(str).astype(np.float)
            print(inputMaterials.dtypes)

            #Filtering out the materials by title
            inputId = materials_df[materials_df['title'].isin(inputMaterials['title'].tolist())]
            #Then merging it so we can get the materialId. It's implicitly merging it by title.
            inputMaterials = pd.merge(inputId, inputMaterials)
            # #Dropping information we won't use from the input dataframe
            # inputMaterials = inputMaterials.drop('year', 1)
            #Final input dataframe
            #If a material you added in above isn't here, then it might not be in the original 
            #dataframe or it might spelled differently, please check capitalisation.
            print(inputMaterials)

            #Filtering out users that have watched materials that the input has watched and storing it
            userSubset = rating_df[rating_df['materialId'].isin(inputMaterials['materialId'].tolist())]
            print(userSubset.head())

            #Groupby creates several sub dataframes where they all have the same value in the column specified as the parameter
            userSubsetGroup = userSubset.groupby(['userId'])
            
            #print(userSubsetGroup.get_group(7))

            #Sorting it so users with material most in common with the input will have priority
            userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

            print(userSubsetGroup[0:])


            userSubsetGroup = userSubsetGroup[0:]


            #Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
            pearsonCorrelationDict = {}

        #For every user group in our subset
            for name, group in userSubsetGroup:
            #Let's start by sorting the input and current user group so the values aren't mixed up later on
                group = group.sort_values(by='materialId')
                inputMaterials = inputMaterials.sort_values(by='materialId')
                #Get the N for the formula
                nRatings = len(group)
                #Get the review scores for the materials that they both have in common
                temp_df = inputMaterials[inputMaterials['materialId'].isin(group['materialId'].tolist())]
                #And then store them in a temporary buffer variable in a list format to facilitate future calculations
                tempRatingList = temp_df['rating'].tolist()
                #Let's also put the current user group reviews in a list format
                tempGroupList = group['rating'].tolist()
                #Now let's calculate the pearson correlation between two users, so called, x and y
                Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
                Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
                Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
                
                #If the denominator is different than zero, then divide, else, 0 correlation.
                if Sxx != 0 and Syy != 0:
                    pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
                else:
                    pearsonCorrelationDict[name] = 0

            print(pearsonCorrelationDict.items())

            pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
            pearsonDF.columns = ['similarityIndex']
            pearsonDF['userId'] = pearsonDF.index
            pearsonDF.index = range(len(pearsonDF))
            print(pearsonDF.head())

            topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:]
            print(topUsers.head())

            topUsersRating=topUsers.merge(rating_df, left_on='userId', right_on='userId', how='inner')
            topUsersRating.head()

                #Multiplies the similarity by the user's ratings
            topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['rating']
            topUsersRating.head()


            #Applies a sum to the topUsers after grouping it up by userId
            tempTopUsersRating = topUsersRating.groupby('materialId').sum()[['similarityIndex','weightedRating']]
            tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
            tempTopUsersRating.head()

            #Creates an empty dataframe
            recommendation_df = pd.DataFrame()
            #Now we take the weighted average
            recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
            recommendation_df['materialId'] = tempTopUsersRating.index
            recommendation_df.head()

            recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
            recommender=materials_df.loc[materials_df['materialId'].isin(recommendation_df.head(10)['materialId'].tolist())]
            print(recommender)
            return recommender.to_dict('records')
            

            

import uuid
from .utils import *


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass0 = request.POST.get('pass0')
        pass1 = request.POST.get('pass1')
        
        #creating user
        check_user=User.objects.filter(email=email).first()


        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
            return render(request,'MaterialRecommender/studyportal.html')
        if not username.isalnum():
            messages.error(request,"Username must contains only letters and numbers!!")
            return render(request,'MaterialRecommender/studyportal.html')
        if pass0 != pass1:
            messages.error(request,"Password doesnot match!!")
            return render(request,'MaterialRecommender/studyportal.html')
        
        if check_user:
            messages.error(request,"Email is already registered!!")
            return render(request,'MaterialRecommender/studyportal.html')
        else:
            myuser=User.objects.create_user(username, email, pass1, first_name=fname, last_name=lname)
            myuser.save()
            puser=Profile.objects.create(user=myuser,email_token=str(uuid.uuid4()))
            puser.save()
            messages.success(request,"Your account is created successfully!! check your mailbox for confirmation..")
            send_email_token(email,puser.email_token)
            return render(request,'MaterialRecommender/studyportal.html')
    else:
        return render(request,'MaterialRecommender/studyportal.html')


def verify(request,token):
    try:
        obj1=Profile.objects.filter(email_token=token).first()
        if obj1:
            if obj1.is_verified:
                messages.success(request,"Your account is already verified.")
                return redirect('studyportal')
            else:
                obj=Profile.objects.get(email_token=token)
                obj.is_verified=True
                obj.save()
                messages.success(request,"Your account is verified.")
                return redirect('studyportal')
    except Exception as e:
        messages.error(request,"Your account nedd to verified.")
        return redirect('studyportal')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass2')


        
        user = authenticate(request, username=username, password=password)


        check_user=User.objects.filter(username=username).first()
        pro_obj=Profile.objects.filter(user=check_user).first()

        if user is None:
            messages.error(request,"User Does not exist!")
            return redirect('studyportal')
        else:
            if user.is_staff:
                if user is not None:
                    login(request, user)
                    print(user)
                    messages.success(request,"You're successfully logged in!")
                    return redirect('studyportal')
                else:
                    messages.error(request,"Sorry invalid credentials!")
                    return redirect('studyportal')
            else:
                if not pro_obj.is_verified:
                    messages.error(request,"Your id is not verified, please check your mailbox!")
                    return redirect('studyportal')
                else:
                    if user is not None:
                        login(request, user)
                        print(user)
                        messages.success(request,"You're successfully logged in!")
                        return redirect('studyportal')
                    else:
                        messages.error(request,"Sorry invalid credentials!")
                        return redirect('studyportal')
    else:
        return redirect('studyportal')



def Rec(request):
    params=Mat()
    a=generateRecommendation(request)
    params['recommended']=a
    return render(request,'MaterialRecommender/home.html',params)



def dashboard(request):
    if request.user.is_authenticated:
        params=Mat()
        params['recommended']=generateRecommendation(request)
        params['user']=request.user
        if request.method=='POST':
            userid=request.POST.get('userid')
            materialid=request.POST.get('materialid')
            material=Material.objects.all()
            u=User.objects.get(pk=userid)
            m=Material.objects.get(pk=materialid)
            rfm=AddRatingForm(request.POST)
            params['rform']=rfm
            if rfm.is_valid():
                rat=rfm.cleaned_data['rating']
                count=Rating.objects.filter(user=u,material=m).count()
                if(count>0):
                    messages.warning(request,'You have already submitted your review!!')
                    return redirect('dashboard')
                action=Rating(user=u,material=m,rating=rat)
                action.save()
                messages.success(request,'You have submitted'+' '+rat+' '+"star")
                return redirect('dashboard')
            return render(request,'MaterialRecommender/dashboard.html',params)
        else:
            #print(request.user.id)
            rfm=AddRatingForm()
            params['rform']=rfm
            material=Material.objects.all()
            return render(request,'MaterialRecommender/dashboard.html',params)
    else:
        return render(request,'MaterialRecommender/studyportal.html',params)
            
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('studyportal')
    else:
        return redirect('studyportal')







