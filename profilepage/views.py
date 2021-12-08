from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from .models import Profile
from resources.days.models import FavoriteDay
from resources.venues.models import FavoriteVenue


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
        context["page_user"] = page_user
        userObject = User.objects.get(id=self.kwargs["pk"])
        context["userDayList"] = userObject.day_set.all().filter(is_active=True)
        context["favorite_day"] = FavoriteDay.objects.filter(user=userObject)
        context["favorite_venue"] = FavoriteVenue.objects.filter(user=userObject)

        return context


@transaction.atomic
def make_profile_private(requests):
    last_URL = requests.GET.get("last")
    user = requests.user
    user_profile = user.profile
    try:
        with transaction.atomic():
            user_profile.is_private = True
            user_profile.save()
    except IntegrityError:
        requests.session["Error_Message"] = ""
        return HttpResponseRedirect(last_URL)

    return HttpResponseRedirect(last_URL)


@transaction.atomic
def make_profile_public(requests):
    last_URL = requests.GET.get("last")
    user = requests.user
    user_profile = user.profile
    try:
        with transaction.atomic():
            user_profile.is_private = False
            user_profile.save()
    except IntegrityError:
        requests.session["Error_Message"] = ""
        return HttpResponseRedirect(last_URL)

    return HttpResponseRedirect(last_URL)
