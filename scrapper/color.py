
class Color:
    def __init__ (self):
        pass

    def Green (self,text): return "\33[92m{}\033[00m".format(text)
    def Red (self,text): return "\33[91m{}\033[00m".format(text)
    def Blue (self,text): return "\33[34m{}\033[00m".format(text)
    def Violet (self,text): return "\33[95m{}\033[00m".format(text)
    
    def Url(self,text):
        return  "[" + (self.Blue(text)) + "]"
     
    def numero(self,text):
        return self.Red(text)


    def angulares(self,text):
         return (self.Blue(text))

    def comentario(self,text):
        return "{" + self.Violet(text) + "}"

        
    def propiedades(self,text):
        return "(" + (self.Green(text)) + ")"


    def texto(self,text):
        return  "(" + (self.Violet(text))  + ")" 

    #Metodo que coje los saltos de linea en <b>
    def tabs (self):
        return "\n"

    def tag(self,text):
        return "(" + self.Red(text ) + ")"

    #aki recibes la cantidad de espacios pa por si hay q replazarlo y saber cuantos son
    def espacios(self,count):
        return str(count)


          


