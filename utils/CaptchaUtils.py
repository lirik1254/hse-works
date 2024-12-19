import base64
import time

import requests
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

api_key = "709473c7de47eb3a7138749c8b6dbbc8"

# Создаёт со скриншота полного окна обрезанное изображение с капчей
# Пример в utils/cropped_image.png
def create_cropped_image(path):
    image = Image.open(path)
    left = 287
    top = 244
    right = 642
    bottom = 495
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save("utils/image/cropped_image.png")

# Создаёт задачу на 2captcha.com
def create_task():
    with open('utils/image/cropped_image.png', 'rb') as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

    task_data = {
        "clientKey": api_key,
        "task": {
            "type": "CoordinatesTask",
            "body": encoded_image,
        }
    }

    url = "https://api.2captcha.com/createTask"

    response = requests.post(url, json=task_data)
    task_id = 0

    if response.status_code == 200:
        response_data = response.json()
        task_id = response_data['taskId']
        return task_id
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return 0

# Получение координат для кликов для решения капчи
def get_coordinates(task_id):
    task_result_data = {
        "clientKey": api_key,
        "taskId": task_id
    }

    # URL API для получения результата задачи
    url = "https://api.2captcha.com/getTaskResult"
    status = "notReady"

    coordinates = []

    while status != "ready":
        response = requests.post(url, json=task_result_data)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('status') == 'ready':
                status = "ready"
                coordinates = response_data['solution']['coordinates']
                print(f"Coordinates: {coordinates}")
                return coordinates
            else:
                print("Task is not ready yet.")
                time.sleep(50)
        else:
            print("Проблема с обращению к капче")
            exit()

# Метод для прохождения капчи
def pass_capcha(driver):
    path = "utils/image/full_page_screenshot.png"
    driver.get_screenshot_as_file(path)
    create_cropped_image(path)

    task_id = create_task()
    if task_id == 0:
        print("Не удалось создать таску")
        exit()

    coordinates = get_coordinates(task_id)
    action = ActionChains(driver)

    for coord in coordinates:
        x = coord["x"]
        y = coord["y"]
        print(f"Clicking at: x={x}, y={y}")

        captcha_element = driver.find_element(By.CLASS_NAME, 'AdvancedCaptcha-ImageWrapper')
        action.move_to_element_with_offset(captcha_element, -174 + x, -97 + y).click().perform()

        time.sleep(3)

    driver.find_element(By.CLASS_NAME, 'CaptchaButton-SubmitContent').click()
