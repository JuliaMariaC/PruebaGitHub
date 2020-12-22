# -*- coding: utf-8 -*-

import ogr

# mejoras en el Pr6Ej1_ogr.py

driver = ogr.GetDriverByName('ESRI Shapefile')
ds = driver.Open('C:\\progTIG\\UNEP-EDE__forest_area__1445948601\\UNEP-EDE__forest_area__1445948601.shp', 1)
numLayers = ds.GetLayerCount()
print(numLayers)
layer = ds.GetLayer(0)
layerName = layer.GetName()
print(layerName)
layerDef = layer.GetLayerDefn()
numFeatures = layer.GetFeatureCount()
print(numFeatures)
spatialRef = layer.GetSpatialRef()

print(spatialRef)
if spatialRef:
    print(spatialRef.ExportToProj4())
    
#feature = layer.GetFeature(0)


for i in range(layerDef.GetFieldCount()):
    fieldName = layerDef.GetFieldDefn(i).GetName()
    fieldTypeCode = layerDef.GetFieldDefn(i).GetType()
    fieldType = layerDef.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
    fieldWidth = layerDef.GetFieldDefn(i).GetWidth()
    precision = layerDef.GetFieldDefn(i).GetPrecision()
    print(fieldName + "-" + " " + str(fieldWidth) + " " + str(precision))

print("*" * 4)

layer.SetAttributeFilter("SREG_NAME = 'Eastern Europe'")

for feature in layer:
    print(feature.GetField("NAME"))

# Sólo borrar una vez. Después, poner en comentarios las  dos líneas siguientes:
#layer.DeleteFeature(29)
#shapefile.ExecuteSQL('REPACK' + layer.GetName())
# asegurar que la extensión espacial se actualiza después del borrado con:
# ds.ExecuteSQL('RECOMPUTE EXTENT ON ' + layer.GetName())

print("#" * 4)

feature = layer.GetFeature(0)
feature.SetField("DEVELOPED", 1)
layer.SetFeature(feature)
print feature.GetField("NAME")

print("=" * 4)

#layer.SetAttributeFilter(None)
print layer.GetFeatureCount()
print("+" * 4)

layer.SetAttributeFilter("ISO_2_CODE IS NULL")
for feature in layer:
    print('\n')
    print(feature.GetField("NAME"))
    feature.SetField("ISO_2_CODE", "NN")
    layer.SetFeature(feature)
print("O" * 4)

#  Adicionalmente al ejercicio 1:  a continuación introducidas consultas SQL del tema: GDAL/OGR (I)

query = "SELECT * FROM 'UNEP-EDE__forest_area__1445948601' WHERE REG_NAME = 'Africa' order by ID desc"
resultLayer = ds.ExecuteSQL(query)
resultFeature = resultLayer.GetNextFeature()
while resultFeature:
    print(resultFeature.GetField('ID'))
    print(resultFeature.GetField('NAME'))
    resultFeature = resultLayer.GetNextFeature()
    print('=' * 40)
ds.ReleaseResultSet(resultLayer)

query = "SELECT COUNT(*) FROM 'UNEP-EDE__forest_area__1445948601' WHERE REG_NAME = 'Africa' order by ID desc"
resultLayer = ds.ExecuteSQL(query)
print(resultLayer.GetFeatureCount())
print(resultLayer.GetFeature(0).GetField(0))
print('*' * 40)

ds.ReleaseResultSet(resultLayer)

query = "SELECT DISTINCT REG_NAME FROM 'UNEP-EDE__forest_area__1445948601'"
resultLayer = ds.ExecuteSQL(query)
resultFeature = resultLayer.GetNextFeature()
while resultFeature:
    print(resultFeature.GetField(0))
    resultFeature = resultLayer.GetNextFeature()
print('#' * 40)

# se puede simplificar
# query = "SELECT * FROM {0} WHERE SREG_NAME = 'Eastern Europe'".format(layerName)
query = "SELECT DISTINCT REG_NAME FROM 'UNEP-EDE__forest_area__1445948601'"
regLayer = ds.ExecuteSQL(query)
regFeature = regLayer.GetNextFeature()
while regFeature:
    query1 = "SELECT COUNT(*) FROM 'UNEP-EDE__forest_area__1445948601' \
    WHERE REG_NAME = '" + regFeature.GetField(0) + "'"
    countLayer = ds.ExecuteSQL(query1)
    print(regFeature.GetField(0) + ' ' + countLayer.GetFeature(0).GetFieldAsString(0))
    ds.ReleaseResultSet(countLayer)
    regFeature = regLayer.GetNextFeature()
print('*' * 40)

ds.ReleaseResultSet(regLayer)

ds.Destroy()