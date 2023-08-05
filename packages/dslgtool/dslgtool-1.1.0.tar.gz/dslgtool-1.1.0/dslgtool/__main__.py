from os import path, walk
import requests
from requests.exceptions import ConnectionError
import json
from cryptography.fernet import Fernet, InvalidToken
from .location import Location
from .track import Track
from .qrcode_detector import is_containing_qr_code
from PIL import Image
import exifread
from datetime import datetime
from .exif_data import *
import base64
from argparse import ArgumentParser


HOST_NAME = 'http://api.digicam.sankukai.intek.edu.vn/api/v1/routes/'


def parse_arguments():
    """Get all the argument needed about QRCode information

    Returns:
        tuple -- All argument values input by user
    """
    parser = ArgumentParser(description='Process QR Code encrypted data.')
    parser.add_argument('--qrcode-value', action='store', help='QR Code value')
    parser.add_argument('--qrcode-path', action='store', help='Path of QR Code Image')

    args = parser.parse_args()
    return args


def input_passphrase_and_route_id():
    """Get passpharse and route_id from user input

    Returns:
        tuple -- Value of passphrase and route_id
    """
    passphrase = input("Please input your passphrase: ")
    while not passphrase:
        print("Your passphrase is invalid. Please try again.")
        passphrase = input("Please input your passphrase: ")

    route_id = input("Please input your route_id: ")
    while not route_id or len(route_id) != 6:
        print("Your route_id is invalid. Please try again.")
        route_id = input("Please input your route_id: ")

    return passphrase, route_id


def input_folder_path():
    """Get the path of folder containing all images that need to be processed

    Returns:
        str -- Path of the folder to process
    """
    folder_path = input("Please input your folder path: ")

    while not folder_path or not path.isdir(folder_path):
        print("Your folder path is invalid. Please try again.")
        folder_path = input("Please input your folder path: ")

    return folder_path


def fetch_route_data(route_id):
    """Get route encrypted data from server based on route_id argument

    Arguments:
        route_id {str} -- Route_id from user input

    Returns:
        tuple(status_code, data) -- Tuple of status code and route data returned from server
    """
    response = requests.get(HOST_NAME + route_id)
    status_code = response.status_code
    if status_code == 200:
        json_response = json.loads(response.text)
        return status_code, json_response['data']
    else:
        return status_code, None


def get_32_length_key_from_passphrase(passphrase):
    """Generate the 32-length key from passphrase to decrypt QRCode data

    Arguments:
        passphrase {str} -- passphrase get from user input

    Returns:
        str -- 32-length string used to decrypt QRCode data
    """
    if len(passphrase) == 32:
        return passphrase
    else:
        tmp = passphrase
        key = ''

        while len(key) < 32:
            key += tmp + '-'
            tmp = tmp[::-1]

        return key[:32][::-1]


def decrypt_data(nonce, data):
    """Decrypt route data using Fernet algorithm

    Arguments:
        nonce {str} -- 32-length key get from QRCode
        data {str} -- Encrypted route data

    Returns:
        str -- Decrypted route data
    """
    fernet = Fernet(base64.b64encode(str.encode(nonce)))
    decrypted_bytes = fernet.decrypt(str.encode(data))
    decrypted_data = decrypted_bytes.decode()

    return decrypted_data


def parse_route_data(route_data):
    """Format route data into list of Track objects, which contain 
    corresponding Location object

    Arguments:
        route_data {dict} -- Route data in Json format

    Returns:
        list -- List of all Track objects in the route
    """
    tracks = []

    # Create list of Track objects
    for track in route_data['tracks']:
        print("Start Time: {}".format(track['startTime']))
        print("End Time: {}".format(track['endTime']))
        tracks.append(Track(track['startTime'], track['endTime']))

    # Create list of locations for each track
    for item in route_data['locations']:
        location = Location(item['latitude'], item['longtitude'], item['timestamp'])
        for track in tracks:
            if track.is_in_track(location.timestamp):
                track.locations.append(location)
                break
    
    return tracks


def get_list_images(folder_path):
    """Scan image folder and get the list of all image objects

    Arguments:
        folder_path {str} -- Path of image folder

    Returns:
        list -- List of all image paths
    """
    list_images = []
    for dir_path, _, files in walk(folder_path):
        for file_name in files:

            try:
                full_path = path.join(dir_path, file_name)
                _ = Image.open(full_path)
                list_images.append(full_path)
            except Exception:
                continue

    return list_images


def find_qr_image_path(list_images):
    """Find the image which contains QRCode in the list of image

    Arguments:
        list_images {list} -- List of all image paths

    Returns:
        str -- Path of image which contains QR Code
    """
    for img_path in list_images:
        if is_containing_qr_code(img_path):
            print("Image contains qr_code: {}".format(img_path))
            return img_path
    return None


def find_nearest_location_by_time(img_time, first_location, last_location):
    """Find the most suitable location for image between 2 nearest locations

    Arguments:
        img_time {datetime} -- Time when image is captured
        first_location {Location} -- The first location object
        last_location {Location} -- The second location object

    Returns:
        Location -- The most suitable location for image
    """
    if last_location is None:
        return first_location

    diff_first = img_time - first_location.timestamp
    diff_last = last_location.timestamp - img_time

    if diff_first <= diff_last:
        return first_location
    else:
        return last_location


def find_image_location(tracks, img_time):
    """Find the suitable location for image from the list of locations in tracks

    Arguments:
        tracks {list} -- List of all tracks in the route
        img_time {datetime} -- The time when image is captured

    Returns:
        Location -- The most suitable location for image
    """
    for track in tracks:
        if track.is_in_track(img_time):

            for idx, first_location in enumerate(track.locations):
                if img_time >= first_location.timestamp:

                    last_location = None

                    if idx + 1 < len(track.locations):
                        last_location = track.locations[idx + 1]

                    return find_nearest_location_by_time(img_time, first_location, last_location)


def find_diff_time(img_path, qr_time):
    """Find the time difference between image time and time in QRCode

    Arguments:
        img_path {str} -- Path of image which contains QRCode
        qr_time {datetime} -- Time data in QRCode

    Returns:
        datetime -- Time difference between image time and QRCode time
    """
    with open(img_path, 'rb') as f:
        tags = exifread.process_file(f)

        if "Image DateTime" in tags.keys():
            img_time = datetime.strptime(str(tags['Image DateTime']),"%Y:%m:%d %H:%M:%S")
            return qr_time - img_time
        else:
            print("Cannot read time of QRCode Image.")
            exit()


def write_image_exif_data(img_path, location):
    overwrite_exif_data(img_path, location.latitude, location.longtitude)


def update_images_location(tracks, list_images, diff_time):
    """Update location information for all images

    Arguments:
        tracks {list} -- List of all tracks in the route
        list_images {list} -- List of all image paths
        diff_time {datetime} -- Time difference between image time and QRCode time
    """
    for img_path in list_images:
        with open(img_path, 'rb') as f:
            tags = exifread.process_file(f)

            if "Image DateTime" in tags.keys():

                img_time = datetime.strptime(str(tags['Image DateTime']),"%Y:%m:%d %H:%M:%S")

                print('Finding location for: {} ...'.format(img_path))
                
                img_location = find_image_location(tracks, img_time + diff_time)

                if img_location:
                    write_image_exif_data(img_path, img_location)
                else:
                    print('This image path is not belonged to any track: {}'.format(img_path))

            else:
                print('Cannot read datetime from: {}'.format(img_path))


def get_time_and_nonce_from_qr_data(qr_data):
    """Extract nonce and time included in QRCode data

    Arguments:
        qr_data {str} -- QRCode data

    Returns:
        tuple(datetime, str) -- Time and nonce extracted from QRCode
    """
    qr_data = qr_data.split('.')
    time = datetime.strptime('.'.join(qr_data[:2]), "%Y-%m-%d %H:%M:%S.%f") 
    nonce = '.'.join(qr_data[2:])
    return time, nonce


def process_data(passphrase, route_id, folder_path, qr_encrypted_data, qrcode_path, route_encrypted_data):
    try:
        # Get key to decrypt QRCode data
        key = get_32_length_key_from_passphrase(passphrase)

        # Get list of images path from folder image
        list_images = get_list_images(folder_path)

        # Get path of image which contains QRCode
        if not qrcode_path:
            qr_image_path = find_qr_image_path(list_images)
        else:
            qr_image_path = qrcode_path

        # Decrypt and extract QRCode Data
        qr_data = decrypt_data(key, qr_encrypted_data)
        qr_time, nonce = get_time_and_nonce_from_qr_data(qr_data)

        if qr_image_path:
            # Find time difference between QRCode image time and time in QRCode data
            diff_time = find_diff_time(qr_image_path, qr_time)

            # Decrypt route data from encrypted data
            route_data = json.loads(decrypt_data(nonce, route_encrypted_data))

            # Parse route data to list of Track objects
            tracks = parse_route_data(route_data)

            # Update image location
            update_images_location(tracks, list_images, diff_time)
        else:
            print('Cannot detect which image contains QR Code.')
            print('Please use --qrcode-path argument to pass path of QR Code Image.')
            exit()

    except InvalidToken:
        print("PassphraseError: Invalid Passphrase")


def main():
    # Get argument 
    args =  parse_arguments()

    qr_encrypted_data = args.qrcode_value
    qrcode_path = args.qrcode_path

    if not qr_encrypted_data:
        print('Please inpyt qr code value.')
        exit()

    passphrase, route_id = input_passphrase_and_route_id()
    folder_path = input_folder_path()

    try:
        # Get route encrypted data from server
        status_code, route_encrypted_data = fetch_route_data(route_id)

        if status_code == 404:
            print("RouteIdNotFoundError: Route Id is not exist.")
        elif status_code != 200:
            print("ServerError: Cannot fetch data from server.")
        else:
            process_data(passphrase, route_id, folder_path, qr_encrypted_data, qrcode_path, route_encrypted_data)
    except ConnectionError:
        raise ConnectionError('Cannot connect to server. Please check your connection.')
    except Exception:
        print("Unexpected Error. Please try again.")

if __name__ == '__main__':
    main()