import time
import requests
from multiprocessing.dummy import Pool # solo con multiprocessing funciona sin dummy

url = [
    'https://www.youtube.com',
    'https://google.com.pe',
    'https://falabella.com.pe',
    'https://outlook.live.com/mail/',
    'https://elcomercio.pe/'
]
start_time = time.time()
# creamos el numero de hilos que se ejecutarn en paralelo
## pool = Pool(1)
result = map(requests.get, url)
elapse_time = time.time() - start_time
r = list(result)
#pool.close()
#pool.join()
print(elapse_time)
print(list(result))