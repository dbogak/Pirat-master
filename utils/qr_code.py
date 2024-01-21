import pyqrcode

def qr_link(link):
    qr = pyqrcode.create(link, "L")
    qr.png("qr_link.png", scale=6)
    file = open("qr_link.png", "rb")
    return file