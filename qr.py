import qrcode
from io import BytesIO
from base64 import b64encode
from flask import render_template, request

def generate_qr():
    if request.method == 'POST':
        memory = BytesIO()
        data = request.form.get('link')
        img = qrcode.make(data)
        filename = f"{data}.png"
        img.save(memory)
        img.save('static/uploads/' + filename)
        memory.seek(0)
        
        base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')
        return render_template('barcode.html', data=base64_img)