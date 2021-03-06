from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from blog.models import Post, Comment, Category
from blog.forms import PostForm

def post_list(request):
    posts = Post.objects.all().filter(published=True)
    categories = Category.objects.all()
    counter = posts.count()
    return render(request, 'blog/post_list.html', {'items':posts,
                                                   'categories':categories,
                                                   'counter':counter})

def categories(request,category_pk):
    posts = Post.objects.filter(category=category_pk)
    categories = Category.objects.all()
    counter = posts.count()
    return render(request, 'blog/post_list.html', {'items': posts,
                                                   'categories': categories,
                                                   'counter':counter})


def post_draft(request): #Refactor post list and post draft to one function
    posts = Post.objects.all().filter(published=False)
    categories = Category.objects.all()
    counter = posts.count()
    return render(request, 'blog/post_list.html', {'items': posts,
                                                   'categories': categories,
                                                   'counter':counter})

def publishing_post(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.published = True
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = Comment.objects.all().filter(post=post_pk)
    counter = comments.count()
    return render(request, 'blog/post_detail.html', {'post':post,
                                                     'comments':comments,
                                                     'counter':counter})

def post_new(request):
    if request.method == 'GET':
        form = PostForm
        return render(request, 'blog/post_new.html', {'form':form})
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk = post.pk)

def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = datetime.now()
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)

def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk).delete()
    return redirect('post_list')