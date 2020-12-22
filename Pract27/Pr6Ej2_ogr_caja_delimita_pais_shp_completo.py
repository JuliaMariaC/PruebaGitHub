# -*- coding: utf-8 -*-

import ogr
import osr
import os

# Establecer espacio de trabajo
os.chdir('/Users/juliaclemente/Desktop/UNEP-EDE__forest_area__1445948601')
print(os.getcwd())

# Obtener el driver para shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')

# Abrir el shapefile de origen para lectura
shapefile = driver.Open('UNEP-EDE__forest_area__1445948601.shp', 0)

# Obtener la única capa de shapefile
layer = shapefile.GetLayer(0)

# Establecer archivo shapefile de destino
finalShape = "boxShape.shp"

# Se recomienda comprobar si realmente existe el shapefile destino
if os.path.exists(finalShape):
    driver.DeleteDataSource(finalShape)

#Crear el shapefile de destino
shapefileOut = driver.CreateDataSource(finalShape)

# Crear un objeto de referencia espacial para la fuente de destino
spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')

# Crear la capa del shapefile destino una vez creado éste
finalLayer = shapefileOut.CreateLayer('layer', spatialReference)

# Crear y asignar los campos al shapefile destino que contendrán la copia
# de los del shapefile origen: COUNTRY y CODE

# Primero, crear un objeto de tipo Field para la capa destino con sus
# características: tipo string y ancho
fieldDef = ogr.FieldDefn("COUNTRY", ogr.OFTString)
fieldDef.SetWidth(50)
# Asignarla a la capa del shapefile destino
finalLayer.CreateField(fieldDef)

# Hacer lo mismo con el segundo campo: CODE
fieldDef = ogr.FieldDefn("CODE", ogr.OFTString)
fieldDef.SetWidth(3)
finalLayer.CreateField(fieldDef)

# Se va a imprimir información sobre los países: definimos una lista
countries = []

# Para cada  feature de origen: obtenemos el valor de los campos
# ISO3 y NAME, así como las coordenadas de su geometría para volcarlo después
# en los respectivos campos de las features en la capa destino
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    countryCode = feature.GetField("ISO_3_CODE") # da error ISO3
    countryName = feature.GetField("NAME")
    geometry = feature.GetGeometryRef()
    minLongitude, maxLongitude, minLatitude, maxLatitude = geometry.GetEnvelope()
    
    countries.append((countryName, countryCode, minLatitude, maxLatitude, minLongitude, maxLongitude))
  
  # Creamos un anillo para definir posteriormente el polígono correspondiente
  # con las coordenadas de la geometría de cada país
  
    linearRing = ogr.Geometry(ogr.wkbLinearRing)
    linearRing.AddPoint(minLongitude, minLatitude)
    linearRing.AddPoint(maxLongitude, minLatitude)
    linearRing.AddPoint(maxLongitude, maxLatitude)
    linearRing.AddPoint(minLongitude, maxLatitude)
    linearRing.AddPoint(minLongitude, minLatitude)
    
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(linearRing)
    
    # Definir un objeto con la estructura de la capa de destino *:
    finalFeatureDef = finalLayer.GetLayerDefn()
    
    # Definimos un objeto feature con la estructura de la capa destino
    finalFeature = ogr.Feature(finalFeatureDef)
    
    # Definimos la geometría y el valor de los campos COUNTRY y CODE
    # en la capa destino con los valores establecidos del polígono definido
    # y valores de campos en el shapefile de origen
    finalFeature.SetGeometry(polygon)
    finalFeature.SetField("COUNTRY", countryName)
    finalFeature.SetField("CODE", countryCode)
    
    # Añadir la feature anterior ya completada a la capa destino
    finalLayer.CreateFeature(finalFeature)
    
    # Eliminar los objetos feature
    feature.Destroy()
    finalFeature.Destroy()
  
countries.sort()

# Imprimimos los datos de cada país, para suministrar esta información por
# pantalla. Los datos previos formateados: nombre, código, mín. y máx lat.
# y long, respectivamente
for name,  code, minLat, maxLat, minLong, maxLong in countries:
    print('{0}  {1}  lat={2:.4f}..{3:.4f}, long={4:.4f}..{5:.4f}'.format(name, code, \
                                                                         minLat, maxLat, minLong, maxLong))

# Eliminar los objetos shapefile
shapefile.Destroy()
shapefileOut.Destroy()