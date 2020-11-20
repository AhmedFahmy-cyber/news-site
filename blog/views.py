from django.shortcuts import render ,reverse, redirect
from .models import *
from django.views import View
from django.views.generic import DetailView ,ListView ,UpdateView ,DeleteView ,FormView
from .forms import PostForm ,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class Home(ListView):

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    
    # def get(self,request):
    #     posts = Post.objects.all()
    #     template = 'blog/home.html',
    #     context = {
    #         'posts':posts , 
    #     }
    #     return render (request , template , context)

# @method_decorator(never_cache, name='dispatch')
# @method_decorator(login_required, name='dispatch')    
# @method_decorator(login_required ,name='dispatch' )
class Dashboard(View):
    def get(self ,request ,*args,**kwargs):

        view = Home.as_view(
            template_name = 'blog/admin_page.html'
        )
        return view(request ,*args,**kwargs)   


class PostDisplay(DetailView):

    model = Post
    

    def get_object(self):
        object = super(PostDisplay ,self).get_object()
        object.view_count += 1
        object.save()
        return object

    # def get_context_data(self , **kwargs):

    #     context = super(PostDetail,self).get_context_data(**kwargs)
    #     context['comments'] = Comment.objects.filter(post=self.get_object())
    #     context['form'] = CommentForm
    #     return context

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.view_count += 1
    #     self.object.save()
    #     post = self.get_context_data(object=self.object)
    #     return render(request, 'blog/post_detail.html', post)
    
    def get_context_data(self, **kwargs):
        context = super(PostDisplay, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object()).order_by('-created_at')
        context['form'] = CommentForm(instance=self.request.user)
        return context    
        
class PostComment(FormView):   

    form_class = CommentForm
    template_name = 'blog/post_detail.html'
    
    def form_valid(self, form):
        form.instance.by = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        form.save()
        return super(PostComment, self).form_valid(form)
        
    def get_success_url(self):
         return reverse('blog:post_detail', kwargs={'pk':self.kwargs['pk']})

class PostDetail(View):
    
    def get(self ,request ,*args,**kwargs):
        
        view = PostDisplay.as_view()
        
        return view(request ,*args,**kwargs) 

    def post(self ,request ,*args,**kwargs):
    
        view = PostComment.as_view()
        
        return view(request ,*args,**kwargs)   


class PostCreate(View):

    def get(self , request):

        form = PostForm()
        
        return render (request , 'blog/post_form.html ' , {'form':form})
    def post(self , request):

        form = PostForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect ('blog:home')
        return render (request , 'blog/post_form.html ' , {'form':form})

class PostUpdate(UpdateView):
    
    model = Post
    fields = ['title' ,'category','content',]
    template_name = 'blog/post_update.html'


class PostDelete(DeleteView):

    model = Post
    success_url = reverse_lazy('blog:dashboard')
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'

