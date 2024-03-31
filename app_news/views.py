from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import News, Categories


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class CategoriesView(ListView):
    model = Categories
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tezkor_yangiliklar'] = Categories.objects.get(name='Tezkor Yangiliklar')
        context['sport_xabarlari'] = Categories.objects.get(name='Sport Xabarlari')
        context['talim_yangiliklari'] = Categories.objects.get(name='Talim Yangiliklari')
        return context


class IndexView(ListView):
    model = News
    template_name = 'index.html'
    context_object_name = 'news'


class AddNewsView(LoginRequiredMixin, CreateView):
    template_name = 'news/add_news.html'
    model = News
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']
    success_url = '/'

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class NewsListView(ListView):
    model = News
    template_name = 'news/news.html'
    paginate_by = 3

    def get_queryset(self):
        if 'category' in self.request.GET:
            try:
                return News.objects.filter(news_category=self.request.GET['category'])
            except:
                return redirect('list_news')
        if 'keyword' in self.request.GET:
            try:
                return News.objects.filter(news_title__icontains=self.request.GET['keyword'])
            except:
                return News.objects.none()
        return News.objects.all()



class NewsDetailView(DetailView):
    model = News
    template_name = 'news/about_news.html'
    context_object_name = 'new'


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'news/edit_news.html'
    model = News
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']
    success_url = reverse_lazy('list_news')

    def test_func(self):
        news = News.objects.get(pk=self.kwargs['pk'])
        return self.request.user == news.news_author

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('list_news')
    template_name = 'news/confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(news_author=self.request.user)
