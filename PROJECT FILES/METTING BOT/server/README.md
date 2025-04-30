python -m venv venv

venv\Scripts\activate



Are you using a Virtualenv? If so make sure that VSCode is using the virtualenv as your python interpreter, otherwise it will not be able to pick up the packages that you installed inside this virtualenv.

To do so, click on the Python interpreter in your bottom bar, you should get a list of possible python interpreters including your virtualenv.

or enter the path to the venv to find.



download these dependencies



pip install flask flask-cors

pip install pyannote.audio

pip install openai-whisper

pip install selenium