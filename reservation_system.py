import os # para manipular paths
import json # para cargar archivos JSON
from datetime import datetime # para operar con objetos de fecha
from uuid import uuid4 # para generar IDs

# encuentra el path del archivo a cargar
def find_path(name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   return os.path.join(script_dir, name)

# carga el archivo en un objeto diccionario
def load_archive(path):
   # Abriendo config.json
   f = open(path)
   # Retorna .json como un diccionario
   archive = json.load(f)
   # Cierra el archivo .json
   f.close()
   return archive

# Clase para crear un objeto para cada reservación realizada
class Reservation():
   # validando que cada key exista, su value no esté vacío y sea del tipo correcto.
   def __init__(self, reservation_object):
      # nombre del cliente debe ser una cadena
      if 'client_name' in reservation_object:
         if type(reservation_object['client_name']) is not str or reservation_object['client_name']==None or reservation_object['client_name']=='':
            print("Nombre del cliente inválido; el campo no puede estar vacío y debe ser una cadena.")
            raise Exception
      else:
         print("El campo del nombre del cliente no puede estar vacío.")
         raise Exception
      self.client_name = reservation_object['client_name']
      
      # fecha de reservación debe estar en formato str %Y/%m/%d %H:%M:%S
      if 'reservation_date' not in reservation_object:
            print("El campo de la fecha y hora de la reservación no puede estar vacío.")
            raise Exception 
      try: self.reservation_datetime = datetime.strptime(reservation_object['reservation_date'], '%Y/%m/%d %H:%M:%S')
      except:
         print("El campo de la fecha y hora de la reservación debe estar escrito en el formato aaaa/mm/dd hh:mm:ss.")
         raise Exception
      # guarda la fecha separada de la hora
      self.reservation_date=self.reservation_datetime.date()
         
      # fecha de check in debe estar en formato str %Y/%m/%d %H:%M:%S
      if 'check_in' not in reservation_object:
         print("El campo de la fecha y hora del check-in no puede estar vacío.")
         raise Exception
      try:
         self.check_in = datetime.strptime(reservation_object['check_in'], '%Y/%m/%d %H:%M:%S')
         # guarda la hora de check in separada de la fecha
         self.check_in_hour = self.check_in.time()
      except:
         print("El campo de la fecha y hora del check-in debe estar escrito en el formato aaaa/mm/dd hh:mm:ss.")
         raise Exception
         
      # fecha de check out debe estar en formato %Y/%m/%d %H:%M:%S
      if 'check_out' not in reservation_object:
            print("El campo de la fecha y hora del check-out no puede estar vacío.")
            raise Exception
      try:
         self.check_out = datetime.strptime(reservation_object['check_out'], '%Y/%m/%d %H:%M:%S')
         # guarda la hora de check in separada de la fecha
         self.check_out_hour = self.check_out.time()
      except:
         print("El campo de la fecha y hora del check-out debe estar escrito en el formato aaaa/mm/dd hh:mm:ss.")
         raise Exception

      # genera duración de la estadía basado en check in y check out
      if (self.check_out.date()-self.check_in.date()).days>1:
         self.length_of_stay = str((self.check_out.date()-self.check_in.date()).days)+' días'
      else:
         self.length_of_stay = str((self.check_out.date()-self.check_in.date()).days)+' día'
   
      # número de huéspedes debe ser un entero
      if "number_of_guests" in reservation_object:
            if type(reservation_object['number_of_guests']) is not int or reservation_object['number_of_guests']==None or reservation_object['number_of_guests']=='':
               print("Número de huéspedes inválido; el campo no puede estar vacío y debe ser un número entero.")
               raise Exception
      else:
         print("El campo del número de huéspedes no puede estar vacío.")
         raise Exception
      self.number_of_guests = reservation_object['number_of_guests']

      # número de habitación debe ser un entero
      if 'room_number' in reservation_object:
         if type(reservation_object['room_number']) is not int or reservation_object['room_number']==None or reservation_object['room_number']=='':
            print("Número de habitación inválido; el campo no puede estar vacío y debe ser un número entero.")
            raise Exception
      else:
         print("El campo del número de habitación no puede estar vacío.")
         raise Exception
      self.room_number = reservation_object['room_number']

      # tipo de habitación debe ser una cadena
      if 'room_type' in reservation_object:
         if type(reservation_object['room_type']) is not str or reservation_object['room_type']==None or reservation_object['room_type']=='':
            print("Tipo de habitación inválido; el campo no puede estar vacío.")
            raise Exception
      else:
         print("El campo del tipo de habitación no puede estar vacío.")
         raise Exception         
      self.room_type = reservation_object['room_type']

      # las preferencias alimentarias deben ser una cadena
      if 'diet' in reservation_object:
         if type(reservation_object['diet']) is not str or reservation_object['diet']==None or reservation_object['diet']=='':
            self.diet = 'Sin preferencias'
         else: self.diet = reservation_object['diet']
      else: self.diet = 'Sin preferencias'
         
      # debe haber al menos 1 campo de contacto lleno, correo o teléfono (ambos str)
      if 'email' not in reservation_object and 'phone' not in reservation_object:
         print("El campo del contacto del cliente (correo o telf) no puede estar vacío.")
         raise Exception
      if 'email' in reservation_object:
         if reservation_object['email']!='' and reservation_object['email']!=None and type(reservation_object['email']) is str:
            self.email = reservation_object['email']
         else: self.email = 'n/a'
      else: self.email = 'n/a'
      if 'phone' in reservation_object:
         if reservation_object['phone']!='' and reservation_object['phone']!=None and type(reservation_object['phone']) is str:
            self.phone = reservation_object['phone']
         else: self.phone = 'n/a'
      else: self.phone = 'n/a'
      if self.email == self.phone:
         print("El campo del contacto del cliente (correo o telf) no puede estar vacío y debe ser una cadena.")
         raise Exception

      # el precio total debe ser un decimal
      if 'total_price' in reservation_object:
         if type(reservation_object['total_price']) is str or reservation_object['total_price']==None or reservation_object['total_price']=='':
            print("Precio total inválido; el campo no puede estar vacío y debe ser un número.")
            raise Exception
      else:
         print("El campo del precio total no puede estar vacio.")
         raise Exception
      self.total_price = float(reservation_object['total_price'])
      
      # el método de pago debe ser una cadena
      if 'payment_method' in reservation_object:
         if type(reservation_object['payment_method']) is not str or reservation_object['payment_method']==None or reservation_object['payment_method']=='':
               print("Método de pago inválido; el campo no puede estar vacío y debe ser una cadena.")
               raise Exception
      else:
         print("El campo del método de pago no puede estar vacio.")
         raise Exception
      self.payment_method = reservation_object['payment_method']
      
      # las notas adicionales deben ser una cadena
      if 'notes' in reservation_object:
         if type(reservation_object['notes']) is not str or reservation_object['notes']==None or reservation_object['notes']=='':
            self.notes = 'No hay notas adicionales.'
         else:
            self.notes = reservation_object['notes']
      else:
         self.notes = 'No hay notas adicionales.'
         
      # el estado de la reservación debe ser una cadena: Pendiente o Confirmado
      if 'reservation_status' in reservation_object:
         if (reservation_object['reservation_status']).lower()!='pendiente' and (reservation_object['reservation_status']).lower()!='confirmado':
               print("Estado de reservación inválido; el campo debe estar lleno con Pendiente o Confirmado.")
               raise Exception
      else:
         print("El campo del estado de la reservación no puede estar vacio.")
         raise Exception
      self.status= reservation_object['reservation_status']

      # genera y guarda ID
      self.id = str(uuid4())

      # genera key de número de reservaciones
      self.number_of_reservations=0

# función para crear lista de objetos de la clase Reservation
def reservation_list(arr):
   reservations = []
   for i in range(len(arr)):
      try:
         reservation = Reservation(arr[i])
         reservations.append(reservation)
      except:
         print("No se pudo crear el objeto %i.\n" %(i+1))
   print("Se cargó un total de %i/%i reservaciones exitosamente.\n" % (len(reservations), len(arr)))
   return reservations

# función para obtener el número de reservaciones por cliente
def get_reservations_per_client(arr):
   for i in range(len(arr)):
      cont=0
      name = getattr(arr[i], 'client_name')
      for j in range(len(arr)):
         if name==getattr(arr[j], 'client_name'):
            cont+=1
      setattr(arr[i],'number_of_reservations', cont)


# Quicksort
# esta implementación utiliza como pivote al último elemento de la lista,
# tiene un puntero para realizar un seguimiento de los elementos más pequeños
# o más grandes (según sea el orden) que el pivote.
# Al final de la función partition(), el puntero se intercambia con el pivote
# para generar números "ordenados" en relación con el pivote

# función para comparar elementos basado en múltiples criterios
def compare_elements(a, b, criteria, order):
    # compara elementos para cada criterio
   for i in criteria:
      if getattr(a,i) != getattr(b,i):
         if order == 0:
            # si el orden es ascendente, retorna True cuando el elemento a
            # es más pequeño que b (pivote) según el criterio que se esté evaluando
            return getattr(a,i)<getattr(b,i)
         # si el orden es descendente, retorna True cuando el elemento a
         # es más grande que b (pivote)
         return getattr(a,i)>getattr(b,i)
   return False
# función para encontrar la posición de partición
def partition(array, low, high, criteria, order):
   # escoge el primer elemento de derecha a izquierda como pivote
   pivot = array[high]
   # puntero para el mayor elemento
   i = low - 1
   # recorre todos los elementos y compara cada elemento con el pivote
   for j in range(low, high):
      if compare_elements(array[j], pivot, criteria, order):
         # si se encuentra un elemento más pequeño o más grande,
         # de acuerdo al order seleccionado, que el pivote,
         # se intercambia ese elemento con el mayor elemento señalado por i
         i = i + 1
         # intercambia elemento en i con elemento en j
         array[i], array[j] = array[j], array[i]
   # intercambia el pivote con el mayor elemento señalado por i
   array[i + 1], array[high] = array[high], array[i + 1]
   # retorna la posición donde se hizo la partición
   return i + 1
# función para ordenamiento Quicksort
def quickSort(array, low, high, criteria, order):
   if low < high:
      # encuentra el pivote tal que
      # elemento más pequeño que pivote a la izq (si asc) o a la derecha (si desc)
      # elemento más grande que pivote a la derecha (si asc) o a la izq (si desc)
      pi = partition(array, low, high, criteria, order)
      # llamada recursiva a la izquierda del pivote
      quickSort(array, low, pi - 1, criteria, order)
      # llamada recursiva a la derecha del pivote
      quickSort(array, pi + 1, high, criteria, order)

# Mergesort
# esta implementación fusiona dos sublistas de la lista para ordenar.
# la primera sublista es arr[l..m]
# la segunda sublista es arr[m+1..r]
def merge(arr, l, m, r, order):
   # calcula los tamaños de las dos sublistas
   n1 = m - l + 1 # tamaño de la sublista izquierda
   n2 = r - m # tamaño de la sublista derecha
   # crea listas temporales para guardar las sublistas derecha e izquierda
   L = [0] * (n1)
   R = [0] * (n2)
   # copia la data de la lista a ordenar a las listas temporales L[] y R[]
   for i in range(0, n1):
      L[i] = arr[l + i]
   for j in range(0, n2):
      R[j] = arr[m + 1 + j]
   # inicializa los punteros para atravesar las sublistas izquierda y derecha
   i = 0	 # índice inicial de la primera sublista
   j = 0	 # índice inicial de la segunda sublista
   k = l	 # #índice inicial de la sublista fusionada
   
   # compara y fusiona elementos de la listas temporales
   # de vuelta a arr[l..r] basado en el orden (asc o desc)
   while i < n1 and j < n2:
      if order==0: # orden ascendente
         if getattr(L[i],'total_price') <= getattr(R[j],'total_price'):
            arr[k] = L[i]
            i += 1
         else:
            arr[k] = R[j]
            j += 1
      else: # orden descendente
         if getattr(L[i],'total_price') >= getattr(R[j],'total_price'):
            arr[k] = L[i]
            i += 1
         else:
            arr[k] = R[j]
            j += 1   
      k += 1
   # copia los elementos restantes de L[], si hay alguno
   while i < n1:
      arr[k] = L[i]
      i += 1
      k += 1
   # copia los elementos restantes de R[], si hay alguno
   while j < n2:
      arr[k] = R[j]
      j += 1
      k += 1
# l es el índice izquierdo y r es el índice derecho de la sublista de la lista a ordenar
def mergeSort(arr, l, r, order):
   if l < r:
      # igual que (l+r)//2, pero evita desbordamiento
      # para valores grandes de l y r
      # calcula el índice del medio de la sublista actual
      m = l+(r-l)//2
      # ordena recursivamente la primera y la segunda mitad de la sublista
      mergeSort(arr, l, m, order)
      mergeSort(arr, m+1, r, order)
      # fusiona las mitades derecha e izquierda ordenadas de vuelta en la lista original
      merge(arr, l, m, r, order)


# Shellsort
# Esta implementación realiza un ordenamiento de inserción con espacios para un
# tamaño de gap del tamaño original de la lista a ordenar.
# Los primeros elementos de la lista a[0..gap-1] ya están en la lista, luego se sigue
# añadiendo elementos hasta completar la lista ya ordenada
def shellSort(arr, order):
   # calcula el tamaño de la lista a ordenar para luego determinar el tamaño del gap
   # y para iterar a través de la lista
   n = len(arr)
   # inicializa el tamaño del gap con la mitad del tamaño de la lista
   # el tamaño del gap determina cuántos elementos serán comparados e intercambiados
   # durante cada pasada.
   gap = n//2
   # inicia el bucle principal para el algoritmo shellsort
   # el bucle continúa hasta que el tamaño del gap se hace 0,
   # lo que indica la completación del proceso de ordenamiento.
   while gap > 0:
      # itera a través de la lista empezando por el valor del gap actual.
      for i in range(gap, n):
      # guarda el valor del elemento actual en una variable temporal
      
      # agrega a[i] a los elementos que han sido ordenados por espacios
      # guarda a[i] en temp y hace un agujero en la posición i
         temp = arr[i]
         # inicializa el puntero j con el índice actual i
         j = i
         # revisa si el orden es ascendente (order == 0).
         if order==0:
            # mientras el puntero j sea más grande o igual que el tamaño del gap
            # y el elemento en j-gap sea más grande que el valor de temp (asc),
            # se mueve el elemento en j-gap a la derecha.
            while j>=gap and getattr(arr[j-gap],'number_of_reservations')>getattr(temp,'number_of_reservations'):
               arr[j] = arr[j-gap]
               j -= gap
         else: # si el orden es descendente (order==1)
            # mientras el puntero j sea más grande o igual que el tamaño del gap
            # y el elemento en j-gap sea más pequeño que el valor de temp (desc),
            # se mueve el elemento en j-gap a la derecha.
            while j>=gap and getattr(arr[j-gap],'number_of_reservations')<getattr(temp,'number_of_reservations'):
               arr[j] = arr[j-gap]
               j -= gap
            # pone temp (el original a[i]) en su ubicación correcta
         arr[j] = temp
      # reduce el tamaño del gap a la mitad, y continúa con la siguiente iteración.
      gap //= 2

# Heapsort
# Implementación para apilar el subárbol con raíz en el índice i
# n es el tamaño de la lista
def heapify(arr, n, i, order):
   largest = i # inicializa el más grande como la raiz
   l = 2 * i + 1 # izquierda = 2*i + 1
   r = 2 * i + 2 # derecha = 2*i + 2
   if order==0:
      #verifica si hijo izquierdo de la raíz existe
      # si el orden es ascendente, verifica que si el hijo izquierdo es más grande que la raíz
      if l < n and getattr(arr[i],'length_of_stay') < getattr(arr[l],'length_of_stay'):
         largest = l
      # verifica si hijo derecho de la raíz existe
      # si el orden es ascendente, verifica si el hijo derecho es más grande que la raíz
      if r < n and getattr(arr[largest],'length_of_stay') < getattr(arr[r],'length_of_stay'):
         largest = r
   else:
      # verifica si hijo izquierdo de la raíz existe
      # si el orden es descendente, verifica que si el hijo izquierdo es más pequeño que la raíz
      if l < n and getattr(arr[i],'length_of_stay') > getattr(arr[l],'length_of_stay'):
         largest = l
      # verifica si hijo derecho de la raíz existe
      # si el orden es descendente, verifica si hijo derecho es más pequeño que la raíz
      if r < n and getattr(arr[largest],'length_of_stay') > getattr(arr[r],'length_of_stay'):
         largest = r
   # cambia la raíz, de ser necesario
   if largest != i:
      (arr[i], arr[largest]) = (arr[largest], arr[i]) # intercambia
      # Heapify la raíz
      heapify(arr, n, largest, order)
# función de ordenamiento heapsort
def heapSort(arr, order):
	n = len(arr)
      # construye un maxheap
      # ya que el último padre estará en (n//2)-1, se puede empezar desde esa ubicación
	for i in range(n // 2 - 1, -1, -1):
		heapify(arr, n, i, order)
      # extrae elementos uno por uno
	for i in range(n - 1, 0, -1):
		(arr[i], arr[0]) = (arr[0], arr[i]) # intercambia
		heapify(arr, i, 0, order)

# función para definir el criterio de ordenamiento
def get_criteria():
   arr = []
   flag = True
   print("""\nCriterios de orden:
1. Nombre del cliente
2. Fecha de reservación
3. Fecha de check in
4. Fecha de check out
5. Hora de check in
6. Hora de check out
7. Duración de la estadía
8. Número de huéspedes
9. Número de la habitación
10. Tipo de habitación
11. Preferencias alimentarias
12. Correo electrónico
13. Número de teléfono
14. Precio total
15. Método de pago
16. Notas adicionales
17. Estado de la reservación
18. ID de la reservación

Escriba 0 si no desea seleccionar más criterios.""")
   while flag:
      option = input('\nSeleccione un criterio de orden: ')
      if option == '0':
         if arr == []:
            arr=['client_name']
         return arr
      elif option == '1':
         arr.append('client_name')
      elif option == '2':
         arr.append('reservation_date')
      elif option == '3':
         arr.append('check_in')
      elif option == '4':
         arr.append('check_out')
      elif option == '5':
         arr.append('check_in_hour')
      elif option == '6':
         arr.append('check_out_hour')
      elif option == '7':
         arr.append('length_of_stay')
      elif option == '8':
         arr.append('number_of_guests')
      elif option == '9':
         arr.append('room_number')
      elif option == '10':
         arr.append('room_type')
      elif option == '11':
         arr.append('diet')
      elif option == '12':
         arr.append('email')
      elif option == '13':
         arr.append('phone')
      elif option == '14':
         arr.append('total_price')
      elif option == '15':
         arr.append('payment_method')
      elif option == '16':
         arr.append('notes')
      elif option == '17':
         arr.append('status')
      elif option == '18':
         arr.append('id')
      else: print("Selección inválida. Inténtelo nuevamente.")
      
# función para definir el tipo de orden               
def get_order():
   flag = True
   print("""\n0. Ascendente
1. Descendente""")
   while flag:
      option = input('Seleccione un orden: ')
      if option == '0':
         return 0
      elif option == '1':
         return 1
      else: print("Selección inválida. Inténtelo nuevamente.")
      
# función para definir el rango de fechas
def get_date_range(string):
   flag = True
   while flag:
      answer = input('Fecha '+string)
      try: return (datetime.strptime(answer, '%Y/%m/%d')).date()
      except: print("Formato de fecha aaaa/mm/dd inválido. Intente nuevamente.")
      
# función para encontrar los elementos comprendidos dentro del rango de fechas
def date_range(arr):
   n=0
   print("\nSeleccione un rango de fechas. Ejemplo: 2023/09/01: ")
   i = get_date_range('inicio: ')
   f = get_date_range('fin: ')
   for j in range(len(arr)):
      x = getattr(arr[j],'reservation_date')
      if i<=x and x<=f:
         aux = arr[n]
         arr[n] = arr[j]
         arr[j]=aux
         n+=1
   return n

# función para imprimir la lista ordenada
def output(arr, n):
   arr2 = ['client_name','reservation_date','check_in','check_out',
           'check_in_hour','check_out_hour','length_of_stay','number_of_guests',
           'room_number','room_type','diet','email','phone','total_price',
           'payment_method', 'notes','status','id']
   print('\nLista de reservaciones ordenada:\n')
   for i in range(n):
      for j in arr2:
         if j=='client_name':
            print("Nombre del cliente:", end=' ')
         elif j=='reservation_date':
            print("Fecha de reservación:", end=' ')
         elif j=='check_in':
            print("Fecha de check in:", end=' ')
         elif j=='check_out':
            print("Fecha de check out:", end=' ')
         elif j=='check_in_hour':
            print("Hora de check in:", end=' ')
         elif j=='check_out_hour':
            print("Hora de check out:", end=' ')
         elif j=='length_of_stay':
            print("Duración de estadía:", end=' ')
         elif j=='number_of_guests':
            print("Número de huéspedes:", end=' ')
         elif j=='room_number':
            print("Número de habitación:", end=' ')
         elif j=='room_type':
            print("Tipo de habitación:", end=' ')
         elif j=='diet':
            print("Preferencias alimentarias:", end=' ')
         elif j=='email':
            print("Correo electrónico:", end=' ')
         elif j=='phone':
            print("Número de teléfono:", end=' ')
         elif j=='total_price':
            print("Precio total:", end=' ')
         elif j=='payment_method':
            print("Método de pago:", end=' ')
         elif j=='notes':
            print("Notas adicionales:", end=' ')
         elif j=='status':
            print("Estado de la reservación:", end=' ')
         elif j=='id':
            print("ID de la reservación:", end=' ')
         print(getattr(arr[i], j))
      print('')
      
# menú de opciones
def menu(arr, config):
   # guarda el nombre del hotel
   hotel_name = config.get('hotel_name')
   flag = True
   while flag:
      n = len(arr)
      print(hotel_name+"""\nMenú principal:
1. Visualizar lista de reservaciones (ordenamiento por default)
2. Reordenar lista de reservaciones por criterio
3. Reordenar lista de reservaciones por rango de fecha según el precio total
4. Reordenar lista de clientes según el nro. de reservaciones realizadas por cliente
5. Reordenar lista de reservaciones según la duración de la estadía
6. Salir""")
      option = input('\nSeleccione una opción del menú principal ingresando un entero: ')
      if option == '1':
            # guarda el criterio de ordenamiento por default
            criteria = [config.get('default_sort')]
            # guarda el tipo de orden por default
            order = config.get('default_order')
            # ordena lista usando función quicksort
            quickSort(arr, 0, n-1, criteria, order)
            # imprime la lista ordenada
            output(arr, n)
      elif option=='2':
            # define el criterio de ordenamiento
            criteria = get_criteria()
            # define el tipo de orden (asc o desc)
            order = get_order()
            # ordena lista usando función quicksort
            quickSort(arr, 0, n-1, criteria, order)
            # imprime la lista ordenada
            output(arr, n)
      elif option=='3':
            # guarda el número de reservas que entran dentro del rango de fechas
            n = date_range(arr)
            # define el tipo de orden (asc o desc)
            order = get_order()
            # ordena lista usando función mergesort
            mergeSort(arr, 0, n-1, order)
            # si hay reservas que entran dentro del rango, imprime la lista ordenada según el precio total
            if n!=0:
               output(arr, n)
            else:
               print("\nNo se encontraron reservaciones dentro del rango de fecha.\n")
      elif option=='4':
            group = []
            # define el tipo de orden (asc o desc)
            order = get_order()
            # ordena lista usando función shellsort
            shellSort(arr, order)
            # imprime lista de clientes y # de reservas por cliente
            # evita que se impriman nombre de cliente más de una vez
            # cuando ha hecho varias reservaciones agregando los nombres
            # a la lista group[] y luego verificando que no hayan sido
            # ya impresos antes de imprimir la salida de datos
            for i in arr:
               if getattr(i,'client_name') not in group:
                  print("\nNombre del cliente:", end=" ")
                  print(getattr(i,'client_name'))
                  print("Número de reservaciones realizadas: ", end=" ")
                  print(getattr(i,'number_of_reservations'))
                  group.append(getattr(i,'client_name'))
            print('')
      elif option=='5':
            # define el tipo de orden (asc o desc)
            order = get_order()
            # ordena lista usando función heapsort
            heapSort(arr, order)
            # imprime la lista ordenada según la duración de la estadía
            output(arr, n)
      elif option=='6':
            return print('\nFin.')
      else:
         print("Opción inválida. Intente nuevamente.")
         
# función principal
def main():
   try:
      # intenta cargar archivo de datos y configuración
      config = load_archive(find_path('config.json'))
      data = load_archive(config.get('file_route_name'))
   except:
      raise Exception("Hubo un error en la carga del archivo. Revisar el path en config.json.")
   # crea lista de objetos de la clase Reservation
   reservations = reservation_list(data)
   # genera las reservaciones hechas por cliente
   get_reservations_per_client(reservations)
   # inicializa la función menú
   menu(reservations, config)
main()
