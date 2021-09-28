import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import csv
import pandas as pd
import io

#UPLOAD_FOLDER = r'D:\Andres\automatizacion'
UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def read_csv(archivo,campo,transaccion):
    with open(archivo,encoding='utf-8-sig') as archivo:
        datos = csv.reader(archivo,delimiter=';')
        for i in datos:
            lista = i
            break
        pos = lista.index(campo)
        suma = 0
        dia = list()
        tra = list()
        valorl = list()
        for linea in datos:
            if linea[1] == transaccion:
                valor = float(linea[pos].replace(',','.'))
                dia.append(linea[0])
                tra.append(linea[1])
                valorl.append(valor)
                suma+=valor 
        df = pd.DataFrame({'dia': dia, 'tra': tra, 'valor':valorl})
        df.to_csv('resultado.csv', index=False)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            campo = request.form.get('campo')
            transaccion = request.form.get('transaccion')
            read_csv(filename,campo,transaccion)
            return redirect(url_for('download_file', name="resultado.csv"))
            #return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Upload new File</title>
    </head>
    <body>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=text id=transaccion name=transaccion placeholder=transaccion>
        <input type=text id=campo name=campo placeholder=campo>
        <input type=submit value=Upload>
        </form>
    </body>
    </html>
    '''
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")