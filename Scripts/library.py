# Bibliotecas
import ctypes
import os

import tkinter as tk
from tkinter import Button, Label, StringVar, filedialog

from pytube.innertube import _default_clients
from pytubefix import Playlist, YouTube

import subprocess

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]