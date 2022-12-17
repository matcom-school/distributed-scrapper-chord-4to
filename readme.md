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

# Ejemplo
### Descripción
Se inicia el servidor implementado con el módulo de python `http.server` y 5 nodos más (1,4,6,7,16), desde 
el navegador se pregunta por "http://localhost:9100" y "http://localhost:8000" simultaneamente con hash 10 y
29 respectivamente. Los encargados de descargar y almacenar en cache según chord son los nodos 16 y 1 

### Salida del server
```bash
Deamon listen to localhost:8999
Deamon listen to localhost:9004
.............. 4 finish start ......................
Deamon listen to localhost:9001
1 init_finger_table ................
1 init_finger_table .........finsih
Deamon listen to localhost:9007
Deamon listen to localhost:9006
.............. 1 finish start ......................
Deamon listen to localhost:9016
7 init_finger_table ................
7 init_finger_table .........finsih
.... Server ready open http://localhost:9100 ........
.............. 7 finish start ......................
.........1 stabilize .............
6 init_finger_table ................
6 init_finger_table .........finsih
.............. 6 finish start ......................
16 init_finger_table ................
16 init_finger_table .........finsih
.............. 16 finish start ......................
.........4 stabilize .............
1 download http://localhost:8000 with hash 29
1 ERROR with http://localhost:8000
127.0.0.1 - - [20/Jun/2021 17:16:09] "GET /?seach=%3A8000 HTTP/1.1" 200 -
.........6 stabilize .............
16 download http://localhost:9100 with hash 10
127.0.0.1 - - [20/Jun/2021 17:16:10] "GET / HTTP/1.1" 200 -
16 finish with http://localhost:9100
.........7 stabilize .............
127.0.0.1 - - [20/Jun/2021 17:16:11] "GET /?seach=%3A9100 HTTP/1.1" 200 -
.........1 stabilize .............
```
