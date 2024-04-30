
1. 打包工具是pyinstaller


2. pathlib has been part of python stdlib since python 3.4, so there is no reason for Anaconda Navigator to depend on external (obsolete and unmaintained) pathlib package. Open a bug with them.

The presence of the obsolete pathlib package may cause errors during PyInstaller analysis (#7406), and since the package is unnecessary, we black list it (along with some other now-obsolete backports of stdlib packages) here: