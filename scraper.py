# Librerias:
import requests as req
import lxml.html as html
# Para la casi ultima clase
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'
# Cambiar este codigo a otro que me genere todas las urls:
XPATH_LINK_TO_ARTICLE = '//div[@class = "flex-grow-1 mr-5"]//div[@class = "news V_Title_Img"]/a/@href'
XPATH_TITLE = '//div[@class = "wrap-info"]/h1/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "news empresasSect"]//div[@class = "html-content"]//text()'


def parsed_notice(link, today):
    try:
        response = req.get(link)
        if response.status_code == 200:
            #Traer el doc html:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                # Devuelde la lista pero solo queremos el titulo
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            #Guardar en archivo:
            # Ver función de f ""
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve) 


def pars_home():
    try:
        response = req.get(HOME_URL)
        if response.status_code == 200:
            # El metodo content trae todo el documento html
            # El metodos decode permite no tener errores con caracteres especiales
            home = response.content.decode('utf-8')
            # Tranforma el contenido htlm para poder hacer spam
            parsed = html.fromstring(home)
            # El metodo parsed
            links_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_notice)

            #Variable para crear la carpeta de almacenamiento:
            today = datetime.date.today(),str('%d-%m-%Y')
            # Si no existe la carpeta una carpeta con la fecha
            # de hoy crearla:
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_notice:
                parsed_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)



def run():
    pars_home()

if __name__ == '__main__':
    run()