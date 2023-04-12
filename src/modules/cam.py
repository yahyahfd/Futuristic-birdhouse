import paramiko
import time
from datetime import datetime

# Paramètres de connexion SSH
HOST = 'raspberrypi.local'
USERNAME = 'pi'
PASSWORD = 'mezianehafid2023'
time_wait = 1
# Paramètres de la caméra (je penses qu'on prend une photo entiere et qu'on la traite après avec resize non?)
# CAMERA_WIDTH = 640
# CAMERA_HEIGHT = 480
# SI on garde les height est width, on doit rajouter -h {CAMERA_HEIGHT} -w {CAMERA_WIDTH} dans la "command" avec un f avant

# Initialisation de la connexion SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USERNAME, password=PASSWORD)

# try finally pour que même si le programme crash ou est interrompu, la connection ssh est fermée
try:
    # Prise de photos en boucle
    while True:
        # Commande pour prendre une photo avec la caméra Raspberry Pi
        # Commande pour prendre une photo avec la caméra Raspberry Pi
        command = 'raspistill -o /home/pi/photo.png'


        # Exécution de la commande sur le Raspberry Pi
        stdin, stdout, stderr = client.exec_command(command)

        # Attendre time_wait secondes avant de prendre la photo suivante
        time.sleep(time_wait)
        
        # Transférer le fichier photo.png vers l'ordinateur
        now = datetime.now()
        heure_actuelle = now.strftime("%Y-%m-%d_%H-%M-%S")

        transport = client.get_transport()
        sftp = transport.open_sftp()
        sftp.get('/home/pi/photo.png', f'./{heure_actuelle}.png')
        sftp.close()
finally:
    # Fermeture de la connexion SSH
    client.close()
