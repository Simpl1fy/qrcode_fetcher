# QR Code fetcher

This is a project for fetching qr code, using python, flask and websockets to fetch qr code from any website and show it in your own website

The project uses websockets, for instant updation when qr code is detected

How to set up the application in local

> ### Installing Virtualenv
> pip install virtualenv

> #### Initializing Virtual enviornment
> python -m virtualenv venv

> #### Activating the Virtual Enviornment
> venv\Scripts\activate

> #### Installing necessary modules
> pip install -r requirements.txt

### Compiling the app

> cd "Application with backend"
>
> pyinstaller --onefile app.py

The app will be compiled in dist/app.py
You can run the app by double clicking the application or running the command in terminal

> dist/app.py

The images will be saved in dist in filename qr_code.png

### Running the flask web socket server

> python server.py

This is enough for the backend

### Frontend

In a different terminal

> cd qrcode-frontend

> npm install
> 
> npm run dev

This should be enough to run the project.