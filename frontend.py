
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
import cryptography
from cryptography.fernet import Fernet
import datetime
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Create your views here.
from Remote_User.models import postdetails_model,ClientRegister_Model,review_Model,attack_Model,recommend_Model,rating_Model


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            return redirect('Upload_Post')


    return render(request,'SProvider/serviceproviderlogin.html')

def Upload_Post(request):
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)  # The key is type bytes still
    file.close()

    file = open('key.key', 'rb')
    key = file.read()  # The key will be type bytes
    file.close()

    password_provided = "password"  # This is input in the form of a string
    password = password_provided.encode()  # Convert to type bytes
    salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

    f = Fernet(key)

    status=''
    result = ''
    pos = []
    neg = []
    oth = []
    se = 'se'
    ft='Added Post Details'
    if request.method == "POST":
        fname = request.POST.get('fname')
        tprice = request.POST.get('tprice')
        tname = request.POST.get('tname')
        fcat = request.POST.get('fcat')
        cname = request.POST.get('cname')
        cmd = request.POST.get('fdesc')

        datetime_object = datetime.datetime.now()

        fname1 = fname.encode()
        encrypted1 = f.encrypt(fname1)

        if '#' in cmd:
         startingpoint = cmd.find('#')
         a = cmd[startingpoint:]
         endingPoint = a.find(' ')
         title = a[0:endingPoint]
         result = title[1:]
        # return redirect('')

        for f in cmd.split():
            if f in ('good', 'nice', 'better', 'best', 'excellent', 'extraordinary', 'happy', 'won', 'love', 'greate',):
                pos.append(f)
            elif f in ('worst', 'waste', 'poor', 'error', 'imporve', 'bad', 'ridicules'):
                neg.append(f)
            else:
                oth.append(f)
        if len(pos) > len(neg):
            se = 'positive'
        elif len(neg) > len(pos):
            se = 'negative'
        else:
            se = 'nutral'

        postdetails_model.objects.create(names=fname ,f_story=cmd ,fcat=fcat, c_name=cname,topics=result, t_price=tprice,t_name=tname, sanalysis=se,
                                        DT=datetime_object,senderstatus='process')
    return render(request,'SProvider/Upload_Post.html', {'obj':status,'result': result, 'se': se,'ft':ft})



def viewtreandingquestions(request,chart_type):
    dd = {}
    pos,neu,neg =0,0,0
    poss=None
    topic = postdetails_model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics=t['ratings']
        pos_count=postdetails_model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss=pos_count
        for pp in pos_count:
            senti= pp['names']
            if senti == 'positive':
                pos= pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics]=[pos,neg,neu]
    return render(request,'SProvider/viewtreandingquestions.html',{'object':topic,'dd':dd,'chart_type':chart_type})

def Positive_Sentiments(request):

    rtype='Positive'
    #obj = review_Model.objects.all()

    obj = review_Model.objects.all().filter(sanalysis=rtype)

    return render(request,'SProvider/Positive_Sentiments.html',{'list_objects': obj})

def View_Attackers(request):

    obj = attack_Model.objects.all()
    return render(request,'SProvider/View_Attackers.html',{'list_objects': obj})

def Negative_Sentiments(request):

    rtype='Negative'
    #obj = review_Model.objects.all()

    obj = review_Model.objects.all().filter(sanalysis=rtype)

    return render(request,'SProvider/Negative_Sentiments.html',{'list_objects': obj})

def Neutral_Sentiment(request):

    rtype='Neutral'
    #obj = review_Model.objects.all()

    obj = review_Model.objects.all().filter(sanalysis=rtype)

    return render(request,'SProvider/Neutral_Sentiment.html',{'list_objects': obj})


def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = postdetails_model.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def negativechart(request,chart_type):
    dd = {}
    pos, neu, neg = 0, 0, 0
    poss = None
    topic = postdetails_model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics = t['ratings']
        pos_count = postdetails_model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss = pos_count
        for pp in pos_count:
            senti = pp['names']
            if senti == 'positive':
                pos = pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics] = [pos, neg, neu]
    return render(request,'SProvider/negativechart.html',{'object':topic,'dd':dd,'chart_type':chart_type})


def charts(request,chart_type):
    chart1 = postdetails_model.objects.values('names').annotate(dcount=Avg('ratings'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def dislikeschart(request,dislike_chart):
    charts = postdetails_model.objects.values('names').annotate(dcount=Avg('dislikes'))
    return render(request,"SProvider/dislikeschart.html", {'form':charts, 'dislike_chart':dislike_chart})

def likeschart(request,like_chart):
    charts = postdetails_model.objects.values('names').annotate(dcount=Avg('likes'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})

def View_Post_Details(request):

    obj = postdetails_model.objects.all()
    return render(request, 'SProvider/View_Post_Details.html', {'list_objects': obj})

def viewallpostsreviews(request):

        obj = review_Model.objects.all()

        return render(request, 'SProvider/Viewallpostsreviews.html', {'list_objects': obj})

def View_Recommended_Post(request):
    obj = recommend_Model.objects.all()

    return render(request, 'SProvider/View_Recommended_Post.html', {'list_objects': obj})





