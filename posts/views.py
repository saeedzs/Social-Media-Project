from django.shortcuts import render,get_object_or_404,redirect
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from django.http import JsonResponse
import json
from django.contrib import messages
from django.db.models import Prefetch

# Create your views here.
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('feed')
    
            
    else:
        form = PostCreateForm()
    return render(request,'posts/create.html',{'form':form})

@login_required
def feed(request): 
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post,id=post_id)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            # Redirect directly to the commented post's anchor
            return redirect(f"{request.path}#post-{post_id}")
    else:
        comment_form = CommentForm()

    posts = Post.objects.select_related('user__profile').prefetch_related(
        Prefetch('comment', queryset=Comment.objects.select_related('user__profile'))
    ).order_by('-created')
    logged_user = request.user
    return render(request, 'posts/feed.html', {'posts':posts , 'logged_user':logged_user, 'comment_form':comment_form})


@login_required
def like_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')

            if not post_id:
                return JsonResponse({'success': False, 'error': 'Missing post_id'}, status=400)

            post = get_object_or_404(Post, id=post_id)

            if post.liked_by.filter(id=request.user.id).exists():
                post.liked_by.remove(request.user)
                is_liked = False
            else:
                post.liked_by.add(request.user)
                is_liked = True

            return JsonResponse({
                'success': True,
                'is_liked': is_liked,
                'like_count': post.liked_by.count()
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = PostCreateForm(instance=post)

    return render(request, 'posts/edit.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user and request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')

    return redirect('feed')