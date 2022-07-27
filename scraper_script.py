#Librerias para el scraping:
import requests as requests
import lxml.html as html
import os
import datetime


# Variables constantes, cada variable es una expresión XPATH para elemento dentro del sitio:
HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//a[contains(@class,"kicker")]/@href'
XPATH_TITLE = '//div[@class="OpeningPostNormal"]//text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY ='//div[@class="html-content"]//text()'


# DEFINIMOS LAS FUNCIONES DEL PROGRAMA:

def get_title(link):
    '''
    Función get_title:
    Esta función se encarga de obtener el titulo de acuerdo al link proporcionado
    el cual se recibe como parametro.
    '''
    # 1 Separarémos por "/" y solo usaremos el ultimo que elemento 
    url = link.split('/')[-1]
    # 2 Separarémos por "-" y borraremos el ultimo elemento
    title_list=url.split('-')[:-1]
    # 3 Unirémos todo lo anterior para obtener e titulo
    title = " ".join(title_list)
    # 4 Retornamo el titulo:
    return(title)


# Función que obtiene los elementos de cada link generado por la función pars_home():

def parse_notice(link, today):
    '''
    Obtiene la información requerida aplicando las las expresiones XPATH al link de los parametros que recibe.
    
    Parametros:
    link:   Es el link al cual se busca aplicar la función.
    today:  Es la fecha en la cual se esta realizando o ejecutando la función.
   
    Genera las siguientes variables internas:
    title:     Almacena el titulo de la noticia
    name_file: Almacena el nombre del archivo el cual es una concatenación de la variable name y los primeros dos strins del link
    summary:   Almacena un resumen de la noticia
    body:      Almacena el cuerpo de la noticia.
    
    Tranforma las convierte en un archivo tipo .txt, por cada ejecución de la función.   
    '''
    name = link[-2:]
    
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = str(get_title(link)).capitalize()
                y = int(title.find(' '))
                name_file = name + title[:y]
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)  

            except IndexError:
                return

            with open(f'{today}/{name_file}.txt', 'w', encoding='utf-8') as f:
                f.write('Titulo: ')
                f.write(title)
                f.write('\n\n')
                f.write('Resumen: ')
                f.write(summary)
                f.write('\n\n')
                f.write('Cuerpo: ')
                for p in body:
                    f.write(p)
                    f.write('\n')
                f.write('\n\n\n')
                f.write(f'Link de la noticia: {link}')
        
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)



# Función que obtiene los links de las noticias del periodico:
def pars_home():
    '''
    Toma la variable contante global; HOME_URL: Almacena el URL de la pagina principal del sitio
    y extrae todos los links de las noticias del sitio y los almacena en la variable:
    
    links_to_notice: Lista de links del sitio.
    
    Posteriormente crea una carpeta con a fecha de ejecución y en un ciclo for aplica llama a
    la función parse_home(), para pasar como parametro todos los links del sitio y guardar dentro de la carpeta creada
    todas la noticias en formato tipo.txt.
    '''
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)



def run():
    pars_home()

if __name__ == '__main__':
    run()
