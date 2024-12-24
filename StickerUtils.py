import requests
from VKInteraction import vk

def download_photo(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('sticker.png', 'wb') as file:
            file.write(response.content)
    else:
        print("Не удалось скачать фото")


def upload_photo_to_server():
    upload_server = vk.photos.getMessagesUploadServer()
    with open('sticker.png', 'rb') as file:
        upload_response = requests.post(upload_server['upload_url'], files={'photo': file}).json()
        return upload_response

def save_photo(upload_response):
    saved_photo = vk.photos.saveMessagesPhoto(
        photo=upload_response['photo'],
        server=upload_response['server'],
        hash=upload_response['hash']
    )[0]
    return saved_photo

def get_attachment(url):
    download_photo(url)
    upload_response = upload_photo_to_server()
    saved_photo = save_photo(upload_response)
    return f"photo{saved_photo['owner_id']}_{saved_photo['id']}"