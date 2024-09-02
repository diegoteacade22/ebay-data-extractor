from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configura el driver de Chrome
service = Service('/ruta/a/chromedriver')  # Cambia a la ruta donde tienes chromedriver
driver = webdriver.Chrome(service=service)

# Inicia sesión en eBay
driver.get('https://www.ebay.com/signin/')
# Aquí debes añadir los pasos para iniciar sesión automáticamente si no tienes una sesión guardada

# Lista para almacenar los datos
data = []

# Reemplaza con los enlaces de las órdenes
order_links = [
    'https://www.ebay.com/sh/ord/details?orderid=...1',
    'https://www.ebay.com/sh/ord/details?orderid=...2'
]

for link in order_links:
    driver.get(link)

    wait = WebDriverWait(driver, 10)
    date_sold = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Date sold"]/following-sibling::div'))).text
    sku = ""  # Si el SKU no está en esta página, deberás adaptarlo
    product = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Item title"]/following-sibling::div'))).text
    sell_price = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Item subtotal"]/following-sibling::div'))).text
    taxes = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Sales tax"]/following-sibling::div'))).text
    total_sell = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Order total"]/following-sibling::div'))).text
    commission = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Transaction fees"]/following-sibling::div'))).text
    shipping_fee = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Shipping label"]/following-sibling::div'))).text
    ad_fee = wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Ad Fee"]/following-sibling::div'))).text
    customer_phone = ""  # Agrega el XPATH para obtener el teléfono si está visible

    data.append({
        'DATE': date_sold,
        'SKU': sku,
        'PRODUCT': product,
        'SELL PRICE': sell_price,
        'IMPUESTOS': taxes,
        'TOTAL SEL': total_sell,
        'COMISION': commission,
        'SHIPPING FEE': shipping_fee,
        'AD FEE': ad_fee,
        'CUSTOMER CELLPHONE': customer_phone
    })

df = pd.DataFrame(data)
df.to_excel('ebay_report.xlsx', index=False)

driver.quit()
