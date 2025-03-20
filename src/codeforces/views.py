import json

from django.http import JsonResponse, Http404
from django.shortcuts import render

from user_profiles.models import UserProfile
from .service import get_user_dict
from custom_auth.tasks import redis_client
from django.contrib.auth.models import User


def codeforces_user_info(request, username):
    try:
        user = User.objects.get(username=username)
    except Exception:
        raise Http404("Пользователь не найден")

    try:
        user_profile = user.userprofile
    except Exception:
        user_profile = None

    user_data = {"user_firstname": user.first_name,
                 "user_lastname": user.last_name,
                 "user_registration": user.date_joined,
                 "user_last_seen": user.last_login}

    if user_profile:
        user_data['user_bio'] = user_profile.bio
        user_data['user_university_group'] = user_profile.university_group
        user_data['codeforces_handle'] = user_profile.codeforces_handle

    cf_data = {}
    if user_profile and user_profile.codeforces_handle:  # Проверяем, что user_profile не None
        redis_data = redis_client.get(user_profile.codeforces_handle)
        if redis_data:  # Проверяем, что данные не None
            cf_data = json.loads(redis_data)

    return render(request, "codeforces/participants_id.html", {"user_data": user_data, "cf_data": cf_data})


def participants(request):
    # Получаем всех пользователей из базы данных
    users = User.objects.all()

    participants_data = []

    for user in users:
        # Получаем профиль пользователя
        user_profile = UserProfile.objects.filter(user=user).first()

        # Если профиль существует, получаем ник и рейтинг, если они есть
        if user_profile:
            codeforces_handle = user_profile.codeforces_handle
            # Получаем рейтинг из Redis по никнейму Codeforces, если он есть
            rating = "-"
            if codeforces_handle:
                try:
                    rating = json.loads(redis_client.get(codeforces_handle))['rating']
                except Exception:
                    rating = "-"
        else:
            codeforces_handle = None
            rating = "-"

        participants_data.append({
            'username': user.username,
            'codeforces_handle': codeforces_handle,
            'rating': rating,
        })

    # Сортируем по убыванию рейтинга, если рейтинг не "-" (то есть это числовое значение)
    participants_data = sorted(participants_data, key=lambda x: (x['rating'] != "-", x['rating']), reverse=True)

    return render(request, 'codeforces/participants.html', {'participants_data': participants_data})

