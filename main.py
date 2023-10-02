from routes import *
from waitress import serve

if __name__ == '__main__':
    print("""
             +===================++++===============================+
             |         Welcome to USYD Digital Badges System         |
             |                                                       |
             |  Open http://127.0.0.1:5000 for accessing the system  |
             +====================================++++===============+
            """)
    serve(app, host='0.0.0.0', port=5000)

