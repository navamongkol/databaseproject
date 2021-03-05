from flask import Flask ,request, render_template
from local import storage
import local as lc
from query import queryfunc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def government():
    return render_template('G.html')

def citizen():
    return render_template('C.html')

@app.route('/tablepositions')
def getPositions():
    return str(storage.get_tablePositions())

@app.route('/tableaddresses')
def getAddresses():
    return str(storage.get_tableAddresses())

@app.route('/tablemembers')
def getMembers():
    return str(storage.get_tableMembers())

@app.route('/tableusers')
def getUsers():
    return str(storage.get_tableUsers())

@app.route('/tablelogins')
def getLogins():
    return str(storage.get_tableLogins())

@app.route('/tableparties')
def getParties():
    return str(storage.get_tableParties())

@app.route('/tablefavorites')
def getFavorites():
    return str(storage.get_tableFavorites())

@app.route('/addtable')
def addTable():
    # storage.insert_positions()
    # storage.insert_addresses()
    # storage.insert_members()
    # storage.insert_users()
    # storage.insert_logins()
    # storage.insert_parties()
    # storage.insert_favorites()
    return "Success"

@app.route('/querytest')
def test():
    return str(queryfunc.selectMember())

print("Helloworld")
# @app.route('/test')
# def test():
#     return render_template('index.html')

app.run(debug = True)
