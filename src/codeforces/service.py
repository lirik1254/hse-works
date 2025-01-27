from .client import get_user_info
from .utils.time_utils import get_registration_time, get_last_seen_time


def get_user_dict(github_handle):
    """
    По гитхаб хендлу возвращает основную информацию о пользователе
    """
    user_info_dict = dict()

    response = get_user_info(github_handle)['result'][0]

    dict_addition(user_info_dict, 'handle', response, 'response')
    dict_addition(user_info_dict, 'rating', response, 'rating')
    dict_addition(user_info_dict, 'max_rating', response, 'maxRating')
    dict_addition(user_info_dict, 'friend_count', response, 'friendOfCount')
    dict_addition(user_info_dict, 'title_photo', response, 'titlePhoto')
    dict_addition(user_info_dict, 'organization', response, 'organization')
    dict_addition(user_info_dict, 'rank', response, 'rank')
    dict_addition(user_info_dict, 'max_rank', response, 'maxRank')

    if 'lastOnlineTimeSeconds' in response:
        user_info_dict['last_online_time'] = get_last_seen_time(response['lastOnlineTimeSeconds'])
    if 'registrationTimeSeconds' in response:
        user_info_dict['registration_date'] = get_registration_time(response['registrationTimeSeconds'])

    return user_info_dict


def dict_addition(user_info_dict, dict_key, response, response_key):
    if response_key in response:
        user_info_dict[dict_key] = response[response_key]



