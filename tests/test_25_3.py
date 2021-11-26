import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from user_data import valid_email, valid_password

#Строка для запуска кода
# python -m pytest -v --driver Chrome --driver-path C:\\WebDriver\\chromedriver.exe test_25_3.py

def test_show_all_pets():
   # Вводим email, пароль,клик кнопки "Войти"
   pytest.driver.find_element_by_id('email').send_keys(valid_email)
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

   # Настраиваем неявные ожидания:
   pytest.driver.implicitly_wait(10)

   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

   # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
   images = pytest.driver.find_elements_by_xpath('//img[@class="card-img-top"]')
   names = pytest.driver.find_elements_by_xpath('//h5[@class="card-title"]')
   descriptions = pytest.driver.find_elements_by_xpath('//p[@class="card-text"]')

   # Проверяем, что на странице у питомцев есть имена, порода, возраст(не пустые строки):
   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0

def test_show_my_pets():
   # Вводим email, пароль,клик кнопки "Войти"
   pytest.driver.find_element_by_id('email').send_keys(valid_email)
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

   #Настраиваем переменную явного ожидания:
   wait = WebDriverWait(pytest.driver, 5)

   # Проверяем, что мы оказались на главной странице сайта,выждав 5с.
   assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME,'h1'), "PetFriends"))

   # Открываем страницу /my_pets.
   pytest.driver.find_element_by_css_selector('a[href="/my_pets"]').click()

   # # Проверяем, что мы оказались на  странице пользователя, выждав 5 с,проверяем наличие имени пользователя
   assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "25_3_1"))

   # Ищем в таблице все строки с полными данными питомцев (имя, порода, возраст, "х" удаления питомца):
   css_locator = 'tbody>tr'
   data_my_pets = pytest.driver.find_elements_by_css_selector(css_locator)

   # Ожидаем, что данные питомцев, найденных локатором css_locator, видны на странице:
   for i in range(len(data_my_pets)):
      assert wait.until(EC.visibility_of(data_my_pets[i]))

   # Ищем в таблице все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице:
   image_my_pets = pytest.driver.find_elements_by_css_selector('img[style="max-width: 100px; max-height: 100px;"]')
   for i in range(len(image_my_pets)):
      if image_my_pets[i].get_attribute('src') != '':
         assert wait.until(EC.visibility_of(image_my_pets[i]))

   # Ищем в таблице все имена питомцев и ожидаем,что видны на странице:
   name_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
   for i in range(len(name_my_pets)):
      assert wait.until(EC.visibility_of(name_my_pets[i]))

   # Ищем в теле таблицы все породы питомцев и ожидаем,что видны на странице:
   type_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')
   for i in range(len(type_my_pets)):
      assert wait.until(EC.visibility_of(type_my_pets[i]))

   # Ищем в теле таблицы все данные возраста питомцев и ожидаем,что видны на странице:
   age_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')
   for i in range(len(age_my_pets)):
      assert wait.until(EC.visibility_of(age_my_pets[i]))

   # Ищем на странице my_pets статистику, выделяем количество питомцев пользователя:
   all_statistics = pytest.driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text.split("\n")
   statistics_pets = all_statistics[1].split(" ")
   all_my_pets = int(statistics_pets[-1])

   # Проверяем, что количество строк в таблице my_pets равно количеству питомцев, указанному в статистике пользователя:
   assert len(data_my_pets) == all_my_pets

   # Проверяем, что хотя бы у половины питомцев есть фото:
   m = 0
   for i in range(len(image_my_pets)):
      if image_my_pets[i].get_attribute('src') != '':
         m += 1
   assert m >= all_my_pets/2

   # Проверяем, что у всех питомцев есть имя:
   for i in range(len(name_my_pets)):
      assert name_my_pets[i].text != ''

   # Проверяем, что у всех питомцев есть порода:
   for i in range(len(type_my_pets)):
      assert type_my_pets[i].text != ''

   # Проверяем, что у всех питомцев есть возраст:
   for i in range(len(age_my_pets)):
      assert age_my_pets[i].text != ''

   # Проверяем, что у всех питомцев разные имена:
   list_name_my_pets = []
   for i in range(len(name_my_pets)):
      list_name_my_pets.append(name_my_pets[i].text)
   set_name_my_pets = set(list_name_my_pets) # преобразовываем список в множество
   assert len(list_name_my_pets) == len(set_name_my_pets) # сравниваем длину списка и множества: без повторов должны совпасть

   # Проверяем, что в списке нет повторяющихся питомцев:
   list_data_my_pets = []
   for i in range(len(data_my_pets)): # отделяем от текстовых данных питомцев столбец "х" удаление питомцев
      list_data = data_my_pets[i].text.split("\n")
      list_data_my_pets.append(list_data[0]) # выбираем элемент с данными питомца и добавляем его в список
   set_data_my_pets = set(list_data_my_pets) # преобразовываем список в множество
   assert len(list_data_my_pets) == len(set_data_my_pets) # сравниваем длину списка и множества: без повторов должны совпасть