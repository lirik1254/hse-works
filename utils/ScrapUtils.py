import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from utils.CaptchaUtils import pass_capcha

# Обрабатываем капчу, если она присутствует на странице
def handle_captcha(driver):
    try:
        captcha_button = driver.find_element(By.CSS_SELECTOR, '.CheckboxCaptcha-Button')
        ActionChains(driver).move_to_element(captcha_button).click().perform()
    except Exception:
        print("Нет капчи")
    finally:
        time.sleep(5)

    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    if "captcha" in body_text:
        pass_capcha(driver)
        time.sleep(5)

# Получение списка ссылок на 250 лучших фильмов
def get_link_list(url, driver):
    driver.get(url)
    handle_captcha(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    base_url = "https://www.kinopoisk.ru"
    links = soup.find_all('a', class_='base-movie-main-info_link__YwtP1')

    return [urljoin(base_url, link['href']) for link in links]

# Получчение отзывов для фильма
def parse_movie_text(movie_url, driver):
    driver.get(movie_url)
    handle_captcha(driver)

    # Скроллинг страницы (необходим, поскольку отзывы находятся внизу карточки фильма
    # и подгружаются динамически)
    for i in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    reviews_dict = {}
    try:
        review_sections = driver.find_elements(By.CSS_SELECTOR, 'section.styles_root__644Yf')
        movie_title = driver.find_element(By.CSS_SELECTOR, 'span[data-tid="75209b22"]').text.strip()

        # Получаем текст отзыва, заголовок, тональность из соответствующих тегов/классов
        for section in review_sections:
            try:
                review_title = section.find_element(By.CSS_SELECTOR, 'h4.styles_title__utMMO').text.strip()
                review_text = section.find_element(By.CSS_SELECTOR, '.styles_text__AYoL6').text.strip()
                section_class = section.get_attribute('class')

                review_type_label = "neutral"
                if "styles_rootNegative" in section_class:
                    review_type_label = "negatives"
                elif "styles_rootPositive" in section_class:
                    review_type_label = "positives"

                reviews_dict.setdefault(movie_title, {'positives': [], 'negatives': [], 'neutral': []})
                full_review_text = f"{review_title} {review_text}"
                reviews_dict[movie_title][review_type_label].append(full_review_text)

            except Exception as inner_error:
                print(f"Ошибка при обработке секции: {inner_error}")

    except Exception as e:
        print(f"Ошибка при извлечении отзывов: {e}")

    return reviews_dict
