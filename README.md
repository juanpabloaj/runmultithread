# runmultithread
Run the same process with different inputs in different threads.

Download from the [releases page](https://github.com/juanpabloaj/runmultithread/releases).

![Imgur](http://i.imgur.com/Fu85uhU.png)

The image was created calling the python interpreter and the code available in [this link](https://gist.github.com/juanpabloaj/dff0e43080b3f6d9c7cac7671613cdc3).


## Development

The runmultithread.exe file is standalone (just download and use), but if you will make changes in the code, you need have installed in your system this requirements:

* Qt 4.8.5
* PySide

### Create the .exe

To create the .exe from the code install pyinstaller

	pip install pyinstaller

And use the .spec file

	pyinstaller.exe runmultithread.spec
