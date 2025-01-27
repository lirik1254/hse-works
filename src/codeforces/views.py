from django.http import JsonResponse
from .service import get_user_dict


def codeforces_user_info(request, username):
    user_info = get_user_dict(username)

    if user_info is None:
        return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse(user_info)
