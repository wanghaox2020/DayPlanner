from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Profile

# Create your views here.


class ProfileView(DetailView):
    model = Profile
    template_name = "profilepage/user_profile.html"

    def get_context_data(self, *args, **kwargs):
        is_login = self.request.user.is_authenticated
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        if is_login:
            curr_user = get_object_or_404(Profile, user=self.request.user)
            context["curr_user"] = curr_user
        page_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        context["page_user"] = page_user
        return context