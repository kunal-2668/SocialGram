from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.

#*******************************************************
# Custom Decorator

def check_profile(view):
    def wrapper(request,*args,**kwargs):
        user = request.user.id
        if Profile.objects.filter(user=user):
            return view(request,*args,**kwargs)
        else:
            return redirect("UserApp:create_profile") 
    return wrapper

#*******************************************************

@check_profile
@login_required(login_url='AuthApp:login')
def new_post(request,user):
    if request.method == 'POST':
        post_title = request.POST['post_title']
        post = request.FILES['post']
        user = request.user
        profile = user.Profile

        created = Posts.objects.create(post_title=post_title,post=post,user=user,profile=profile)
        if created:
            return redirect('UserApp:home')
        else:
            messages.error(request,"Something went wrong!!")
            return redirect('UserApp:home')
    else:
        return render(request,'NewPost.html')


@check_profile
@login_required(login_url='AuthApp:login')
def home(request):
    user = request.user
    posts = []
    if len(user.Profile.following.all()) > 0:
        for user in user.Profile.following.all():
            for post in Posts.objects.filter(Q(user=user) | Q(user = request.user)):
                    posts.append(post)
        context = {
            'data':posts
        }
    else:
        post = [post for post in Posts.objects.filter(user = request.user)]

        context = {
            'data':post
        }
    return render(request,'index.html',context)


def HomeByTitle(request,slug):
    url = slug
    return redirect('UserApp:HomeByTitle',slug = url)


@login_required(login_url='AuthApp:login')
def create_profile(request):
    if request.method == 'GET':
        if Profile.objects.filter(user = request.user.id).exists():
            return redirect("UserApp:home")
        else:
            return render(request,'createprofile.html')
    else:
        user = request.user
        profilePhoto = request.FILES['profilePhoto']

        Profile.objects.create(user = user,profilePhoto=profilePhoto)
        return redirect("UserApp:home")



@check_profile
def profile_page(request,user):
    data = get_object_or_404(User,username=user)
    return render (request,'profilePage.html',{'data':data})


@login_required(login_url='AuthApp:login')
def delete_Comment(request,id,slug):
    comment = Comments.objects.get(id=id)
    if request.user == comment.user:
        comment.delete()
        # url = "#"+comment.Post.post_slug
        # return redirect(f'/{url}')
        return redirect('UserApp:PostView',slug = slug)


@check_profile
def postView(request,slug):
    data = Posts.objects.get(post_slug= slug)
    return render(request,'singlePost.html',{'data':data})


@check_profile
@login_required(login_url='AuthApp:login')
def addComment(request,slug):
    if request.method == 'POST':
        post = Posts.objects.get(post_slug=slug)
        comment = request.POST['comment']
        user = request.user
        profile = user.Profile
        
        created = Comments.objects.create(Post = post, Comment = comment, user = user, profile = profile)
        if created:
            return redirect('UserApp:PostView',slug = slug)
        else:
            return redirect("UserApp:home")
    else:
        return redirect("UserApp:home")
    

@check_profile
@login_required(login_url='AuthApp:login')
def addRemoveLike(request,slug):
    post = get_object_or_404(Posts,post_slug = slug)
 
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    url = "#"+slug
    return redirect(f'/{url}')


@check_profile
@login_required(login_url='AuthApp:login')
def FollowUser(request,profile):
    user = User.objects.get(username = profile)
    user_profile = get_object_or_404(Profile,user = user)

    current_user = request.user
    current_profile = get_object_or_404(Profile,user = current_user)

    if user_profile.followers.filter(id = current_user.id).exists():
        user_profile.followers.remove(current_user)
        current_profile.following.remove(user_profile.user)
    else:
        user_profile.followers.add(current_user)
        current_profile.following.add(user_profile.user)

    return redirect('UserApp:profile',user = user_profile.user)
       

@check_profile
def Discover(request):
    users = User.objects.all().exclude(username=request.user).order_by('?')
    posts = Posts.objects.all().order_by('?')
    return render(request,'discover.html',{'users':users,'posts':posts})


@check_profile
def searchUser(request):
    user = request.POST['search']
    exist = User.objects.filter(username__contains=user).exists()
    if exist:
        data = User.objects.filter(username__contains=user)
        return render(request,'searchpage.html',{'data':data})
    else:
        messages.info(request,'User not found!!')
        return render(request,'searchpage.html')
        

# @check_profile
def searchUseraxios(request,user):
    exist = User.objects.filter(username__contains=user).exists()
    if exist:
        data = User.objects.filter(username__contains=user)
        new_data = ""
        obj = {}
        for i in data:
            profile = i.Profile.profilePhoto.url
            user = i.Profile.user
            i = str(i)
            obj[i] = i
            new_data += f"""
                <div class="col-lg-4 center">
                <img src="{profile}" class="profilePhoto3" alt="">
                <div class="text-center">
                    <p class="fs-4">
                        {i}
                    </p>
                    <a href='/profile/{user}' class="btn btn-outline-primary">View Profile</a>
                </div>
            </div>
        """
        return JsonResponse(new_data,safe=False)
    else:
        data = f"""
            <h1 class="text-center mt-5">User Not Found!!</h1>
        """
        return JsonResponse(data,safe=False)
        
@check_profile
@login_required(login_url='AuthApp:login')
def editProfile(request):
    if request.method == 'GET':
        return render(request,'editProfile.html')
    else:
        data = Profile.objects.get(user = request.user)
        Photo = request.FILES['profilephoto']
        data.profilePhoto = Photo
        data.save()
        return redirect('UserApp:profile',user = request.user)


