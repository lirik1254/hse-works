import json

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from custom_auth.tasks import redis_client
from .models import UserProfile
from .forms import UserProfileForm, UserEditForm


@login_required
def user_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль успешно сохранен.")
            return redirect("user_profile")  # Перезагрузка страницы после сохранения

    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    cf_data = {}
    if user_profile.codeforces_handle:
        cf_data = json.loads(redis_client.get(user_profile.codeforces_handle))

    return render(
        request,
        "user_profiles/profile.html",
        {"user_form": user_form, "profile_form": profile_form, "cf_data": cf_data}
    )
