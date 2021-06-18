import uuid, re, openpyxl
from flask import Flask, render_template, request, redirect, url_for, session, escape, g
# from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired,Email,Length, DataRequired
import threading
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo

from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------COMPLAINTS INTERNET------------------------------------------------------
#   IMPORT MODULE WHICH WILL SEND AND RETURN XML FILE RESPONSE OF HLR   #
from complaints_internet.hlr_module import Soap_class

#   IMPORT MODULE WHICH WILL READ XML FILE RESPONSE OF HLR   #
from complaints_internet.read_xml_module import Read_request_by_msisdn

#   IMPORT MODULE WHICH WILL CHECK HLR AND PROVIDE DECISIONS   #
from complaints_internet.corrections_module import Check_hlr_info_and_provide_decision as provide_decision

#   IMPORT MODULE WHICH WILL SEND AND RETURN LOG FILE RESPONSE OF SGSN   #
from complaints_internet.sgsn_module import Telnet_sgsn

#   IMPORT MODULE WHICH WILL SEND AND RETURN LOG FILE RESPONSE OF SGSN   #
from complaints_internet.read_log_module import Read_sgsn_log

# -------------------------COMPLAINTS CALL------------------------------------------------------
#   IMPORT MODULE WHICH WILL SEND AND RETURN XML FILE RESPONSE OF HLR   #
from complaints_call.hlr_module import Soap_class as soap_call

from complaints_call.read_xml_module import Read_xml_for_complaints_call

from complaints_call.check_msisdn_in_msc_module import Check_msisdn

from complaints_call.corrections_module import Check_hlr_info_and_provide_decision
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "db": "robic_db",
}
db = MongoEngine(app)
app.config['SECRET_KEY'] = "my secret key"
app.config['MONGO_URI'] = 'mongodb://localhost:27017/robic_db'
app.config['USE_SESSION_FOR_NEXT']=True



app.config["MONGO_URI"] = "mongodb://localhost:27017/robic_db"
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="/"
login_manager.login_message = "You may to be identified"

@app.before_request
def before_request():
    if 'user_id' in session:
        users=mongo.db.users.find()
        for user in users:
            if user['id'] == session['user_id']:
                User = user
        g.User = User

class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonimous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @login_manager.user_loader
    def load_user(username):
        user = mongo.db.users.find_one({"username": username})
        if not user:
            return None
        return User(username=user['username'])

#------------------------------ login page's --------------------------------------
@app.route('/', methods=['GET', 'POST'])
def home_page():
    session['next']=request.args.get('next')
    return render_template('users/login.html')

@app.route('/login', methods=['POST'])
def login():
    session.pop('user_id', None)
    user = mongo.db.users.find_one({"username": request.form["username"]})
    if user and User.check_password(user['password'], request.form['password']):
        session['user_id'] = user['id']
        user_obj = User(username=user['username'])
        login_user(user_obj)
        return redirect('/dashboard')
    else:
        error = 'login or password is incorrect !'
        return render_template('users/login.html', error=error)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if(request.method == 'POST'):
        username=request.form['username']
        password=request.form['password']

        test=uuid.uuid4().hex

        user={"id":test, "username":username, "password":generate_password_hash(password)}
        mongo.db.users.insert_one(user)
        return redirect("/dashboard")
    return render_template('users/sign_in.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

#---------------------------------------------- Plaintes Internet ------------------------------------------------------------
class Msisdn_form_class(FlaskForm):
    msisdn = StringField("Enter the msisdn : ")
    submit = SubmitField("Submit")

@app.route('/internet_complaints', methods=['GET', 'POST'])
@login_required
def internet_complaints():

    msisdn_form = None
    info_parameter = None
    msisdnForm = Msisdn_form_class()
    msisdn_info_results = {'imsi' : 'None','encKey' : 'None','algoId' : 'None','kdbId' : 'None','acsub' : 'None','imsiActive' : 'None','accTypeGSM' : 'None','accTypeGERAN' : 'None','accTypeUTRAN' : 'None','odboc' : 'None','odbic' : 'None','odbr' : 'None','odboprc' : 'None','odbssm' : 'None','odbgprs' : 'None','odbsci' : 'None','isActiveIMSI' : 'None','msisdn' : 'None','actIMSIGprs' : 'None','obGprs' : 'None','qosProfile' : 'None','refPdpContextName' : 'None','imeisv' : 'None','ldapResponse' : 'None'}

    if msisdnForm.validate_on_submit():
        msisdn_form = msisdnForm.msisdn.data
        msisdnForm.msisdn.data = ''

        if re.match('^[0-9]*$', msisdn_form):
            # Recuperation des inforamtions de l'abonne dans la HLR pour Complaints_internet
            msisdn = Soap_class(msisdn=msisdn_form)
            xml_reveived_from_hlr = msisdn.main()

            # Recuperation des inforamtions de l'abonne dans la SGSN pour Complaints_internet
            log_from_sgsn = Telnet_sgsn(msisdn=msisdn_form).main()
            xlsx_sgsn_info = Read_sgsn_log(sgsn_log_file=log_from_sgsn)
            xlsx_sgsn_info.txt_reader()
            xlsx_sgsn_info = xlsx_sgsn_info.xlsx_writter()
            workbook = openpyxl.load_workbook(filename=xlsx_sgsn_info)

            sheet = workbook.active
            dict = {}

            radio_access_type = sheet['C2'].value
            pdp_state = sheet["D2"].value
            terminal_type = sheet["E2"].value
            lac = sheet["F2"].value
            ci = sheet["G2"].value

            # Enrichissement du dataset avec des inforamtions de l'abonne dans la Complaints_internet (ce dernier modifiera le contenu du dictionnaire )
            try:
                Read_request_by_msisdn(xml_reveive_from_hlr=xml_reveived_from_hlr, msisdn_info_results=msisdn_info_results).put_data_in_dataset()
            except :
                messageErreur = 'Error -> file not closed:-) You must first closed the "dataset_internet.xlsx" file !'
                return messageErreur

            # ============================= Correction du probleme ===========================
            subscriber_info = provide_decision()
            info_parameter = subscriber_info.main()
            return render_template("complaints_internet/index.html",
                                   radio_access_type=radio_access_type,
                                   pdp_state=pdp_state,
                                   terminal_type=terminal_type,
                                   lac=lac,
                                   ci=ci,
                                   msisdn_info_results=msisdn_info_results,
                                   msisdn=msisdn_form,
                                   msisdn1=info_parameter,
                                   msisdnForm=msisdnForm)
        else:
            error = "Sorry, the msisdn should be a number only !!!"
            return render_template('complaints_internet/index.html', error=error,msisdnForm=msisdnForm)
    return render_template("complaints_internet/index.html",
                           msisdn_info_results = msisdn_info_results,
                           msisdn = msisdn_form,
                           msisdn1 = info_parameter,
                           msisdnForm = msisdnForm)

@app.route('/call_complaints', methods=['GET', 'POST'])
@login_required
def call_complaints():
    msisdn_form = None
    info_parameter = None
    msisdnForm = Msisdn_form_class()
    msisdn_info_results = {'imsi': 'None','imsiActive': 'None','odboc': 'None','odbic': 'None','odbr': 'None','msisdn': 'None','isActiveIMSI': 'None','imeisv': 'None','ldapResponse': 'None','vlrIdValid': 'None','isdnNumberOfVLR':'None','mss_ip':'None','cfu':'None','cfb':'None','cfnrc':'None','cfnry':'None'}

    if msisdnForm.validate_on_submit():
        msisdn_form = msisdnForm.msisdn.data
        msisdnForm.msisdn.data = ''

        if re.match('^[0-9]*$', msisdn_form):
            # Recuperation des inforamtions de l'abonne dans la HLR pour Complaints_internet
            msisdn = soap_call(msisdn=msisdn_form)
            xml_reveived_from_hlr = msisdn.main()

            # Enrichissement du dataset avec des inforamtions de l'abonne dans la Complaints_internet (ce dernier modifiera le contenu du dictionnaire )

            # Donnees des mss a ajouter dans le dataset
            mss_result_of_check = Check_msisdn(msisdn=msisdn_form).main()

            msisdn_info_results['YAMS01'] = mss_result_of_check['YAMS01']
            msisdn_info_results['YAMS02'] = mss_result_of_check['YAMS02']
            msisdn_info_results['DOMS01'] = mss_result_of_check['DOMS01']
            msisdn_info_results['DOMS02'] = mss_result_of_check['DOMS02']

            # try:

            Read_xml_for_complaints_call(xml_reveive_from_hlr=xml_reveived_from_hlr,msisdn_info_results=msisdn_info_results).put_data_in_dataset()

            # except:
            #     messageErreur = 'Error -> file not closed:-) You must first closed the "dataset_call.xlsx" file !'
            #     return messageErreur

            # Proposition de solutions
            decision = Check_hlr_info_and_provide_decision().main()

            return render_template("complaints_call/index.html",
                                   decision=decision,
                                   msisdn_info_results=msisdn_info_results,
                                   msisdn=msisdn_form,
                                   msisdnForm=msisdnForm)
        else:
            error = "Sorry, the msisdn should be a number only !!!"
            return render_template('complaints_call/index.html', error=error, msisdnForm=msisdnForm)

    return render_template('complaints_call/index.html', msisdnForm = msisdnForm)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('users/settings.html')