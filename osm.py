import geopandas as gpd
from django.contrib.gis.geos import Polygon
from core.models import Province, City, District, Village

# خواندن فایل GeoJSON
gdf = gpd.read_file('tehran_regions.geojson')

# ایجاد استان تهران
tehran_province, _ = Province.objects.get_or_create(name="تهران")

# ایجاد شهر تهران
tehran_city, _ = City.objects.get_or_create(name="تهران", province=tehran_province)

# تبدیل داده‌های GeoJSON به مدل District
for index, row in gdf.iterrows():
    properties = row['properties']
    geometry = row['geometry']

    # ایجاد یک شیء Polygon از هندسه
    if geometry.geom_type == 'Polygon':
        polygon = Polygon(geometry.exterior.coords)
    else:
        continue  # اگر هندسه Polygon نباشد، از آن صرف‌نظر کنید

    # ایجاد شیء District و ذخیره در دیتابیس
    District.objects.create(
        name=properties.get('name', ''),
        city=tehran_city,
        geometry=polygon
    )
