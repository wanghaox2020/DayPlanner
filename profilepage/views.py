from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Profile

# Create your views here.

class ProfileView(DetailView):
    model = Profile
    template_name = 'profilepage/user_profile.html'
    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ProfileView, self).get_context_data( *args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context