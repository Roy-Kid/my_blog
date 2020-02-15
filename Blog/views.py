from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from .forms import *

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from .models import *

import markdown

from django.views.generic import ListView, DetailView

from django.contrib.auth.decorators import login_required

# Create your views here.

class Blog_index(ListView):

    model = ColumnPost

    template_name = 'Blog/blog_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['columns'] = ColumnPost.objects.all()
        context['articles'] = ArticlePost.objects.all()[:2]

        return context

class Column_detail(ListView):

    model = ArticlePost

    template_name = 'Blog/column_detail.html'


    # paginate_by = 10
    # page_kwarg = 'p' /list/?page=2 -> /list/?p=2

    # ordering = 'created_time'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["column"] =  ColumnPost.objects.get(name=self.kwargs['column_name'])
        context["articles"] = ArticlePost.objects.filter(column__name=self.kwargs['column_name'])
        
        return context

  #  def get_queryset(self):
  #      self.column = get_object_or_404(ColumnPost, name=self.kwargs['column_name'])
  #      return ArticlePost.objects.filter(column__name=self.column.name)
    
    
class Article_detail(DetailView):

    model = ArticlePost

    template_name = 'article_detail.html'

    context_object_name = 'articles'

    slug_url_kwarg = 'article_name'
    
    slug_field  = 'slug_title'

    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        article = ArticlePost.objects.get(slug_title=self.kwargs['article_name'])
        
        article.total_views += 1
        article.save(update_fields=['total_views'])
        article.body = markdown.markdown(article.body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', ])

        context['article'] = article
        
        return context


def article_delete(request, column_name, article_name):

    article = ArticlePost.objects.get(slug_title=article_name)

    article.delete()

    return redirect('Blog:column_detail', column_name)

@login_required(login_url='/blog/login')
def article_create(request):
    if request.method == 'POST':
        data = request.POST
        article_post_form = ArticlePostForm(data=data)


        if article_post_form.is_valid():


            new_article = article_post_form.save(commit=False)

            new_article.author = User.objects.get(id=request.user.id)

            if request.POST['column'] != 'none':
                new_article.column = ColumnPost.objects.get(id=request.POST['column'])
            new_article.save()

            return redirect('Blog:blog_index')

        else:
            print(data)
            return HttpResponse('error')

    else:

        article_post_form = ArticlePostForm()

        columns = ColumnPost.objects.all()

        context = {'article_post_form': article_post_form, 
                    'columns':columns,
                    'article': ArticlePost}

        return render(request, 'create.html', context)

