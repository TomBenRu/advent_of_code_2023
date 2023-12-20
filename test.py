import shapely

polygon = shapely.Polygon(((0, 0), (0, 4), (4, 4), (4, 0)))

print(polygon.area)
print(polygon.length)