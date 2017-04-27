# 2016-17
Code base for the 2016-17 buld season

## UI Dependencies

### Python VLC
pip install python-vlc
ALSO make sure 32 bit VLC player is installed to the OS:

| Operating System | Installation |
| :----------------: | :----------------------------------------------: |
| Linux (Ubuntu) | Usually comes by default, otherwise usually in the package manager |
| Windows | http://get.videolan.org/vlc/2.2.4/win32/vlc-2.2.4-win32.exe |

### PyQT4 Installation:
| Operating System | Installation  (Neither seems to work in pip) |
| :----------------: | :----------------------------------------------: |
| Linux (Ubuntu) | sudo apt-get install python-qt4 |
| Windows | http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe |

### Numpy Installation:
pip install numpy

### SDL2 Installation:
pip install PySDL2

Also download SDL.dll from http://libsdl.org/download-2.0.php for your version of Python (i.e.: x86 SDL for x86 Python install)
Add to Python install directory under DLLs and add PYSDL2_DLL_PATH=\<Your python dll directory\> to the system path

