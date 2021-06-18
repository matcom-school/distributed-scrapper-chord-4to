from bs4 import BeautifulSoup
from .color import Color




html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a  href="http://example.com/elsie" class="sister" id="link2 asdas sadas ">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they  lived == at the bottom of a well.</p>

<p class="story">...</p>
"""
class Parser:

    def __init__(self , html_Doc):
        self.documento = html_Doc
        self.soup = BeautifulSoup(html_Doc, 'html.parser')
        self.formato = self.soup.prettify()
    
    def IsUrl(self,text):
        url=[]
        for link in self.soup.find_all():
            href=(link.get('href')) 
            if(href != None):
                url.append(href)
                
            ref=(link.get("ref"))
            if(ref != None):
                url.append(ref)
        return text in url
    
    def comentarios(self,string,Color):

        aux = string.split('"')
        devo=[]
        for i in range(len(aux)):
            if(i%2 !=0 and not(self.IsUrl(aux[i]))) :
                devo.append(aux[i])

        for item in devo:
            
            string = string.replace('"' +item + '"' , Color.comentario('"' +item + '"'))

        return string 

    



    def Url (self,text,Color):
        url=[]
        for link in self.soup.find_all():
            href=(link.get('href')) 
            if(href != None and not(href in url)):
                
                url.append(href)
                
            ref=(link.get("ref"))
            if(ref != None  and not(ref in url)):
                url.append(ref)

        linea = text.split("\n")
        aux=""    
        for lin in linea :    

            for item in url:
                if(item in lin):
                    posicion = lin.index(item)
                    cadena =lin[posicion-1: posicion + len(item)+1]
                    lin= lin.replace(cadena , Color.Url(cadena))  
            aux = aux + lin +   "\n"       
        return aux
    
    def angulares(self , text,Color):
        head= ""

        for item in text :
            if item != "<" and item != ">" and item != "/":
                head = head + item 

        if('</' in text):

            text = text.replace("</" , Color.angulares("</")) 
            text = text.replace(head , Color.tag(head))

        else:
            if ('<' in text):
                text = text.replace("<" , Color.angulares("<")) 
                text = text.replace(head , Color.tag(head))
        
       

        if('>' in text):
            text = text.replace('>',Color.angulares(">"))

        return text

    def iguales (self , text,Color):
        if("=" in text):
            posicion = text.index("=")
            cadena =text[:posicion+1]
            verde = Color.propiedades(cadena)

            text = text.replace(cadena , verde)
        return text


    

    def numero(self,text,Color):
        if(text.isdigit()):
            return Color.numero(text)  
        return text  


    #Metodo que devuelve en formato con colores
    def Main(self,Color):

        lineas = self.formato.split("\n")
        aux= ""    
        texto_plano = self.soup.get_text()
        
        for i in range(len(lineas)):
        
            if(lineas[i] in texto_plano):
                continue
            
            lineas[i] =self.comentarios(lineas[i],Color)    
            
            text = (lineas[i].split(" "))
            
            for j in range(len(text)):
                text[j] = self.angulares(text[j],Color)
                text[j] = self.iguales(text[j],Color)
                text[j] = self.numero(text[j],Color)
                aux = aux + text[j] + " " 
            lineas[i] = aux + "\n"
            aux = ""    
        texto = "".join(lineas) 

        url = self.Url(texto,Color)  
        espacio = self.Espacios(Color,url)
        return(self.tabs(Color,espacio))

    # Metodo que convierte los espacios en numero 
    def Espacios (self,Color,text):
        lineas= text.split("\n")
        salida=""
        count=0
        
        for linea in lineas:
            for item in linea:
                if(item == " "):
                    count = count + 1
                    continue
                if(count !=0):    
                    salida = salida + Color.espacios(count) + linea[count:len(linea)]+ "\n"
                    count=0 
                    break    
                salida = salida + linea + "\n"
                break
        return salida 


    


    #Metodo que convierte los saltos de linea en <b>
    def tabs(self,Color,text):
        lineas=text.split("\n")
        salida=""
        s = ""
        for item in lineas:
            s = "".join(item)
            salida = salida + s + Color.tabs() +""
        return salida       
   


