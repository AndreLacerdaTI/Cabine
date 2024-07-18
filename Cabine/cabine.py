from flask import Flask, render_template, Response, request, jsonify, url_for, flash
import cv2

from dados import *

app = Flask(__name__)
app.secret_key = 'cabine'
camera = cv2.VideoCapture(0)  # Inicia a captura da webcam

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
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tirar_foto', methods=['POST'])
def tirar_foto():
    return render_template('capturar.html')

    
@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    codigo = data.get('codigo', '')
    nome = data.get('nome', '')
    anos = data.get('anos', '')
    dados=[codigo, nome, anos]
    success, frame = camera.read()
    if success:
        cv2.imwrite(f'./static/fotos/{codigo}.jpg', frame)
        #return jsonify(success=True, codigo=codigo)
        
        redirect_url = url_for('fotografia', codigo=codigo, nome=nome, anos=anos)
        return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)
        #redirect_url = url_for('fotografia', dados=dados)
        #return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)
    else:
        return jsonify(success=False, message="Falha ao capturar a imagem.", codigo=codigo)

@app.route('/fotografia')
def fotografia():
    return render_template('fotografia.html')

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.20.125')
