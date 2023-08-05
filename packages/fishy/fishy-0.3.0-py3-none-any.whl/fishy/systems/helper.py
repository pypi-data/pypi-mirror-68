import logging
import os
import shutil
import sys
import threading
import traceback
import webbrowser
from decimal import Decimal
from threading import Thread
from zipfile import ZipFile

import cv2
import numpy as np
from uuid import uuid1
from hashlib import md5

from win32com.client import Dispatch

import fishy
import winshell
import functools

from fishy.systems.gui import GUIFunction


def round_float(v, ndigits=2, rt_str=False):
    """
    Rounds float
    :param v: float ot round off
    :param ndigits: round off to ndigits decimal points
    :param rt_str: true to return string
    :return: rounded float or strings
    """
    d = Decimal(v)
    v_str = ("{0:.%sf}" % ndigits).format(round(d, ndigits))
    if rt_str:
        return v_str
    return Decimal(v_str)


def draw_keypoints(vis, keypoints, color=(0, 0, 255)):
    """
    draws a point on cv2 image array
    :param vis: cv2 image array to draw
    :param keypoints: keypoints array to draw
    :param color: color of the point
    """
    for kp in keypoints:
        x, y = kp.pt
        cv2.circle(vis, (int(x), int(y)), 5, color, -1)


def enable_full_array_printing():
    """
    Used to enable full array logging
    (summarized arrays are printed by default)
    """
    np.set_printoptions(threshold=sys.maxsize)


def open_web(website):
    logging.debug("opening web, please wait...")
    Thread(target=lambda: webbrowser.open(website, new=2)).start()


def create_new_uid():
    return md5(str(uuid1()).encode()).hexdigest()


def install_thread_excepthook():
    """
    Workaround for sys.excepthook thread bug
    https://bugs.python.org/issue1230540
    (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psycho.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    """
    import sys
    run_old = threading.Thread.run

    def run(*args, **kwargs):
        try:
            run_old(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            sys.excepthook(*sys.exc_info())

    threading.Thread.run = run


def unhandled_exception_logging(*exc_info):
    text = "".join(traceback.format_exception(*exc_info))
    logging.error("Unhandled exception: %s", text)


def get_data_file_path(rel_path):
    return os.path.join(os.path.dirname(fishy.__file__), rel_path)


def create_shortcut(gui):
    try:
        user = os.path.expanduser("~")
        if os.path.exists(os.path.join(user, "Desktop")):
            path = os.path.join(user, "Desktop", "Fishybot ESO.lnk")
            _copy_shortcut(path)
        else:
            gui.call(GUIFunction.ASK_DIRECTORY, (_copy_shortcut,
                                                 "Could not find Desktop please specify path to create shortcut"))
    except Exception:
        logging.info("Couldn't create shortcut")
        traceback.print_exc()


def _copy_shortcut(path):
    desktop = winshell.desktop()
    path = os.path.join(desktop, "Fishybot ESO.lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = os.path.join(os.path.dirname(sys.executable), "python.exe")
    shortcut.Arguments = "-m fishy"
    shortcut.IconLocation = get_data_file_path("icon.ico")
    shortcut.save()

    logging.info("Shortcut created")


def check_addon():
    try:
        user = os.path.expanduser("~")
        addon_dir = os.path.join(user, "Documents", "Elder Scrolls Online", "live", "Addons")
        if not os.path.exists(os.path.join(addon_dir, 'ProvisionsChalutier')):
            logging.info("Addon not found, installing it...")
            with ZipFile(get_data_file_path("ProvisionsChalutier.zip"), 'r') as zip:
                zip.extractall(path=addon_dir)
            logging.info("Please make sure you enable \"Allow outdated addons\" in-game\n"
                         "Also, make sure the addon is visible clearly on top left corner of the game window")
    except Exception:
        print("couldn't install addon, try doing it manually")


def restart():
    os.execl(sys.executable, *([sys.executable] + sys.argv))
