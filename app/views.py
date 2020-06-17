from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AuthUser, UserFriend, UserScore
from datetime import datetime
from app import emailService
from random import randint

# Create your views here.


def login_user(request):
    data = {}
    data['user'] = []
    data['user'].append(request.user)
    return render(request, 'login.html', data)

@login_required(login_url='')
def index(request):
    data = {}
    data['user'] = []
    data['score'] = []
    data['user'].append(request.user)
    data['error'] = []
    try:
        user = AuthUser.objects.get(id=request.user.id)
        data['score'] = UserScore.objects.filter(user=user)
    except:
        data['error'].append('Erro ao carregar dados, tente novamente!')
    return render(request, 'index.html', data)

def logout_user(request):
    logout(request)
    return redirect('/')

@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index.html')
        else:
            messages.error(request,'Usuário ou senha inválidos. Tentar novamente ou cadastre-se')
    return redirect('/')

@csrf_protect
def submit_register(request):
    data = {}
    data['msg'] = []
    x = 0
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        is_superuser = False
        is_staff = True
        is_active = True
        date_joined = datetime.now()
        try:
            val_username = User.objects.filter(username=username)
            val_email = User.objects.filter(email=email)
            if (len(val_username) > 0):
                data['msg'].append('usuário já cadastrado!')
                x = 1
            if (len(val_email) > 0):
                data['msg'].append('E-mail já cadastrado!')
                x = 1
        except:
            data['msg'].append('Erro ao verificar usuário ou email!')
            return render(request, 'register.html', data)
        
        if (password != rpassword):
            data['msg'].append('Senhas não conferem')
            x = 1
        if (x > 0):
            return render(request,'register.html', data)
        try:
            user = User(is_superuser=is_superuser,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            date_joined=date_joined)
            user.set_password(password)
            user.save()
            data['msg'].append('Cadastro realizado com Sucesso!')
            return render(request, 'login.html', data)
        except:
            data['msg'].append('Ocorreu algum erro, tente novamente mais tarde!')
            return render(request,'register.html', data)
    else:
        return render(request, 'register.html', data)

def register(request):
    return render(request, 'register.html')        

@csrf_protect
def recovery_pass(request):
    data = {}
    data['msg'] = []
    data['error'] = []
    if request.method =='POST':
        email = request.POST.get('email')
        try:
            if(email == ''):
                data['error'].append('email inválido')
            else:
                val_user = User.objects.filter(email=email)
                if (len(val_user) > 0):
                    newpass = randint(10000000,99999999)
                    user = User.objects.get(email=email)
                    user.set_password(newpass)
                    user.save()
                    emailService.recoveryPass(newpass, user.username, email)
                    data['msg'].append('Sua nova senha foi enviada no email!')
                else:
                    data['error'].append('email não cadastrado!')   
        except:
            data['error'].append('Ocorreu algum erro, tente novamente mais tarde!')
            return render(request,'recovery_pass.html', data)  
    return render(request, 'recovery_pass.html', data)

@csrf_protect
def submit_score(request):
    data = {}
    data['sucess'] = []
    data['error'] = []
    if request.method == 'POST':
            nivel = request.POST.get('nivel')
            ponto = request.POST.get('ponto')
            print(nivel)
            print(ponto)
    try:
        user = AuthUser.objects.get(id=request.user.id)
        print("passei aqui")
        userScore = UserScore.objects.filter(user=user)
        print("passei aqui ok")
        if (len(userScore) < 1):
            userScoreIn = UserScore(user=user,dif_easy=5,dif_med=4,dif_hard=1)
            userScoreIn.save()
            print("passei aqui")
        else:
            userScore[0].dif_easy = 6
            userScore[0].dif_med = 4
            userScore[0].dif_hard = 7
            userScore[0].save()
            print("passei aqui 2")
        print("passei aqui 3")
        return redirect('index')
    except: 
        data['error'].append('Erro ao salvar pontuação!')
        return redirect('index')

@login_required(login_url='')
@csrf_protect
def game(request):
    data = {}
    data['user'] = []
    data['user'].append(request.user)
    data['nivel'] = []
    data['life'] = []
    data['time'] = []
    data['error'] = []
    if request.method =='POST':
        if request.POST.get('easy'):
            data['nivel'].append('Fácil')
            data['life'].append(7)
            data['time'].append(10)
        elif request.POST.get('med'):
            data['nivel'].append('Médio')
            data['life'].append(5)
            data['time'].append(7)
        elif request.POST.get('hard'):
            data['nivel'].append('Difícil')
            data['life'].append(3)
            data['time'].append(3)
        else:
            data['error'].append('Erro ao carregar nível de dificuldade, tente mais tarde!')
    return render(request, 'game.html',data)

'''@csrf_protect
def friend(request):
    data = {}
    #data['user'] = []
    #data['users'] = []
    #data['user'].append(request.user)
    #data['friends'] = []
    data['error'] = []
    if request.method == 'GET':
        id = request.GET.get('id')
        op = request.GET.get('op')
        if(id != None and op != None):
            try:           
                friend = AuthUser.objects.get(id=id)
                iduser = int(request.user.id)
                #x = UserFriend.objects.filter(my_id=iduser,friend_id=friend)
                if(friend == ''):
                    data['error'].append('Amigo inválido')
                #elif(x[0].friend_id == friend):
                #    data['error'].append('Amigo já adicionado')
                #    return redirect(request, 'index', data)
                elif(op == "add"):
                    fr = UserFriend(my_id=iduser,friend_id=friend)
                    fr.save()
                elif(op == "del"):
                    fr = UserFriend.objects.get(my_id=iduser,friend_id=friend)
                    fr.delete()
            except:
                data['error'].append("Erro ao adicionar amigo! Tente novamente")
        return redirect('index')'''