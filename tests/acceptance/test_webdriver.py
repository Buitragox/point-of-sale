from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.product import Product
from models.sale import Sale
from utils.db import db
from random import randint

def login(driver: WebDriver, username: str, password: str):
    driver.get('http://localhost:5000')
    # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button')))
    form_username = driver.find_element(By.NAME, 'username')
    form_username.send_keys(username)
    form_password = driver.find_element(By.NAME, 'password')
    form_password.send_keys(password)
    form_password.submit()

def test_successful_sale(driver):
    login(driver, 'seller', 'seller')

    WebDriverWait(driver, 5).until(EC.title_is('Vendedor'))
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Registrar venta').click()

    WebDriverWait(driver, 5).until(EC.title_is('Register sale'))
    add_button = driver.find_element(By.ID, 'add-button')
    client_id = str(randint(100000, 999999))
    driver.find_element(By.NAME, 'client_id').send_keys(client_id)

    products: list[Product] = Product.query.all()
    total_price = 0

    for i, product in enumerate(products):
        add_button.click()
        driver.find_element(By.ID, f'id-{i}').send_keys(str(product.product_id))
        driver.find_element(By.ID, f'amount-{i}').send_keys(1)
        total_price += product.product_price

    driver.find_element(By.ID, 'submit-sale').click()

    flash_text = driver.find_element(By.CSS_SELECTOR, "strong").text

    assert flash_text == "Venta exitosa"

    sale = db.session.query(Sale).filter(Sale.client_id == client_id).first()
    assert sale.sale_price == total_price


def test_add_seller(driver):
    login(driver, 'admin', 'admin')

    WebDriverWait(driver, 5).until(EC.title_is('Administrador'))
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Agregar vendedor').click()

    credential = 'new_seller'

    WebDriverWait(driver, 5).until(EC.title_is('Add seller'))
    driver.find_element(By.NAME, 'username').send_keys(credential)
    driver.find_element(By.NAME, 'password').send_keys(credential)
    driver.find_element(By.NAME, 'pass_check').send_keys(credential)

    driver.find_element(By.CSS_SELECTOR, 'button').click()

    flash_text = driver.find_element(By.CSS_SELECTOR, "div.alert").text

    assert flash_text == "Se registró correctamente!"

    login(driver, credential, credential)

    WebDriverWait(driver, 5).until(EC.title_is('Vendedor'))

    assert 'Vendedor' == driver.title


def test_add_product(driver):
    login(driver, 'admin', 'admin')

    WebDriverWait(driver, 5).until(EC.title_is('Administrador'))
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Agregar producto').click()

    name = 'amazing product'
    amount = 10
    price = 10000

    WebDriverWait(driver, 5).until(EC.title_is('Add product'))
    driver.find_element(By.NAME, 'name').send_keys(name)
    driver.find_element(By.NAME, 'amount').send_keys(amount)
    driver.find_element(By.NAME, 'price').send_keys(price)

    driver.find_element(By.CSS_SELECTOR, 'button').click()

    flash_text = driver.find_element(By.CSS_SELECTOR, "strong").text

    assert "Se registró el producto" == flash_text

    driver.find_element(By.PARTIAL_LINK_TEXT, 'Regresar').click()
    WebDriverWait(driver, 5).until(EC.title_is('Administrador'))

    driver.find_element(By.PARTIAL_LINK_TEXT, 'Listar productos').click()
    WebDriverWait(driver, 5).until(EC.title_is('Products'))

    body = driver.find_element(By.TAG_NAME, 'tbody')
    rows = body.find_elements(By.TAG_NAME, 'tr')

    text_found = False
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells[1].text == name:
            text_found = True
            break

    assert text_found


def test_modify_user(driver):
    login(driver, 'admin', 'admin')

    WebDriverWait(driver, 5).until(EC.title_is('Administrador'))
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Modificar usuarios').click()

    WebDriverWait(driver, 5).until(EC.title_is('Modify users'))

    body = driver.find_element(By.TAG_NAME, 'tbody')
    rows = body.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells[0].text == 'tobedisabled':
            cells[3].find_element(By.PARTIAL_LINK_TEXT, 'Activar / Desactivar').click()
            break

    login(driver, 'tobedisabled', 'tobedisabled')

    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'strong')))
    WebDriverWait(driver, 5).until(EC.url_contains('login'))
    flash_text = driver.find_element(By.CSS_SELECTOR, "strong").text

    assert "Usuario deshabilitado" == flash_text
