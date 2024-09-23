import os, requests, pyfiglet
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from time import sleep as t

def limpiar():
 so=os.name
 if so == 'nt':
  os.system('cls')
 else:
  os.system('clear')
limpiar()
init(autoreset=True)

def iniciar():
 r=pyfiglet.figlet_format("Dakster")
 print(f"""{r}
 {Fore.WHITE}{Style.BRIGHT}[1]{Fore.GREEN} Buscar Por Cedula de Identidad
 {Fore.WHITE}{Style.BRIGHT}[2]{Fore.GREEN} Buscar Por Nombre y Apellido
 """)

 x=input("Seleccionar Opcion -> ")
 if x == '1':
  cantidad = 1
  cedula = input("CEDULA DE IDENTIDAD -> ")
  name=''
 elif x == '2':
  name = input("NOMBRE Y APELLIDO -> ")
  cedula=''
  cantidad = int(input("CANTIDAD DE RESULTADOS A MOSTRAR -> "))
 else:
  print("Opcion Invalida...")
  t(3)
 print("")
 dt = 'https://www.dateas.com'
 url = 'https://www.dateas.com/es/consulta_venezuela'
 params = {'name': f'{name}', 'cedula': f'{cedula}'}
 headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.0'}
 r = requests.post(url, params=params, headers=headers)
 with open('found.txt', 'w') as f:
  f.write(r.text)
 names = []
 enlaces = []

 with open('found.txt', 'r') as f:
  ver = f.read()
  soup = BeautifulSoup(ver, 'html.parser')
  y = soup.find_all('td')
  for i in y:
   name = i.text
   a_tag = i.find('a')
   if a_tag:
    link = a_tag['href']
    if link not in enlaces:
     names.append(name)
     enlaces.append(link)

 info = []
 n = 0
 resultados = []
 en0=[]
 for a, b in zip(names, enlaces):
  link = dt + b
  if n <= cantidad - 1:
   en0.append(link)
   peticion = requests.get(link)
   with open('file.txt', 'w') as f:
    f.write(peticion.text)
   with open('file.txt', 'r') as f:
    ver = f.read()
    soup = BeautifulSoup(ver, 'html.parser')
    ff = soup.find_all('td')
    count = 0
    for i in ff:
     if count < 4:
      info.append(i.text)
      count += 1
     else:
      break
  n = n + 1
 n = 0
 nk=0
 for i in info:
  if n % 4 == 0:
   nombre = i
   cedula = info[n + 1]
   fecha_nacimiento = info[n + 2]
   ubicacion = info[n + 3]
   save = f"Enlace: {en0[nk]}" + f"\nNOMBRE: {nombre}\nCEDULA DE IDENTIDAD: {cedula}\nFECHA DE NACIMIENTO: {fecha_nacimiento}\nUBICACION: {ubicacion}\n"    
   formatted_output = f"{Fore.WHITE}{Style.BRIGHT}Enlace: {Fore.GREEN}{en0[nk]}\n{Fore.WHITE}NOMBRE: {Fore.GREEN}{nombre}\n{Fore.WHITE}CEDULA DE IDENTIDAD: {Fore.GREEN}{cedula}\n{Fore.WHITE}FECHA DE NACIMIENTO: {Fore.GREEN}{fecha_nacimiento}\n{Fore.WHITE}UBICACION: {Fore.GREEN}{ubicacion}\n{Fore.WHITE}"
   print(f"{Fore.GREEN}{Style.BRIGHT}{formatted_output}")
   resultados.append(save)
   resultados.append('\n')
   nk=nk+1
  n += 1

 if os.path.exists('resultados.txt'):
  os.remove('resultados.txt')

 for i in resultados:
  with open('resultados.txt', 'a') as f:
   f.write(i + '\n')
 os.remove('found.txt')
 os.remove('file.txt')
 input("Presione [ENTER] Para Continuar...")
 limpiar()
 iniciar()
try:
 iniciar()
except:
 print(f"{Fore.RED}{Style.BRIGHT}No encontrado..."); input()
 limpiar(); iniciar()
