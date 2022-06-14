from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from . models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required


def dash(request):
    return render(request, 'blog/dash.html')



class PostListView(ListView,LoginRequiredMixin):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts' 
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)    
    


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)    
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False     


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url ='home/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 

@login_required
def about(request):
    return render(request,'blog/about.html',{'title':'About'})   