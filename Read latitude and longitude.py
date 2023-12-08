from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    """ 获取图像的EXIF数据 """
    image = Image.open(image_path)
    exif_data = image._getexif()
    return exif_data

def get_geotagging(exif_data):
    """ 从EXIF数据中提取地理标签 """
    if not exif_data:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif_data:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif_data[idx]:
                    geotagging[val] = exif_data[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):
    """ 将经纬度的度分秒格式转换为十进制格式 """
    degrees = dms[0].numerator / dms[0].denominator
    minutes = dms[1].numerator / dms[1].denominator / 60.0
    seconds = dms[2].numerator / dms[2].denominator / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return degrees + minutes + seconds


    return degrees + minutes + seconds

def get_coordinates(geotags):
    """ 从geotags中获取经纬度坐标 """
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat, lon)

# Example usage:
if __name__ == '__main__':
    # Replace with the path to your JPEG image
    image_path = r'C:\\Users\Dell\Desktop\test3.JPG'
    try:
        exif_data = get_exif_data(image_path)
        geotags = get_geotagging(exif_data)
        coordinates = get_coordinates(geotags)
        print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
    except Exception as e:
        print(e)

