óúíéá
# Proyecto Final de Sistams Distribuido 

El proyecto consta de un cliente html y un server implementado con el módulo de python 
`http.server`. Además al iniciar este server se levantan una serie de procesos que simularán
la red distribuida. En dicha red se encotrarán los nodos encargados de realizar el scrapper y 
el debido almacenamiento de las informaciones para evitar descargas multiples. La red fué 
implementada sobre la DHT chord, los request de descarga son enrutado mediante el hash de 
las urls y el algoritmo de busqueda del chord (osea cada nodo se encarga de descargar y guardar 
en su cache las urls cuyo hash reconoce el nodo chord como llaves que le pertencen almacenar). 
Los request ya procesados se almacenan junto con su hash, pues en el background de los procesos
antes expuestos se realizan periodicas estabilizaciones del anillo chord y reubicaciones de la
información. Los cambios en la red son provocados por dos escenarios; en caso de que algún 
proceso no responda a su llamado se asume caído, en tal caso se levanta un procesos que lo 
sustituya. Por otro lado; en caso de que todos los procesos se encuentre ocupados descargando 
en el momento que se requiere una nueva descarga, se levanta un nuevo proceso para que se 
encarge de dicha descarga. En ambos casos se agrega un id nuevo al sistema y se hace necesario
la actualización de las finger tables y la reubicacion de las tuplas en cache

# Como ejecutarlo
python3 main.py
Luego abrá en el navegador http://localhost:9100 
