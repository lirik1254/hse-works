import requests
from VKInteraction import vk
from PIL import Image, ImageDraw, ImageFont


def download_photo(url):
    # Скачиваем фото
    response = requests.get(url)
    if response.status_code == 200:
        with open('Photo/sticker.png', 'wb') as file:
            file.write(response.content)
        image = Image.open('Photo/sticker.png')
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            font = ImageFont.load_default()
        text = "Топ стикер за день"
        image_width, image_height = image.size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_position = ((image_width - text_width) // 2, 20)
        draw.text(text_position, text, font=font, fill="black")
        image.save('Photo/sticker.png')
    else:
        print("Не удалось скачать фото")


def upload_photo_to_server():
    upload_server = vk.photos.getMessagesUploadServer()
    with open('Photo/sticker.png', 'rb') as file:
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