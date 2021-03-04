from flask import Flask ,request, render_template
from local import storage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

print("Helloworld")
# @app.route('/test')
# def test():
#     return render_template('index.html')

app.run(debug = True)
