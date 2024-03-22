from django.shortcuts import render
import pyrebase

config = {
  'apiKey': "AIzaSyAz2CUQWAMTHDkjQhqnunY7MVEXunE2aVo",
  'authDomain': "fir-django-415bb.firebaseapp.com",
  "databaseURL": "https://fir-django-415bb-default-rtdb.firebaseio.com/",
  'projectId': "fir-django-415bb",
  'storageBucket': "fir-django-415bb.appspot.com",
  'messagingSenderId': "610100914118",
  'appId': "1:610100914118:web:d1b229f25f705f4624b4c7",
  'measurementId': "G-EQK8MP57P6"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()


# Create your views here.

# home
# ---------------------------------------------------------------------------------
def home(request):
    
    day = database.child('data').child('day').get().val()
    id = database.child('data').child('id').get().val()
    projectname = database.child('data').child('projectname').get().val()
    
    context = {
        "day": day,
        "id": id,
        "projectname": projectname
    }
    
    return render(request, 'appone/home.html', context)


# signIn
# ---------------------------------------------------------------------------------
def signIn(request):
    return render(request, "appone/Login.html")


# postsignIn
# ---------------------------------------------------------------------------------
def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request, "appone/Login.html", {"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    
    day = database.child('data').child('day').get().val()
    id = database.child('data').child('id').get().val()
    projectname = database.child('data').child('projectname').get().val()
    
    context = {
        "day": day,
        "id": id,
        "projectname": projectname,
        "email":email
    }
    
    return render(request, "appone/home.html", context)


# logout
# ---------------------------------------------------------------------------------
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "appone/Login.html")


# signUp
# ---------------------------------------------------------------------------------
def signUp(request):
    return render(request, "appone/Registration.html")


# postsignUp
# ---------------------------------------------------------------------------------
def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
    except:
        return render(request, "appone/Registration.html")
    return render(request, "appone/Login.html")


# reset
# ---------------------------------------------------------------------------------
def reset(request):
	return render(request, "appone/Reset.html")


# postreset
# ---------------------------------------------------------------------------------
def postReset(request):
	email = request.POST.get('email')
	try:
		authe.send_password_reset_email(email)
		message = "A email to reset password is successfully sent"
		return render(request, "appone/Reset.html", {"msg":message})
	except:
		message = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "appone/Reset.html", {"msg":message})
