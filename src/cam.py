from picamera import PiCamera
from time import sleep

# fonction qui renvoie true si un oiseau est detecte
def bird_detected():
    # TODO

def photo_loop():
    camera = PiCamera()
    camera.start_preview()
    i = 0
    while not (bird_detected()):
        sleep(5)
        camera.capture('/home/pi/Desktop/image%s.jpg' % i)
        i += 1
    camera.stop_preview()
