#Libiraries
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pyrebase
import pandas as pd
import numpy as np
import excel2json
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import json
from pandas import read_csv,read_excel
from django.utils.datastructures import MultiValueDictKeyError


# Configuartion Data from firebase
config={
    "apiKey": "AIzaSyDV4C8wI362b2ZpdSmGXVULLzdiTTwOg9s",
    "authDomain": "vajara-5f025.firebaseapp.com",
    "databaseURL":"https://vajara-5f025-default-rtdb.firebaseio.com",
    "projectId": "vajara-5f025",
    "storageBucket": "vajara-5f025.appspot.com",
   "messagingSenderId": "103552132125",
    "appId": "1:103552132125:web:ff22f2eefcbb6128b212f4",
    "measurementId": "G-5RY51MHTH2",
    
  }

# For firebase configuration
firebase=pyrebase.initialize_app(config)

#Aucthication      
authe=firebase.auth()

#To store the datavalues in firebase[RealTime database]
db=firebase.database()

#To store the datavalues in firebase[Storage]
storage= firebase.storage()

#Retrive data from database
user1 =db.get()

@csrf_exempt
def singIn(request):
	return render(request,"authication.html")
@csrf_exempt
def postsign(request):
    email=request.POST.get('form3Example3')
    passw=request.POST.get('form3Example4')
    try:
         user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"authication.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    nam="Welcome {}".format(email)
    return render(request,'dashboard.html',{"e":nam})

@csrf_exempt
def post_create(request):
    list1=[]
    if request.method == 'POST':
        file = request.FILES["data_file"]
        xlx =pd.read_excel(file)
        print(xlx.head())
        for i in range(len(xlx)):
            x=xlx.iloc[i]
            data={"Name":x[0],"Course":x[1],"Contact":x[2]}
            print(data)
            db.push(data)
            list1.clear()
            for i in user1.each():
                list1.append(i.val())
    print("This is list",list1)
    tex="{} Succussfully uploaded".format(file)
    return render(request,'dashboard.html', {'fi':tex,"allitems":list1})

















































