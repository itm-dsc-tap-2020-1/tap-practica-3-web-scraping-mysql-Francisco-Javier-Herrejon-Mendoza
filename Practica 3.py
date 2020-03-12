from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector as mysql

def avance():
    band=False
    conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='practica3' )
    operacion = conexion.cursor()
    operacion.execute( "SELECT * FROM enlaces" )
    for enlace, status in operacion.fetchall():
        if(status==0):
            stat=False
            break
        else:
            stat=True
    conexion.close()
    return stat

pagina=input("Introduce la pagina a analizar: ")

conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='practica3' )
operacion = conexion.cursor()
operacion.execute(f"INSERT IGNORE INTO enlaces values('{pagina}', '{0}')")
conexion.commit()
conexion.close()
url=urlopen(pagina)
bs=BeautifulSoup(url.read(), 'html.parser')
cont=1

while (avance()==False):
    print("\nExtrayendo enlaces de una pagina web")
    
    for enlaces in bs.find_all("a"):
        cadena=(enlaces.get("href"))
        conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='practica3' )
        operacion = conexion.cursor()
        try:
            operacion.execute(f"INSERT IGNORE INTO enlaces values('{cadena}', '{0}')")
            conexion.commit()
            conexion.close()
        except:
            print("")
        print("href: {}".format(enlaces.get("href")))
    print("\nFin de enlaces encontrados.\n")
    operacion.execute( "SELECT * FROM enlaces" )
    for enlace, status in operacion.fetchall():
        if(status==0):
            operacion.execute(f"UPDATE enlaces SET status='1' where enlace='{enlace}'")
            break
    try:
        nueva_url = urlopen(enlace)
        bs = BeautifulSoup(nueva_url.read(), 'html.parser')     
    except:
        print("")  
    conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='practica3' )
    operacion = conexion.cursor()
    operacion.execute(f"UPDATE enlaces SET status='1' where enlace='{pagina}'")
    conexion.commit()
    conexion.close()
    cont=cont+1
    conexion.close()
    
