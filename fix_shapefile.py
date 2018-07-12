import ogr
import gdal

ogr.UseExceptions()

bad_shapefile_path = r"C:\projects\ForestSentinel\Example_outputs\KENYA_LAIKIPIA_20171006_20170718_001_BROKEN\KENYA_LAIKIPIA_20171006_20170718_001.shp"
new_shapefile_path = r"C:\projects\ForestSentinel\Example_outputs\KENYA_LAIKIPIA_20171006_20170718_001\KENYA_LAIKIPIA_20171006_20170718_001.shp"


def iterate_features(layer):
    for feature_index in range(layer.GetFeatureCount()-1):
        yield layer.GetFeature(feature_index)


def iterate_fields(feature):
    feature_def = feature.GetDefnRef()
    for field_index in range(feature.GetFieldCount()-1):
        yield feature_def.GetFieldDefn(field_index)


if __name__ == "__main__":

    bad_shapefile = ogr.Open(bad_shapefile_path)
    old_layer = bad_shapefile.GetLayer()
    srs = old_layer.GetSpatialRef().Clone()

    driver = ogr.GetDriverByName("ESRI Shapefile")
    new_shapefile = driver.CreateDataSource(new_shapefile_path)
    new_layer = new_shapefile.CreateLayer(
        "remarks",
        srs,
        geom_type=ogr.wkbPolygon
    )

    for field in iterate_fields(old_layer.GetFeature(0)):
        new_layer.CreateField(field)

    for old_feature in iterate_features(old_layer):
        geo = old_feature.GetGeometryRef()
        new_feature = old_feature.Clone()
        new_feature.SetGeometry(geo)
        new_layer.CreateFeature(new_feature)

    new_shapefile.FlushCache()
    new_layer = None
    new_shapefile = None


