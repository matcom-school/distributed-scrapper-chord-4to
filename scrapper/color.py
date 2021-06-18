
class Color:
    def __init__ (self):
        pass
    
    @staticmethod
    def yellow(text): return "\33[93m{}\033[00m".format(text)
    @staticmethod
    def blueBack(text): return "\33[44m{}\033[00m".format(text)
    @staticmethod
    def blue(text): return "\33[94m{}\033[00m".format(text)
    @staticmethod
    def red(text): return "\33[91m{}\033[00m".format(text)
    @staticmethod
    def green(text): return "\33[92m{}\033[00m".format(text)


    
    def Green (self,text): return "\33[92m{}\033[00m".format(text)
    def Red (self,text): return "\33[91m{}\033[00m".format(text)
    def Blue (self,text): return "\33[34m{}\033[00m".format(text)
    def Violet (self,text): return "\33[95m{}\033[00m".format(text)
    
    def Url(self,text):
        return f'[a]{text}[/a]'
     
    def numero(self,text):
        return f'[g]{text}[/g]'

    def angulares(self,text):
        if text == '<': text = '&lt;'
        elif text == '>': text = '&gt;'
        elif text == '</': text = '&lt;/'
        elif text == '/>': text = '/&lt;'
        return f'[gr]{text}[/gr]'

    def propiedades(self,text):
        return text
    
    def comentario(self,text):
        return f'[r]{text}[/r]'

    def texto(self,text):
        return f'[r]{text}[/r]'  

    #Metodo que coje los saltos de linea en <b>
    def tabs (self):
        return "<br/>"

    def tag(self,text):
        return f'[b]{text}[/b]'
    #aki recibes la cantidad de espacios pa por si hay q replazarlo y saber cuantos son
    def espacios(self,count):
        return '&nbsp;'*count


          


