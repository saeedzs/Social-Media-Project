from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse 
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
# def user_login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(
#                 request,username=data['username'],password=data['password'])
#             if user is not None:
#                 login(request,user)
#                 return redirect('index')
#             else:
#                 messages.error(request, "Invalid username or password.")
#                 return redirect('login')
#     else:
#         form = LoginForm()
#     return render(request, 'users/login.html', {'form': form})

@login_required
def index(request):
    current_user = request.user
    post_id = request.POST.get('post_id')
    posts = Post.objects.filter(user=current_user).order_by('-created')
    return render(request, 'users/index.html', {'posts':posts } )

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit = False)
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             Profile.objects.create(user=new_user)
#             return render(request,'users/register_done.html')
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'user_form': user_form})

class UserRegisterationView(UserPassesTestMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def test_func(self):
        # Only allow users who are NOT authenticated
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        # Redirect logged-in users away from the registration page
        return redirect('index')  # or settings.LOGIN_REDIRECT_URL
    
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
        data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            #return redirect('index') # Redirect to profile dashboard
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'users/edit.html', {'user_form': user_form, 'profile_form':profile_form })
    
