# webcam-armbian-docker

Созданно специально для сайта https://cctv-m.ru/%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BD%D0%B0%D0%B1%D0%BB%D1%8E%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BD%D0%B0-armbian-%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%D0%B8-%D1%80%D1%83%D0%BA%D0%B0%D0%BC%D0%B8-diy

И так что нужно сделать.

1) Подключить USB камеру к raspberryPi или OrangePi
2) Armbian 21.08.6 Buster
3) Камера должна определиться как /dev/video1 (если это не так в app.py и docker-compose.yml поправьте на нужную)
4) Установите docker и docker-compose
5) Запустите: docker-compose up -d

Данный контейнер откроет порт 5000. К примеру http://192.168.0.10:5000 .

Внимание: Данный код предназначен только для просмотра в реальном времени в 1 поток видео.

    Примечание: если у вас /dev/video0 , то необходимо поменять в app.py в строке 45 camera = cv2.VideoCapture(1) на camera = cv2.VideoCapture(0)  и конечно же везде /dev/video1 на /dev/video0
