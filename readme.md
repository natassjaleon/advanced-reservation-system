# Sistema Avanzado de Gestión de Reservas

## Descripción general

Este repositorio de GitHub alberga un sistema avanzado de gestión de reservas diseñado para gestionar de forma eficiente las reservas de un hotel o servicio similar. El sistema proporciona varias funciones, incluidas funciones de clasificación y la capacidad de generar informes detallados, lo que lo convierte en una herramienta valiosa para agilizar las operaciones de reserva.


## Características

 - **Gestión eficiente de reservas:** este sistema permite a los hoteles o proveedores de servicios gestionar eficientemente las reservas organizándolas y clasificándolas en función de múltiples criterios.
 
 - **Representación de datos:** el sistema utiliza un archivo JSON (data.json) para almacenar datos de prueba que representan reservas. Incluye campos relevantes como nombre del cliente, fecha de reserva, fecha de entrada, fecha de salida, número de habitación, duración de la estancia, tipo de habitación, preferencias de comida, número de huéspedes, correo electrónico, número de teléfono, precio total, método de pago, notas adicionales y estado de la reserva.
 - **Archivo de configuración:** Se implementa un archivo de configuración en formato JSON (config.json) para configurar aspectos del sistema. Puede configurar opciones de clasificación predeterminadas (ascendente o descendente), definir detalles del hotel y especificar la ruta de carga del archivo de datos.
 - **Carga de datos:** el sistema carga datos de archivos JSON al iniciar el programa, lo que garantiza que los datos de la reserva estén disponibles para su procesamiento.
 - **Funciones de ordenamiento:** los usuarios pueden ordenar las reservas según múltiples criterios de clasificación, incluida la hora de entrada, el ID de la reservación (autogenerado), el número de habitación, la duración de la estadía y más.
 - **Funciones de ordenamiento adicionales:**
  	1. Los usuarios pueden seleccionar un rango de fechas y ordenar las reservas que se encuentran dentro de ese rango por precio total en orden ascendente o descendente.
	2. Los clientes se pueden enumerar en orden ascendente o descendente según la cantidad de reservas que tengan.
	3. Las reservas también se pueden listar en orden ascendente o descendente según la duración de la estancia.

## Cómo empezar

 1. Clona el repositorio en tu computadora local:

     git clone https://github.com/natassjaleon/advanced-reservation-system.git

 2. Asegúrate de tener Python 3.x instalado en tu sistema.
 3. Personaliza el archivo config.json para configurar el sistema según tus preferencias.
 4. Ejecuta el programa:

    python main.py


## Uso

Utiliza las opciones de menú proporcionadas por el programa para gestionar y ordenar reservas según tus necesidades.

Puedes ordenar las reservas según varios criterios, generar informes y realizar otras tareas de gestión de reservas de manera eficiente.
