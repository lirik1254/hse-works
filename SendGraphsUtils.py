import time
import vk_api


def send_graphic(vk, attachment_path, peer_id):
    """Загружает и отправляет график в VK"""
    upload = vk_api.VkUpload(vk)

    # Загрузка изображения
    photo = upload.photo_messages(attachment_path)[0]
    attachment = f"photo{photo['owner_id']}_{photo['id']}"

    # Отправка изображения в беседу
    vk.messages.send(
        peer_id=peer_id,
        attachment=attachment,
        random_id=int(time.time())
    )