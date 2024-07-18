from flask import Flask, render_template, Response, request, jsonify, url_for, flash, g
import cv2
import os

from dados import *

app = Flask(__name__)
app.secret_key = 'cabine'
camera = cv2.VideoCapture(0)  # Inicia a captura da webcam

global cliente_codigo
global codigo_foto
cliente_codigo = 0
codigo_foto = 0

global tema
tema = 'branco'

def gen_frames():
    while True:
        success, frame = camera.read()  # Lê o frame da câmera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Converte o frame em bytes e envia para o navegador

@app.route('/')
def index():
    DIRETORIO = './static/fotos/'
    global tema
    fotos = [os.path.basename(arquivo) for arquivo in os.listdir(DIRETORIO)]
    return render_template('index.html', fotos=fotos[-3:], tema=tema)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tirar_foto', methods=['POST'])
def tirar_foto():
    global cliente_codigo
    global codigo_foto
    cliente_codigo = cliente_codigo + 1
    return render_template('capturar.html')

@app.route('/tirar')
def tirar():
    return render_template('capturar.html')

@app.route('/capture', methods=['POST','GET'])
def capture():
    global cliente_codigo
    cliente = cliente_codigo
    global codigo_foto
    codigo_foto = codigo_foto + 1
    DIRETORIO = './static/fotos/'
    #num_arquivos = sum(len(arquivos) for _, _, arquivos in os.walk(DIRETORIO))
    success, frame = camera.read()    
    if success:
        cv2.imwrite(f'./static/fotos/{cliente}-{codigo_foto}.jpg', frame)
    else:
        return jsonify(success=False, message="Falha ao capturar a imagem.")
    
    if codigo_foto==3:
        redirect_url = url_for('fotografia', cliente=cliente)
        codigo_foto = 0
        return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)
    else:
        #redirect_url = url_for('fotografia', cliente=cliente)
        #return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)
        redirect_url = url_for('tirar')
        return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)

    
@app.route('/fotografia')
def fotografia():
    cliente = request.args.get('cliente', '')
    return render_template('fotografia.html', cliente = cliente)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/trocar_tema', methods=['POST'])
def trocar_tema():
    return render_template('admin.html', trocar_tema=True)

@app.route('/salvar_tema', methods=['POST'])
def salvar_tema():
    novo_tema = request.form['tema']
    global tema
    tema = novo_tema
    return render_template('admin.html')

@app.route('/trocar_logo', methods=['POST'])
def trocar_logo():
    return render_template('admin.html', trocar_logo=True)

@app.route('/sair', methods=['POST'])
def sair():
    return render_template('index.html') 

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='192.168.20.125', debug=True)
