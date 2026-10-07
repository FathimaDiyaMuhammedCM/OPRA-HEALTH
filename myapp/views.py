import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

import cv2
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


# Create your views here.
# from fer import FER

from myapp.models import *


def login_get(request):
    return render(request,'login.html')

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(request, username=username, password=password)
    if not user is None:
        login(request, user)
        if user.groups.filter(name="admin").exists():
            messages.error(request,'Login successful.')
            return redirect('/myapp/adminhome/')
        else:
            messages.error(request, 'No such groups.')
            return redirect('/myapp/login_get/')
    else:
        messages.error(request,'User not found')
        return render(request, 'login.html')

def logout1(request):
    logout(request)
    return redirect('/myapp/login_get/')

def and_forget_password(request):
    return render(request, 'forgottenpassword.html')

def and_forget_password_post(request):
    if request.method == 'POST':
        email = request.POST['textfield']

        user = User.objects.get(email=email)
        print(user)
        if user is None:
            messages.warning(request,'Email doest not exists')
            return redirect('/myapp/login/')
        import random
        psw = random.randint(1000, 9999)

        user.set_password(str(psw))
        user.save()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("trainingstarted@gmail.com", "nlxasujxgazlbmgz")  # App Password

        subject = "Password Reset - Construction App"
        body = "Your new password is: " + str(psw)
        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail("trainingstarted@gmail.com", email, msg)
        server.quit()

        messages.success(request,'Password Send successfully')
        return redirect('/myapp/login/')


    else:
        messages.warning(request, 'Failed to send')
        return render(request,'login.html')

@login_required(login_url='/myapp/login_get/')
def adminhome(request):
    return render(request,'adminhome.html')



@login_required(login_url='/myapp/login_get/')
def view_users(request):
    data=Users.objects.all()
    return render(request,'view_users.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def view_complaints(request):
    data=Complaint.objects.all()
    return render(request,'view_complaints.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def send_reply(request,id):
    return render(request,'send_reply.html',{'id':id})

def send_reply_post(request):
    id=request.POST['id']
    reply=request.POST['reply']
    Complaint.objects.filter(id=id).update(reply=reply,status='replied')
    return redirect('/myapp/view_complaints/')


@login_required(login_url='/myapp/login_get/')
def view_feedback(request):
    data=Feedback.objects.all()
    return render(request,'view_feedback.html',{'data':data})

@login_required(login_url='/myapp/login_get/')
def admin_change_password(request):
    return render(request, 'change_password.html')


def admin_change_password_post(request):
    c_password = request.POST['current_password']
    n_password = request.POST['new_password']
    con_password = request.POST['confirm_password']
    data = request.user
    if not data.check_password(c_password):
        messages.error(request,'Invalid password')
        return render(request, 'change_password.html')
    if n_password != con_password:
        messages.error(request,'Password mismatch')
        return render(request, 'change_password.html')
    data.set_password(n_password)
    data.save()
    return redirect('/myapp/login_get/')


#Mentor
# us=User.objects.get(username="ramni@gmail.com")
# us.set_password("sivakami")
# us.save()
def login_flut(request):
    username=request.POST['username']
    password=request.POST['password']
    print(password)
    user = authenticate(request, username=username, password=password)
    print(user)
    if not user is None:
        login(request, user)
        if user.groups.filter(name="users").exists():
           
            return JsonResponse({'status':'ok','lid':str(user.id)})
       
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})


def android_forget_password_post(request):
    email = request.POST['email']
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'})

    user = User.objects.get(username=email)
    print(user, "iii")
    print(email)
    print("hhhh")

    # Generate new password
    import random
    new_pass = str(random.randint(1000, 9999))
    user.password = make_password(new_pass)
    user.save()
    print(new_pass)

    # Email configuration
    print("jjjj")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "trainingstarted@gmail.com"
    app_password = "nlxasujxgazlbmgz"

    subject = "Your New Password"
    body = f"Your new password is: { new_pass }"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(message)
    server.quit()

    return JsonResponse({'status': 'ok', 'message': 'Password sent to your email'})




def User_sendchat(request):
    FROM_id = request.POST['from_id']
    print(FROM_id)
    msg = request.POST['message']

    from  datetime import datetime
    c = Chat()
    c.FROM_id = FROM_id
    c.message = msg
    c.date = datetime.now()
    c.time = datetime.now().time()
    c.save()
    return JsonResponse({'status': "ok"})

def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status": "ok", 'data': l})






def user_register(request):
    name = request.POST['firstname']
    email = request.POST['email']
    dob = request.POST['dateofbirth']
    place = request.POST['country']
    gender = request.POST['gender']
    phone = request.POST['phonenumber']
    pin = request.POST['pin']
    post = request.POST['post']
    password = request.POST['password']
    confirmpassword = request.POST['confirmpassword']

    # Fetch image from FILES (not POST)
    image = request.FILES.get('image')

    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    file_url = fs.url(filename)

    # Save Login
    lobj = User.objects.create_user(username=email, password=password, email=email)
    lobj.groups.add(Group.objects.get(name='users'))
    lobj.save()

    uobj = Users()
    uobj.name = name
    uobj.email = email
    uobj.phone = phone
    uobj.image = filename
    uobj.pin = pin
    uobj.post = post
    uobj.place = place
    uobj.gender = gender
    uobj.dob = dob
    uobj.USER = lobj
    uobj.save()

    return JsonResponse({'status': 'ok'})


def user_view_profile(request):
    id=request.POST['lid']


    print(id,"===")
    
    data=Users.objects.get(USER_id=id)

    print(data)

    return JsonResponse({'status':'ok',
                'name': data.name,
                'gender': data.gender,
                'email': data.email,
                'phone': data.phone,
                'dob': data.dob,
                'place': data.place,
                'district': data.post,
                'state': "",
                'pin': data.pin,
                'photo': data.photo,})


def user_edit_profile(request):
    id=request.POST['lid']
    username = request.POST['uname']
    print(username, "----------------------------------------")
    gender = request.POST['gender']
    dob = request.POST['udob']
    email = request.POST['uemail']
    phone = request.POST['uphoneno']
    place = request.POST['uplace']
    district = request.POST['udistrict']
    state = request.POST['ustate']
    pin = request.POST['upin']
    data=Users.objects.get(USER=id)

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.datetime.now().strftime("%d-%M-%Y-%H-%M-%S") + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        data.photo=path
        data.save()



    data.name = username
    data.email = email
    data.dob = dob
    data.gender = gender
    data.phone = phone
    data.place = place
    data.district = district
    data.state = state
    data.pin = pin
    data.save()

    return JsonResponse({'status': 'ok', 'id': data.id})

    print(mentor_list)

    return JsonResponse({'status': 'ok', 'data': mentor_list})

def User_sendchat1(request):
    FROM_id = request.POST['from_id']
    TOID_id = request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg = request.POST['message']

    from  datetime import datetime
    c = Chat()
    c.FROM_id = FROM_id
    c.TO_id = TOID_id
    c.message = msg
    c.date = datetime.now()
    c.save()
    return JsonResponse({'status': "ok"})

def User_viewchat1(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status": "ok", 'data': l})




def add_complaint(request):
    complaint = request.POST['complaint']
    id = request.POST['lid']

    # Save Customer data
    data = Complaint()
    data.WOMEN = Women.objects.get(USER=id)
    data.complaint = complaint
    data.date = datetime.datetime.now().today()
    data.reply='pending'
    data.status='pending'
    data.save()
    return JsonResponse({'status': 'ok', 'id': data.id})

import cv2


def user_view_complaints(request):
    id=request.POST['lid']
    data=Complaint.objects.filter(USERS__USER_id=id)
    l=[]
    for i in data:
        l.append({'id':i.id,'date':i.date,'complaint':i.complaint,'reply':i.reply,'status':i.status})
    print(l)
    return JsonResponse({'status':'ok','data':l})

def add_feedback(request):
    feedback = request.POST['feedback']
    id = request.POST['lid']

    # Save Customer data
    data = Feedback()
    data.USERS = Users.objects.get(USER=id)
    data.feedback = feedback
    data.date = datetime.datetime.now().today()
    data.save()
    return JsonResponse({'status': 'ok', 'id': data.id})




import os
import datetime
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
from django.http import JsonResponse
from .models import Facial_emotion, Users

# ----------------------------
# PyTorch Model Setup
# ----------------------------
MODEL_PATH = "C:\\Riss\\mithra\\web\\mithra\\myapp\\saved_models\\facial_emotion_model.pth"
IMG_SIZE = 64
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])

# Load model
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, len(classes))
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

# ----------------------------
# Emotion prediction function
# ----------------------------
def predict_emotion(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1).cpu().numpy().flatten()
        pred_class = classes[probs.argmax()]
    return pred_class, probs

# ----------------------------
# Django API: Save facial emotion
# ----------------------------
def save_facial_emotion(request):
    if request.method == "POST" and 'photo' in request.FILES:
        wid=request.POST['lid']
        photo = request.FILES['photo']

        # Save image locally
        save_dir = "media/facial_images/"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{datetime.datetime.now().timestamp()}_{photo.name}")
        with open(save_path, 'wb+') as f:
            for chunk in photo.chunks():
                f.write(chunk)

        # Predict emotion
        emotion, _ = predict_emotion(save_path)

        # Save to database
        try:
            w = Users.objects.get(USER=wid)
            Facial_emotion.objects.create(
                date=datetime.date.today(),
                time=datetime.datetime.now().time(),
                emotion=emotion,
                photo=save_path,
                USERS=w
            )
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid woman ID'}, status=400)

        # Return detected emotion
        return JsonResponse({'status': 'ok', 'emotion': emotion})

    return JsonResponse({'status': 'error', 'message': 'POST request with photo required'}, status=400)



def user_view_symptoms(request):

    
    sympt=['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

    l=[]

    for i in sympt:
        l.append(
            {
                'name':i
            }
        )
    
    return JsonResponse({'status':'ok','data':l})



def algo_predict(algo,choice_input):
    import pandas as pd
    data=pd.read_csv('C:\\Riss\\mithra\\web\\mithra\\myapp\\training.csv')
    X = data.drop('prognosis', axis=1)  # Assuming 'prognosis' is the target variable
    y = data['prognosis']
    if algo=='DecisionTree':
        DTmodel=DecisionTreeClassifier()
        DTmodel.fit(X, y)
        pred=DTmodel.predict([choice_input])
        return pred
    elif algo=='RandomForest':
        RFmodel=RandomForestClassifier(n_estimators=200)
        RFmodel.fit(X, y)
        pred=RFmodel.predict([choice_input])
        return pred
    elif algo=='KNN':
        KNNmodel=KNeighborsClassifier(n_neighbors=3)
        KNNmodel.fit(X, y)
        pred=KNNmodel.predict([choice_input])
        return pred
    elif algo=='SVM':
        SVMmodel=SVC()
        SVMmodel.fit(X, y)
        pred=SVMmodel.predict([choice_input])
        return pred
    elif algo=='NaiveBayes':
        NBmodel=GaussianNB()
        NBmodel.fit(X, y)
        pred=NBmodel.predict([choice_input])
        return pred
    return None

def predictdiseasebysymptoms(request):
    s=request.POST['s']

    m=s.split(',')

    sympt=['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
    symptoms = []
    for i in sympt:
        if i in m:
            symptoms.append(1)
        else:
            symptoms.append(0)

    prediction=algo_predict("RandomForest",symptoms)

    return JsonResponse({'status':'ok','data':prediction[0]})

    







