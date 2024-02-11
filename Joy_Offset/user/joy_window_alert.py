import ctypes
import subprocess
import threading

from user.joy_translation import translate_txt


def alert_task(arg):
    try:
        try:
            ctypes.windll.user32.MessageBoxW(0, translate_txt(arg), "Error", 0x10)
        except:
            raise Exception
    except:
        subprocess.run(["zenity", "--error", "--text", translate_txt(arg)])


def show_message(message):
    alert_msg = threading.Thread(target=alert_task, args=(message, ))
    alert_msg.start()
    