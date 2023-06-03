from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.core.paginator import Paginator
from .forms import UserRegistrationForm, LoginForm, CreatePostForm
from .models import *

# TODO: Подготовить все представления для всех страниц
# TODO: Возможность пользователям менять изображения
# TODO: Возможность менять пароль
# TODO: Если изображения нет- стоковое (ограничения на размер изображения)

def response(request):
    page=1
    if request.GET.get('page'):
        page = request.GET.get('page')
    if request.GET.get('tag'):
        tag = request.GET.get('tag')
        posts = Post.objects.all().select_related('creator').filter(tag__name=tag)
    else:
        posts = Post.objects.all().select_related('creator')
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)
    return render(request, 'posts/main.html', {'page_obj':page_obj})


def show_categories(request):
    return render(request, template_name='posts/view_on_tags.html')


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'posts/main.html')
    
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST)
        if post_form.is_valid():
            print(post_form.data)
            new_post = post_form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
            post_form.save_m2m()
            return HttpResponseRedirect(reverse('main'))
    
    else:
        post_form = CreatePostForm()
    return render(request, 'posts/main.html', {'post_form': post_form})


def profile_view(request, name,pk):
    if request.GET.get('tag'):
        tag = request.GET.get('tag')
        posts = Post.objects.all().filter(creator=pk, tag__name=tag)
    else:
        posts = Post.objects.all().filter(creator=pk)
    post_form = CreatePostForm()
    user = User.objects.get(id=pk, username=name)
    
    return render(request, 'profile/profile_view.html', {'creator':user, 'posts':posts, 'post_form':post_form})

class PostDetails(DetailView):
    model = Post
    template_name = 'posts/detail_post.html'
    context_object_name = 'post'