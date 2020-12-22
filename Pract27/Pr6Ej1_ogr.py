#-*- coding: utf-8 -*-

import ogr

# añadir: establecer espacio de trabajo 
#  poner comentarios
# menos hard-coded
# que sirva para shapefile de más de  una  capa: obtener el número de capas e iterar sobre
#  ellas para hacer lo mismo, esto, sobre cada capa

driver = ogr.GetDriverByName('ESRI Shapefile')

shapefile = driver.Open('C:\\progTIG\\UNEP-EDE__forest_area__1445948601\\UNEP-EDE__forest_area__1445948601.shp', 1)

numLayers = shapefile.GetLayerCount()

print(numLayers)

layer = shapefile.GetLayer(0)

# objeto que define la capa
layerDef = layer.GetLayerDefn()

numFeatures = layer.GetFeatureCount()

print(numFeatures)

spatialRef = layer.GetSpatialRef()

print(spatialRef)
if spatialRef:
    print(spatialRef.ExportToProj4())
    
feature = layer.GetFeature(0)

# GetFieldDefn(i)  obtenido sólo una vez en el for con una variable. No invocarla tantas 
# veces
for i in range(layerDef.GetFieldCount()):
    fieldName = layerDef.GetFieldDefn(i).GetName()
    fieldTypeCode = layerDef.GetFieldDefn(i).GetType()
    fieldType = layerDef.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
    fieldWidth = layerDef.GetFieldDefn(i).GetWidth()
    precision = layerDef.GetFieldDefn(i).GetPrecision()
    print(fieldName + "-" + " " + str(fieldWidth) + " " + str(precision))

layer.SetAttributeFilter("SREG_NAME = 'Eastern Europe'")

for feature in layer:
    print(feature.GetField("NAME"))
# no hace falta limpiar el filtro o sí (mejor sí): layer.SetAttributeFilter(None)

# U obtener el FID: GetNextFeature() de la layer y leugo, while, dentro distinguir
# cada caso: field_FID = feature.GetFID() y GetField('ISO_2_CODE')
 

#layer.DeleteFeature(29)
#shapefile.ExecuteSQL('REPACK' + layer.GetName())
# you can ensure that the spatial extent gets updated by calling this después de 56
# ds.ExecuteSQL('RECOMPUTE EXTENT ON ' + layer.GetName())

#GetFID()en variable y si es == 0:
feature = layer.GetFeature(0)
feature.SetField("DEVELOPED", 1)
layer.SetFeature(feature)

layer.SetAttributeFilter("ISO_2_CODE IS NULL")
for feature in layer:
    print('\n')
    print(feature.GetField("NAME"))
    feature.SetField("ISO_2_CODE", "NN")
    layer.SetFeature(feature)
# no hace falta limpiar el filtro o sí (aquí  no, porque luego no se usa): layer.SetAttributeFilter(None)

feature.Destroy()

shapefile.Destroy()