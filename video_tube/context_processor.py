from .forms import VideoForm
def videoform(request):
    context={
        'video_form': VideoForm
    }
    return context