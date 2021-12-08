from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


def main():
    path = '/Users/cesarisaacgonzaleznaranjo/chromedriver'
    driver = webdriver.Chrome(path)
    url = 'https://www.latamairlines.com/mx/es/ofertas-vuelos?dataFlight=%7B%22tripTypeSelected%22%3A%7B%22label%22%3A%22Ida%20y%20Vuelta%22%2C%22value%22%3A%22RT%22%2C%22isHandledExternally%22%3Afalse%7D%2C%22cabinSelected%22%3A%7B%22label%22%3A%22Economy%22%2C%22value%22%3A%22Economy%22%7D%2C%22passengerSelected%22%3A%7B%22adultQuantity%22%3A1%2C%22infantQuantity%22%3A0%2C%22childrenQuantity%22%3A0%7D%2C%22originSelected%22%3A%7B%22airportName%22%3Anull%2C%22countryName%22%3A%22M%C3%A9xico%22%2C%22cityName%22%3A%22Ciudad%20de%20M%C3%A9xico%22%2C%22airportIataCode%22%3A%22MEX%22%2C%22iata%22%3A%22MEX%22%7D%2C%22destinationSelected%22%3A%7B%22airportName%22%3Anull%2C%22countryName%22%3A%22Brasil%22%2C%22cityName%22%3A%22Sao%20Paulo%22%2C%22airportIataCode%22%3A%22GRU%22%2C%22iata%22%3A%22GRU%22%7D%2C%22dateGoSelected%22%3A%222021-12-23T19%3A30%3A00%22%2C%22dateReturnSelected%22%3A%222021-12-31T23%3A15%3A00%22%7D&sort=PRICE,asc'
    driver.get(url)
    # Introducir una demora
    delay = 10
    try:
        # introducir demora inteligente
        vuelo = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//li[@class="sc-eAudoH rtrCi"]')))
        print('La página terminó de cargar')
        info_vuelos = obtener_info(driver)
            
    except TimeoutException:
        print('La página tardó demasiado en cargar')
        info_vuelos = []
        driver.close()

    return print(info_vuelos)

  
def obtener_precios(vuelo):
    """
    Función que recibe como parámetro un vuelo y regresa un diccionario con las tarifas que tiene
    con sus respectivos precios
    """
    tarifas = {}
    precios = vuelo.find_elements(By.XPATH,'//ol[@class="sc-fepxGN kEDzSd"]//span[@class="sc-ijnzTp hUOrir displayAmount"]')
    precio_tarifa_light = precios[0].text
    precio_tarifa_plus = precios[1].text
    precio_tarifa_top = precios[2].text
    tarifas = {'Precio tarifa light': precio_tarifa_light,
                'Precio tarifa plus': precio_tarifa_plus,
                'Precio tarifa top': precio_tarifa_top,}
    return tarifas

  
def obtener_escalas(vuelo):
    """
    Función que toma como parámetro un vuelo y regresa infromación acerca de sus escalas
    """
    time.sleep(1)
    segmentos = vuelo.find_elements_by_xpath("//section[@class='sc-kIWQTW lnftOM']")
    info_escalas = []
    
    for segmento in segmentos:
        time.sleep(1)
        #Origen
        origen = segmento.find_element(By.XPATH,".//div[@class='sc-gLdKKF emZdpB']//span[@class='ariport-name']").text
        #Hora de Salida
        h_salida = segmento.find_element(By.XPATH,".//span[@class='time']").text
        #Destino
        destino = segmento.find_element(By.XPATH,".//div[@class='sc-gCUMDz kiipcI']//span[@class='ariport-name']").text
        #Hora de Llegada
        h_llegada = segmento.find_element(By.XPATH,".//div[@class='sc-gCUMDz kiipcI']//span[@class='time']").text
        #Duración del vuelo
        duracion_vuelo = segmento.find_element(By.XPATH,".//div[@class='sc-RWGNv jlZNft']/span[@class='time']").text
        #Número de vuelo
        num_vuelo = segmento.find_element(By.XPATH,".//div[@class='sc-iWadT gtvDXT']//div[@class='incoming-outcoming-title']").text
        #Modelo de avión
        modelo_avion = segmento.find_element(By.XPATH,".//span[@class = 'airplane-code']").text
        #Duración de la escala
        if segmento != segmentos[-1]:
            duracion_escala = segmento.find_element(By.XPATH,"//div[@class='sc-cAJUJo kOmCVk']/div/span[@class='time']").text
        else:
            duracion_escala = ''

        data_dic = {
            'origen':origen,
            'Hora de Salida':h_salida,
            'Destino':destino,
            'Hora de llegada':h_llegada,
            'Duración del vuelo':duracion_vuelo,
            'Número de vuelo':num_vuelo,
            'Modelo de avión':modelo_avion,
            'Duración de la escala':duracion_escala
        }
        info_escalas.append(data_dic)
    
    return info_escalas

  
def obtener_tiempos(vuelo):
    info_tiempos = []
    time.sleep(1)
    segmentos = vuelo.find_elements_by_xpath("//section[@class='sc-kIWQTW lnftOM']")
    for i,segmento in enumerate(segmentos):
        ti = vuelo.find_elements(By.XPATH,"//div[@class='sc-RWGNv jlZNft']//span[@class = 'time']")[i].text
        info_tiempos.append(ti)
    return info_tiempos
    

def obtener_info(driver):
    vuelos = driver.find_elements(By.XPATH,'//li[@class = "sc-eAudoH rtrCi"]')
    
    print(f'Se encontraron {len(vuelos)}  vuelos.')
    print('Iniciando el Scraping...')
    info = []
    for vuelo in vuelos:
        #clickear botón de escalas 
        vuelo.find_element(By.XPATH,".//div[@class = 'sc-blIhvV cUAiPA']/a").click()
        escalas = obtener_escalas(vuelo)
        #obtener los tiempos 
        tiempos = obtener_tiempos(vuelo)
        #Cerrar botón de escalas
        vuelo.find_element(By.XPATH,'//button[contains(@id,"dialog-close")]').click()
        #Clickear en vuelo para ver tarifas 
        time.sleep(.6)
        vuelo.click()
        precios = obtener_precios(vuelo)
        #Cerrar botón de precios
        driver.find_element(By.XPATH,"//button[@class = 'MuiButtonBase-root MuiButton-root MuiButton-text xp-Button-null MuiButton-textSizeSmall MuiButton-sizeSmall MuiButton-disableElevation']").click()
        info.append({'precios':precios, 'tiempos':tiempos, 'escalas':escalas})
        time.sleep(.4)
    return info

    

if __name__ == "__main__":
    main()
    
  




