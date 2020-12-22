#-*- coding: utf-8 -*-

# cabecera


# importar módulos incluyendo los siguientes
import ogr
import os

# Establecer espacio de trabajo (uso de chdir)


# Obtener el driver para shapefile


# Abrir el shapefile de origen para lectura


# Obtener la  única capa del shapefile


# Establecer archivo shapefile de destino


# Comprobar si existe el archivo shapefile destino. Si existe, eliminarlo (no debe existir previamente)


# Crear el objeto shapefile de destino


# Crear un objeto de referencia espacial para la fuente de destino 

# Establecer el objeto de referencia espacial con referencia WGS84: SetWellKnownGeogCS('WGS84')


# Crear la capa del shapefile destino con la referencia espacial previa


# Crear (definir) y asignar los campos al shapefile destino que contendrán, más tarde,  una copia
# de los del shapefile origen. PARA ELLO:
# Primero, crear un objeto de tipo Field COUNTRY  para la capa destino con sus
# características: tipo string y ancho 50


# Asignarla a la capa del shapefile destino


# Igual para CODE

# Se va a mostrar en pantalla más tarde información sobre los países: 
# Por lo  tanto, definimos aquí  una lista para ello
countries = []

# Para cada feature del shp origen:
# obtenemos el valor de sus campos ISO_3_CODE y NAME, y las coordenadas de su geometría 
# para copiarlos en los respectivos campos (COUNTRY Y CODE) de las features en la capa destino
for i in range(layer.GetFeatureCount()):

   # Obtener feature de posición i

   # Obtener el valor de los campos ISO_3_CODE y NAME de feature i

   # Obtener referencia de geometría de feature i

   # Obtener de la geometría anterior las coordenadas (minLong, maxLong, minLat y maxLat: 
   # usar método GetEnvelope() sobre la geometría

   # Añadir las coordenadas anteriores como tupla nueva a la lista countries 

   # Crear un objeto anillo para definir posteriormente el polígono correspondiente: el anillo
   # se crerá con las coordenadas de la  geometría de feature de  origen anteriores

   # Añadir al objeto de tipo anillo anterior las coordenadas de la geometría de cada país
   # Se proporcionan sólo los dos  primeros  puntos del anillo de tipo rectángulo (faltan otros dos):
   linearRing.AddPoint(minLong, minLat)
   linearRing.AddPoint(maxLong, minLat)


   # Crear un objeto polígono. 
   
   # Añadir al polígono anterior el anillo creado previamente


   # Definir un objeto para los registros destino con la estructura de la 
   # capa de destino:
   #    final_layer_defn = ogr.Feature(<capa_destino>.GetLayerDefn())
   
   
   # Definir un objeto feature destino vacío con la estructura del objeto anterior:
   #    finalFeature (o como queráis nombrarlo) = ogr.Feature(final_layer_defn)
   


   # Añadir a ese objeto feature destino su geometría (el polígono con el anillo, obtenido antes) 
   
   
   
   # Establecer el valor de sus campos COUNTRY Y CODE con los valores de ISO_3_CODE y NAME 
   # de la feature i de origen (se almacenaron antes en sendas variables python al comienzo del for.
   
   
   # Añadir la feature anterior ya completada a la capa destino
   # Fíjese que en cada iteración se hacen todas estas tareas para cada feature origen- feature destino.
   

# Eliminar objetos "pesados" en memoria con Destroy()


# Ordenar la lista de países countries final. ¡Cuidado con la tabulación!


# Mostramos información de los países en pantalla con
# los datos previos formateados: nombre, código, min y max latitud y long.
# respectivamente. Para cada elemento (país) de la lista  countries (tupla en la lista), 
# se itera con tantas variables como elementos de la tupla asociada
for name, code, minLat, maxLat, minLong, maxLong in countries:
  print "{0} {1} lat={2:.4f}..{3:.4f}, long={4:.4f}..{5:.4f}".format(name, code, maxLat, minLong, maxLong)

# Eliminar objetos shapefile (origen y destino)
