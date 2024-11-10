# Wander

## URL to the First Page of Our Application Hosted on Vercel
https://wander-g8t9.vercel.app

## URL to Our Git Repository
https://github.com/JonOng2002/Wander

## Project Setup

### Prerequisites


Ensure that you have the following installed:

- **Node.js** (for the frontend)
- **npm** or **Yarn** (for managing frontend packages)
- **Python 3.11** (ensure that your virtual environment Python version is 3.11.x) and **pip** (for the backend)
- **Virtual environment tool** (e.g., `venv` or `virtualenv`)

### Steps

1. **Cloning the Repository**

    ```bash
    git clone https://github.com/JonOng2002/Wander.git
    cd Wander
    ```

2. **Frontend Setup**

    1. **Navigate to the Frontend Directory**

        ```bash
        cd frontend
        ```

    2. **Install Frontend Dependencies**

        ```bash
        npm install
        ```

    3. **Set Up Environment Variables**

        Ensure that the `.env` file exists and contains the necessary configurations for running the frontend server.

        ```env
        VUE_APP_GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE

        VUE_APP_FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY_HERE
        VUE_APP_FIREBASE_AUTH_DOMAIN=your-firebase-auth-domain.firebaseapp.com
        VUE_APP_FIREBASE_PROJECT_ID=your-firebase-project-id
        VUE_APP_FIREBASE_STORAGE_BUCKET=your-firebase-storage-bucket.appspot.com
        VUE_APP_FIREBASE_MESSAGING_SENDER_ID=YOUR_FIREBASE_MESSAGING_SENDER_ID
        VUE_APP_FIREBASE_APP_ID=YOUR_FIREBASE_APP_ID
        VUE_APP_MEASUREMENT_ID=YOUR_MEASUREMENT_ID

        
        VUE_APP_UNSPLASH_ACCESS_KEY=YOUR_UNSPLASH_API_KEY_HERE
        ```

    4. **Run the Development Frontend Server**

        ```bash
        npm run serve
        ```

        This command will start the Vue development server and enable the proxy setup in `vue.config.js` for API requests.

3. **Backend Setup**

    1. **Navigate to the Backend Directory**

        ```bash
        cd ../backend
        ```

    2. **Install Backend Dependencies**

        ```bash
        pip install -r requirements.txt
        ```

    3. **Set Up Environment Variables**

        Ensure that the `.env` file exists and contains the necessary configurations for running the backend server.

        **Example `.env` File for Backend:**

        ```env
        GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE  # Need to enable Maps Javascript API and Places API
        OPENAI_API_KEY=YOUR_OPENAI_KEY_HERE
        UNSPLASH_ACCESS_KEY=YOUR_UNSPLASH_API_KEY_HERE
        ```

    4. **Set Up Virtual Environment**

        - **Using `pyenv` to Install Python 3.11**

            If you don't have Python 3.11 installed, use `pyenv` to install it:

            ```bash
            pyenv install 3.11.0
            pyenv global 3.11.0  # or use `pyenv local 3.11.0` to set it only for this project directory
            ```

    5. **Verify Python Version**

        ```bash
        python --version  # Should output `Python 3.11.x`
        ```

    6. **Create Virtual Environment**

        - **Windows Example**

            ```bash
            python3.11 -m venv venv-windows
            ```

        - **macOS Example**

            ```bash
            python3.11 -m venv venv-macos
            pip install -r requirements.txt
            ```

    7. **Check `pyvenv.cfg` Structure**

        - **Windows Example**

            ```cfg
            home = C:\Users\domin\.pyenv\pyenv-win\versions\3.11.0
            include-system-site-packages = false
            version = 3.11.0
            executable = C:\Users\domin\.pyenv\pyenv-win\versions\3.11.0\python.exe
            command = C:\Users\domin\.pyenv\pyenv-win\versions\3.11.0\python.exe -m venv C:\wamp64\www\WAD2_Project\WadProj\backend\venv
            ```

        - **macOS Example**

            ```cfg
            home = /opt/homebrew/opt/python@3.11/bin
            include-system-site-packages = false
            version = 3.11.10
            executable = /opt/homebrew/Cellar/python@3.11/3.11.10/Frameworks/Python.framework/Versions/3.11/bin/python3.11
            command = /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv /Users/jonathanong/Wander/backend/venv-macos
            ```

    8. **Activate the Virtual Environment**

        - **Windows**

            ```bash
            venv-windows\Scripts\activate
            ```

        - **macOS**

            ```bash
            source venv-macos/bin/activate
            ```

    9. **Run the Backend Server**

        ```bash
        python main.py
        ```

### Compilation Commands

- **Compiles and Hot-Reloads for Development**

    ```bash
    npm run serve
    ```

- **Compiles and Minifies for Production**

    ```bash
    npm run prod
    ```

## Signup Instructions

1. Click on the **'Sign Up'** button.
2. Enter your desired **username**, a valid **email**, and a **password** that is 6 characters or longer in the respective fields.
3. You can also sign up using your **Google** or **Facebook** account.
4. Click on the **'Sign Up Now'** button to access the app.

## Customize Configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## License

[Specify your project's license here.]

## Contact

[Provide contact information or links for users to reach out.]

---

*This README was generated to provide clear and organized instructions for setting up and using the Wander project.*
