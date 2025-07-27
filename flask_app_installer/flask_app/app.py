from flask import Flask, render_template
import threading
import webbrowser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start() 
    app.run()
