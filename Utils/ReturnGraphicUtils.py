import vk_api


def return_graphic(vk, attachment_path):
    """Загружает и отправляет график в VK"""
    upload = vk_api.VkUpload(vk)

    # Загрузка изображения
    photo = upload.photo_messages(attachment_path)[0]
    attachment = f"photo{photo['owner_id']}_{photo['id']}"

    return attachment