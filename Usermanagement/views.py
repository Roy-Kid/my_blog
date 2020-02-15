from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from .forms import *

from .models import Profile

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])

            if user:
                login(request, user)
                return redirect('Blog:blog_index')

            else:
                return HttpResponse('username or passwd is not correct, please 好好想想')
    
        else:
            return HttpResponse('别找事嗷！')

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request, 'Usermanagement/login.html', context)

    else:
        return HttpResponse('报警了嗷！')

def user_logout(request):
    logout(request)
    return redirect("Blog:blog_index")

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterFrom(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("Blog:blog_index")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterFrom()
        context = { 'form': user_register_form }
        return render(request, 'Usermanagement/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

@login_required(login_url='/blog/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect('Blog:blog_index')
    else:
        return HttpResponse('no authority')

@login_required(login_url='/blog/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data

            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd['avatar']
            profile.save()
            # 带参数的 redirect()
            return redirect("Usermanagement:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'Usermanagement/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")