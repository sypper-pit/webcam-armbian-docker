import cv2
import subprocess
from flask import Flask, Response, render_template, request

app = Flask(__name__)

# Настройки камеры
camera_params = {
    'exposure_auto': 1,
    'exposure_absolute': 50,
    'video_mjpeg_width': 1280,
    'video_mjpeg_height': 720,
    'saturation': 255,
    'brightness': 128,
    'contrast': 128,
    'hue': 0,
    'sharpness': 128,
    'white_balance_temperature_auto': 1,
    'white_balance_temperature': 4000,
    'backlight_compensation': 0,
    'gain': 0
}
# Настройка камеры
def init_camera():
    # Установить параметры камеры с помощью v4l2-ctl
    import subprocess
    subprocess.Popen(["v4l2-ctl", "-d", "/dev/video1", "--set-fmt-video=width=1280,height=720,pixelformat=1"])
    for param, value in camera_params.items():
        subprocess.Popen(["v4l2-ctl", "-d", "/dev/video1", "-c", f"{param}={value}"])



# Обработка кадра и кодирование в JPEG
def process_frame(frame):
    # Ресайз кадра
    frame = cv2.resize(frame, (camera_params['video_mjpeg_width'], camera_params['video_mjpeg_height']))
    # Кодирование в JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return frame


# Чтение видеопотока и отправка в формате JPEG
def gen_frames():
    camera = cv2.VideoCapture(1)
    while True:
        success, frame = camera.read()
        if not success:
            break
        # Обработка кадра и кодирование в JPEG
        frame = process_frame(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# Отображение страницы настроек
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        for param in camera_params.keys():
            value = int(request.form[param])
            camera_params[param] = value
            subprocess.Popen(["v4l2-ctl", "-d", "/dev/video1", "-c", f"{param}={value}"])
    return render_template('settings.html', params=camera_params)
# Отображение главной страницы
@app.route('/')
def index():
    return """<p>Web-Cam use:</p>

                <ul>
                        <li><a href="/video_feed">Video</a></li>
                        <li><a href="/settings">Settings</a></li>
                </ul>"""
# Отображение видеопотока
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    init_camera()
    app.run(host='0.0.0.0', debug=True)

