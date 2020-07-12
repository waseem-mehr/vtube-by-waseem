from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from .forms import VideoForm,ImageForm,UserCreateForm
from .models import Video,Categorey,Like,Unlike,Commment,Reply,Views,UserModel
# Create your views here.

class Home(View):
    def get(self,request,*args,**kwargs):
        user=User.objects.get(id=request.user.id)
        if not UserModel.objects.filter(user=user):
            UserModel.objects.create(user=user)
        videos=Video.objects.all()
        categories=Categorey.objects.all()
        videos_info=[]
        for vid in videos:
            likes=Like.objects.filter(video=vid).count()
            views=Views.objects.filter(video=vid).count()
            video={
                'video':vid,
                'likes':likes,
                'views':views
            }
            videos_info.append(video)

        context={
            'videos':videos_info,
            'categories':categories
        }
        return render(request,'video_tube/home.html',context)
@login_required(login_url='/login/')
def video(request,pk):

    user=User.objects.get(pk=request.user.id)
    video=Video.objects.get(id=pk)
    cat=video.categorey
    categorey_videos=Video.objects.filter(categorey=cat).all()
    if not Views.objects.filter(user=user,video=video):
        Views.objects.create(user=user,video=video)
    profile=UserModel.objects.get(user=user)
    print(profile)
    if request.method=='POST':

        if 'like' in request.POST:
            if Unlike.objects.filter(video=video, user=profile):
                l = Unlike.objects.filter(video=video, user=profile)
                l.delete()
                return HttpResponseRedirect(f"/video/id={pk}")
            else:
                if not Like.objects.filter(video=video, user=profile):
                    Like.objects.create(video=video, user=profile)
                    return HttpResponseRedirect(f"/video/id={pk}")
                else:
                    l = Like.objects.filter(video=video, user=profile)
                    l.delete()
                    return HttpResponseRedirect(f"/video/id={pk}")
        elif 'unlike' in request.POST:
            if Like.objects.filter(video=video,user=profile):
                l = Like.objects.filter(video=video, user=profile)
                l.delete()
                return HttpResponseRedirect(f"/video/id={pk}")
            else:
                if not Unlike.objects.filter(video=video, user=profile):
                    Unlike.objects.create(video=video, user=profile)
                    return HttpResponseRedirect(f"/video/id={pk}")
                else:
                    l = Unlike.objects.filter(video=video, user=profile)
                    l.delete()
                    return HttpResponseRedirect(f"/video/id={pk}")
        elif 'comment' in request.POST:

            comment_txt=request.POST.get('comment_text')
            if not comment_txt.strip()=='':
                Commment.objects.create(comment_text=comment_txt,video=video,user=profile)
                return HttpResponseRedirect(f"/video/id={pk}")
        elif 'reply' in request.POST:
            comment_id=request.POST.get('comment_id')
            reply_text=request.POST.get('comment_reply')
            comment=Commment.objects.get(id=comment_id)
            reply=Reply.objects.create(comment=comment,user=profile,comment_text=reply_text)
            return HttpResponseRedirect(f"/video/id={pk}")


    likes=Like.objects.filter(video=video).count()
    unlikes=Unlike.objects.filter(video=video).count()
    views=Views.objects.filter(video=video).count()
    comments=Commment.objects.filter(video=video)
    comp_comments=[]
    for comment in comments:
        replies=Reply.objects.filter(comment=comment)
        c={
            'comment':comment,
            'reply':replies
        }
        comp_comments.append(c)
    context={
        'video':video,
        'likes':likes,
        'unlikes':unlikes,
        'views':views,
        'related_videos':categorey_videos,
        'comments':comp_comments,
        'total_comments':comments.count()
    }

    return render(request, 'video_tube/video_by_id.html',context)

class Category(View):
    def get(self,request,*args,**kwargs):
        id = self.kwargs.get('pk')
        cat=Categorey.objects.filter(id=id)
        cat_name=None
        for x in cat:
            cat_name=x
        videos=Video.objects.filter(categorey=cat_name)
        videos_info = []
        for vid in videos:
            likes = Like.objects.filter(video=vid).count()
            views=Views.objects.filter(video=vid).count()
            video = {
                'video': vid,
                'likes': likes,
                'views':views
            }
            videos_info.append(video)

        context = {
            'videos': videos_info,

        }

        return render(request,'video_tube/category_wise.html',context)
@login_required(login_url='/login/')
def Userprofile(request,pk):
    profile=UserModel.objects.get(id=pk)
    videos=Video.objects.filter(user=profile)
    total_likes=0
    total_views=0
    videos_info = []
    for vid in videos:
        likes = Like.objects.filter(video=vid).count()
        views = Views.objects.filter(video=vid).count()
        total_likes=total_likes+likes
        total_views=total_views+views
        video = {
            'video': vid,
            'likes': likes,
            'views': views
        }
        videos_info.append(video)
    context={
        'videos':videos_info,
        'total_video':videos.count(),
        'user':profile,
        'total_likes':total_likes,
        'total_views':total_views,

    }
    return render(request,'video_tube/user_profile.html',context)
@login_required(login_url='/login/')
def profile(request):
    user=request.user.id
    user=User.objects.get(id=user)
    profile=UserModel.objects.get(user=user)
    videos=Video.objects.filter(user=profile)
    total_likes=0
    total_views=0
    videos_info = []
    for vid in videos:
        likes = Like.objects.filter(video=vid).count()
        views = Views.objects.filter(video=vid).count()
        total_likes=total_likes+likes
        total_views=total_views+views
        video = {
            'video': vid,
            'likes': likes,
            'views': views
        }
        videos_info.append(video)
    if request.method=='POST':
        if 'edit' in request.POST:
            form = ImageForm(request.POST, request.FILES,instance=profile)
            if form.is_valid():
                prof = form.save(commit=False)
                prof.user = user
                prof.save()

    context={
        'videos':videos_info,
        'total_video':videos.count(),
        'user':profile,
        'total_likes':total_likes,
        'total_views':total_views,
        'change_image_form':ImageForm(instance=profile)
    }
    return render(request,'video_tube/my_profile.html',context)

class UploadView(View):
    def post(self,request,*args,**kwargs):
        user = request.user.id
        user = User.objects.get(id=user)
        user_profile = UserModel.objects.get(user=user)
        error=True
        if 'upload' in request.POST:

            if request.method == 'POST':
                form = VideoForm(request.POST, request.FILES)
                if form.is_valid():

                    profile = form.save(commit=False)
                    profile.user = user_profile
                    profile.save()



            return HttpResponseRedirect(f'/?error={error}')

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,'video_tube/login.html')
    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            if 'login' in request.POST:
                user_name=request.POST.get('user_name').strip()
                user_password=request.POST.get('user_password').strip()
                user=authenticate(request,username=user_name,password=user_password)

                if user is not None:
                    login(request,user)
                    return redirect('/')
                else:

                    messages.warning(request, 'Username Or Password not matched.')
                    return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/login/')

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            context={
                'user_form':UserCreateForm()
            }
            return render(request,'video_tube/signup.html',context)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        user=UserCreateForm(request.POST)
        if user.is_valid():
            user.save()
            return HttpResponseRedirect('/login')
        else:
            context={
                'errors':user.errors
            }
            return render(request,'video_tube/signup.html',context)
