extensions = 'com'
two_points = '%3A'

def url_hashing(url : str, md) :
    urll, boolean = dns(url)    
    if boolean: return urll, hash(urll) % md 

    urll = urll if not urll[-1] == '.' else urll[0:-1] 
    u = urll + '.' + extensions
    return u, hash(u) % md
    
def dns(url : str) -> str :
    http, innertext = parser(url, 'http', inInnit )
    if innertext == url: twoPoint, backs, s = ':', '//', ''
    else:
        s, innertext = parser(innertext, 's', inInnit, requered= False)
        twoPoint, innertext = parser(innertext, ':', inInnit)
        backs, innertext = parser(innertext, '//', inInnit)

    innertext = space(innertext)
    try: 
        int(innertext[0]) 
        return http + s + twoPoint + backs + innertext, True
    except ValueError: pass
    
    if ':' in innertext: return http + s + twoPoint + backs + number_addr(innertext), True
     
    return http + s + twoPoint + backs + innertext, '.' in innertext and not innertext.index('.') == len(innertext) - 1

def number_addr(url):
    index = url.index(':')
    if index == 0: return 'localhost' + url

    return url

def space(text, reversed = False):
    for i in range(len(text)):
        if not text[i] == ' ': return text[i:]
    
    return text

def parser(text, patron, pred, requered=True):
    innertext = space(text)
    
    if pred(innertext, patron): return patron, innertext[len(patron):]
    elif not requered: return '', text

    return patron, innertext

def inInnit(text : str, patron):
    try: return text.index(patron) == 0
    except ValueError: return False


