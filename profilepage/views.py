from django.contrib.auth.models import User
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

        page_user = get_object_or_404(Profile, user_id=self.kwargs["pk"])
        print(page_user)
        context["page_user"] = page_user

        userObject = User.objects.get(id=self.kwargs["pk"])
        print(userObject)
        context["userDayList"] = userObject.day_set.all().filter(is_active=True)

        return context
