import requests


def get_user_info(github_handle):
    """
    Получает сырые json данные о пользователе по api.
    (codeforce позволяет тянуть данные 1р в 2 сек)
    """
    url = f"https://codeforces.com/api/user.info?handles={github_handle}&checkHistoricHandles=false"
    response = requests.get(url)
    return response.json()

