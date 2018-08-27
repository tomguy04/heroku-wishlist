# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# from .models import User, TripSchedule, Follow, Trip -old code
from .models import User, ItemList, Follow
import bcrypt
from itertools import chain
from operator import attrgetter
from datetime import datetime
from django.utils import timezone
from django.forms import extras
# the index function is called when root is visited
def index(request):
    return render(request,"wl_app/registrationForm.html")

def doregister(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        u1 = User(name = request.POST['name'], username = request.POST['username'], 
        date_hired = request.POST['datehired'],
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        u1.save()
        return redirect('/main')

def login(request):
    post_password = request.POST['password']
    post_username = request.POST["username"]
    print "*****************post_username " + post_username
    print "*****************post_pass " + post_password
    
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        try:
            u = User.objects.get(username = post_username)
            print "****************successful try"
            u.save()
            print u.id
            if bcrypt.checkpw(post_password.encode(), u.password.encode()):
                print "password match"
                request.session['id']=u.id
                print "*********** "
                print request.session['id']
                return redirect('/dashboard')
            return redirect('/main')
        except:
            return redirect('/main')
def dashboard(request):
    if 'id' in request.session:
        u = User.objects.get(id = request.session['id'])
        user_name = u.name
        print "user name is " + user_name
        today_date = timezone.now().date()
        print "today_date " + str(today_date)

        list1=[]  #wishes others created 
        list2 =[] #wishes I am following
        list3 = [] #all wish ids that I am following
        Final = [] #wishes others created that I am not following.

        for data in ItemList.objects.exclude(user_id=request.session['id']):
            list1.append(data)
        for data in Follow.objects.filter(follower_id=request.session['id']):
            list2.append(data)
        for data in list2:
            list3.append(data.item_id)
        # of the trips I did not create, which ones am I not following?
        for data in list1:
            if data.id not in list3:
                Final.append(data)

        context = {
            'user':user_name,
            'my_wishes': ItemList.objects.filter(user_id=request.session['id']),
            'wishes_joined': Follow.objects.filter(follower_id=request.session['id']),
            'other_wishes': Final
        }

        return render(request, "wl_app/dashboard.html", context) 
    else:
        return redirect('/main')

def getawish(request):
    if 'id' in request.session:
        u = User.objects.get(id = request.session['id'])
        user_name = u.name
    
        context = {
            'user':user_name,
        }

        return render(request, "wl_app/wishesadd.html", context)

def processwish(request): 
    errors = ItemList.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/wish_items/create')
    else:
        wish1 = ItemList(name = request.POST['name'], user_id = request.session['id'])
        wish1.save()
        return redirect ('/dashboard')


def remove(request,wid,uid): #deletes an wish from the follow table
    Item = Follow.objects.filter(item_id=wid, follower_id=uid)
    Item.delete()
    return redirect ('/dashboard')


def delete(request,wid): #deletes an entire wish from db
    Item = ItemList.objects.get(id=wid)
    Item.delete()
    return redirect ('/dashboard')

def wish(request,wid):
    myItemList = ItemList.objects.get(id=wid)
    if 'id' in request.session:
            u = User.objects.get(id = request.session['id'])
            user_name = u.name
    context={
        'myWishes':myItemList,
        'name':myItemList.user.name,
        'followers': Follow.objects.filter(item_id=wid),
        'user':user_name
    }
    return render(request, "wl_app/wish.html", context)

def joinwish(request,wid,uid):
    wish1 = ItemList.objects.get(id=wid)
    wish1.save()
    u1 = User.objects.get(id = uid)
    u1.save()
    Follow.objects.create(item = wish1, follower = u1)
    return redirect ('/dashboard')

def logout(request):
    request.session.clear()
    return redirect("/main")

def home(request):
    return redirect("/dashboard")



