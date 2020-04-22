# respiface
A mechanical ventilator user interface made for the Rapsberry Pi with a 7'' touch display

## Notice:
Changes to the interface can be made using QTDeisgner. Agter saving a new interface design
(.ui file), it must be converted to a python file/class using pyuic5. Example:

    pyuic5 mainwindow.ui -o ui_mainwindow.py
    

## QTDesigner
In Linux, after installing PyQt5, this tool can be run as follows:

    qtchooser -run-tool=designer -qt5