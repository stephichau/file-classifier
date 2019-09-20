import qrcode

def new_qr(_data: str):
    _qr = qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=15, border=1)
    _qr.add_data(_data)
    _qr.make(fit=True)
    return _qr.make_image(fill_color='black', back_color='white')
