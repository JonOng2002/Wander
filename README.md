# Wander

## URL to the first page of our application hosted on Vercel
```
https://wander-g8t9.vercel.app
```

## URL to our GIT repo where our application files are contained
```
https://github.com/JonOng2002/Wander
```

## Project setup
```
Prerequisites
Ensure that you have the following installed:

Node.js (for the frontend)
npm or Yarn (for managing frontend packages)
Python 3.11 (ensure that your virtualenv Python version is on 3.11.x) and pip (for the backend)
Virtual environment tool (e.g., venv or virtualenv)

```

1. Cloning the repository:
```
cd WAD2_Project/WadProj
```

Frontend Setup:

1. Navigate to the frontend directory:
```
cd frontend
```
2. Install the frontend dependencies:
```
npm install
```

3. Set up environment variables: Ensure that the .env file exists and contains the necessary configurations for running the frontend server.
```
VUE_APP_GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE

VUE_APP_FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY_HERE
VUE_APP_FIREBASE_AUTH_DOMAIN=your-firebase-auth-domain.firebaseapp.com
VUE_APP_FIREBASE_PROJECT_ID=your-firebase-project-id
VUE_APP_FIREBASE_STORAGE_BUCKET=your-firebase-storage-bucket.appspot.com
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=YOUR_FIREBASE_MESSAGING_SENDER_ID
VUE_APP_FIREBASE_APP_ID=YOUR_FIREBASE_APP_ID
VUE_APP_MEASUREMENT_ID=YOUR_MEASUREMENT_ID
```

4. Run the development frontend server:
npm run serve

This command will start the Vue development server and enable the proxy setup in vue.config.js for API requests.
```

Backend Setup
```
1.Navigate to the backend directory:
```
cd ../backend
```
2.Install the backend dependencies:
```
pip install -r requirements.txt
```
3.Set up environment variables: Ensure that the .env file exists and contains the necessary configurations for running the backend server.
Example .env file for backend:
```
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE (Need to enable Maps Javascript API and Places API)
OPENAI_API_KEY=YOUR_OPENAI_KEY_HERE
UNSPLASH_ACCESS_KEY=YOUR_UNSPLASH_API_KEY_HERE
```
4. Set up virtual environment for Windows/macOS

5.Ensure Python 3.11 is Installed Using pyenv: If you don't have Python 3.11 installed, use pyenv to install it:
```
pyenv install 3.11.0
pyenv global 3.11.0  # or use `pyenv local 3.11.0` to set it only for this project directory
```
6.Verify that Python 3.11 is the current version:
```
python --version  # Should output `Python 3.11.x`
```
7.venv setup using Python 3.11 (Windows Example)
```
python3.11 -m venv venv-windows
```
venv setup using Python 3.11 (macOS Example)
```
python3.11 -m venv venv-macos
pip install -r requirements.txt
```
8.Check that your pyvenv.cfg has a structure similar to these examples:

Example virtual environment pyvenv.cfg for Windows:
```
home = C:\Users\domin\.pyenv\pyenv-win\versions\3.11.0
include-system-site-packages = false
version = 3.11.0
executable = C:\Users\domin\.pyenv\pyenv-win\versions\3.11.0\python.exe
command = C:\Users\domin\.pyenv\pyenv-win\versions\3.11.0\python.exe -m venv C:\wamp64\www\WAD2_Project\WadProj\backend\venv
```
Example virtual environment pyvenv.cfg for MacOS:
```
home = /opt/homebrew/opt/python@3.11/bin
include-system-site-packages = false
version = 3.11.10
executable = /opt/homebrew/Cellar/python@3.11/3.11.10/Frameworks/Python.framework/Versions/3.11/bin/python3.11
command = /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv /Users/jonathanong/Wander/backend/venv-macos
```
9.Activate the virtual environment:

Windows:
```
venv-windows\Scripts\activate
```

macOS:
```
source venv-macos/bin/activate
```
Run the backend server:
```
python main.py
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
