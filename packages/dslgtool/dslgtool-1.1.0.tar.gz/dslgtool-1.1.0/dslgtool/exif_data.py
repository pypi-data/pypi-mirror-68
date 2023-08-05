import exifread
from GPSPhoto import gpsphoto

import PIL
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def overwrite_exif_data(img_path, lat, long):
    photo = gpsphoto.GPSPhoto(img_path)
    info = gpsphoto.GPSInfo((lat, long))

    photo.modGPSData(info, img_path)


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 7)


def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)


# def main():
#     # overwrite_exif_data( "/home/ldlong/Pictures/ho-ngoc-ha-8-15409508284741091357269.jpg", 0.0, 2.7)

#     exif = get_exif('/home/ldlong/Pictures/ho-ngoc-ha-8-15409508284741091357269.jpg')
#     geotags = get_geotagging(exif)
#     print(exif)
#     print(get_coordinates(geotags))



# if __name__ == "__main__":
#     main()