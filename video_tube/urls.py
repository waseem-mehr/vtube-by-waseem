from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'video_tube'
urlpatterns = [
    path('',login_required(views.Home.as_view(),login_url='/login/'), name='home'),
    path('video/id=<int:pk>/', views.video, name='video'),
    path('user/id=<int:pk>/', views.Userprofile, name='profile'),
    path('categorey/id=<int:pk>/',login_required(views.Category.as_view(),login_url='/login/'),name='category'),
    path('profile/',views.profile,name='profile'),
    path('upload/',login_required(views.UploadView.as_view(),login_url='/login/'),name='upload'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',login_required(views.logoutView,login_url='/login/'),name='logout'),
    path('signup/',views.SignUpView.as_view(),name='signup')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
