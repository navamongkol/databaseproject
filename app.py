from flask import Flask ,request, render_template, redirect, url_for, session
from local import storage
from local import storage
from query import queryfunc
import json
import sqlite3

LOCAL_DB = 'local.db'
app = Flask(__name__)
app.secret_key = "super secret key"

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def return_to_homepage():
    user_id = session['userid']
    fullname = session['fullname']
    return render_template('C1.html',datas = queryfunc.APIshowpartiesforuser(user_id),name=fullname)

@app.route('/G')
def G():
    return render_template('G.html')

@app.route('/G1', methods=['POST'])
def governmentlogin():
    Role = request.form['role']
    Password = request.form['password']
    loginresult = queryfunc.APIloginGovernment(Role, Password)
    if (loginresult is not None):
        return render_template('G1.html',datas = queryfunc.APIshowpartiesforgovernment(), top3 = queryfunc.APIshowtopfavorite())
    else:
        return "Failed"

@app.route('/G2/<int:PartyId>')
def G2(PartyId):
    session['PartyId'] = PartyId
    print(session['PartyId'])
    return render_template('G2.html',datas = queryfunc.APIshowpartiesbyid(PartyId))

@app.route('/G3')
def G3():
    PartyId = session['PartyId']
    print(PartyId)
    return render_template('G3.html')

@app.route('/G4')
def G4():
    return render_template('G4.html')

@app.route('/C')
def C():
    return render_template('C.html')    

@app.route('/C1', methods=['POST'])
def userlogin():
    CitizenId = request.form['citizenid']
    BirthDate = request.form['birthdate']
    Password = request.form['password']
    loginresult = queryfunc.APIloginUser(CitizenId,BirthDate,Password)
    if (loginresult is not None):
        session['userid'] = loginresult[0]
        session['fullname'] = loginresult[1]
        session['PartyId'] = queryfunc.APIshowpartiesforuser(loginresult[0])[0][0]
        session['PartyName'] = queryfunc.APIshowpartiesforuser(loginresult[0])[0][1]
        session['MemberName'] = queryfunc.APIshowpartiesforuser(loginresult[0])[0][2]
        # PartyName = session['PartyName']
        # MemberName = session['MemberName']
        print("MemberName",session['MemberName'])
        print(session['PartyId'],session['PartyName'])
        return render_template('C1.html',datas = queryfunc.APIshowpartiesforuser(loginresult[0]),
                                         name=loginresult[1],
                                         show=queryfunc.APIshowfavorite(loginresult[0]))
    else:
        return 'Failed'

@app.route('/C2')
def C2():
    return render_template('C2.html')

@app.route('/insertparty', methods = ['POST'])
def insertparty():
    if request.method == 'POST':
        partyname = request.form['partyname']
        leadername = request.form['leadername']
        province = request.form['province']
        district = request.form['district']
        queryfunc.APIinsertparty(partyname, leadername, province, district)
        return "Success"

@app.route('/updateuser', methods = ['POST'])
def updateuser():
    Province = request.form['province']
    District = request.form['district']
    Phonenumber = request.form['phonenumber']
    userid = session['userid']
    queryfunc.APIupdateUser(userid, Province, District, Phonenumber) 
    return redirect(url_for('return_to_homepage')) 

@app.route('/deleteparty/<int:id>', methods = ['GET'])
def deleteparty(id):
    queryfunc.APIdeleteparty(id)
    return "Success"

@app.route('/addmember', methods = ['POST'])
def addmember():
    if request.method == 'POST':
        partyid = session['PartyId']
        name = request.form['name']
        position = request.form['position']
        province = request.form['province']
        district = request.form['district']
        print(type(partyid),type(name),type(position),type(province),type(district))
        queryfunc.APIaddmember(partyid, name, position, province, district)
        return "Success"

@app.route('/deletemember', methods = ['POST'])
def deletemember():
    if request.method == 'POST':
        partyid = session['PartyId']
        name = request.form['name']
        queryfunc.APIdeletemember(partyid, name)
        return "Success"

@app.route('/favorite/<int:PartyId>', methods = ['GET','POST'])
def favorite(PartyId):
    userid = session['userid']
    queryfunc.APIaddfavorite(PartyId, userid)
    return "Success"

app.run(debug = True)
