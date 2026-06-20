from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Category, Article, Comment, Carousel
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import UserLogin, UserRegister, CommentForm, ArticleForm, CarouselForm
from django.urls import reverse_lazy
from django.db.models import Q


def index(request):
    categories = Category.objects.all()
    articles = Article.objects.all()
    carousels = Carousel.objects.all()
    context = {
        'categories': categories,
        'title': "Birinchi sayt",
        'articles': articles,
        'carousels': carousels
    }
    return render(request, "shop/index.html", context)


def category_by(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    articles = Article.objects.filter(category=category)
    context = {
        'categories': categories,
        'title': category.title,
        'articles': articles
    }
    return render(request, "shop/index.html", context)


def profile(request):
    context = {
        'title': 'Profile'
    }
    return render(request, "shop/profile.html", context)


class AddArticle(CreateView):
    model = Article
    template_name = 'shop/add_article.html'
    form_class = ArticleForm
    success_url = reverse_lazy('index')


def user_login(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLogin()
    context = {
        'form': form,
        'title': 'Kirish'
    }
    return render(request, 'shop/login_form.html', context)


def user_logaut(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegister(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegister()
    context = {
        'title': "Ro'yxatdan o'tish",
        'form': form
    }
    return render(request, "shop/register.html", context)


def save_comment(request, pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        article = get_object_or_404(Article, pk=pk)
        comment.article = article
        comment.save()
    return redirect('article_detail', pk)


class EditArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'shop/add_article.html'
    success_url = reverse_lazy('index')


def search(request):
    word = request.GET.get('q', '')
    articles = Article.objects.filter(
        Q(title__icontains=word) | Q(content__icontains=word)
    )
    context = {
        'articles': articles,
        'title': "Qidirish"
    }
    return render(request, 'shop/index.html', context)


class CarouselDetail(DetailView):
    model = Carousel
    template_name = 'components/carousel.html'


class AddCarousel(CreateView):
    model = Carousel
    form_class = CarouselForm
    template_name = 'carousel/form.html'
    success_url = reverse_lazy('carousel_list')


class EditCarousel(UpdateView):
    model = Carousel
    form_class = CarouselForm
    template_name = 'carousel/form.html'
    success_url = reverse_lazy('carousel_list')


class DeleteCarousel(DeleteView):
    model = Carousel
    template_name = 'carousel/confirm_delete.html'
    success_url = reverse_lazy('index')


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    categories = Category.objects.all()
    return render(request, 'shop/article_detail.html', {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
    })