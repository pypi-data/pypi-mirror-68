import cv2


def is_containing_qr_code(img_path):
    image = cv2.imread(img_path)

    qrCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)

    if points is not None:
        return True
        
    return False