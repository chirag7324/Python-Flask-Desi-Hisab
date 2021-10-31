from flask import Flask,render_template,request,redirect,flash,url_for,session
from flask_modals import Modal,render_template_modal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,and_,func
import json
from datetime import date
import datetime

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/budget_db"

db = SQLAlchemy(app)
modal = Modal(app)

class Tbluser(db.Model):
    # id,type,name,description,date,amount,start_date,end_date,month
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(512), nullable=False)
    password = db.Column(db.String(512), nullable=False)

class Tblincome(db.Model):
    # id,type,name,description,date,amount,start_date,end_date,month
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    amount = db.Column(db.Float(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    start_date = db.Column(db.String(12), nullable=True)
    end_date = db.Column(db.String(12), nullable=True)
    month = db.Column(db.Integer, nullable=False)

class Tblbanks(db.Model):
    # id,type,name,description,date,amount,start_date,end_date,month
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(80), nullable=False)
    banks = db.relationship('Tblexpense', backref='tblbanks', lazy=True)
    banks1 = db.relationship('Tblbankdeposit', backref='tblbanks', lazy=True)
    banks_ccpayment = db.relationship('Tblccpayment', backref='tblbanks', lazy=True)
    banks_borrow = db.relationship('Tblborrow', backref='tblbanks', lazy=True)


class Tblcategory(db.Model):
    # id,type,name,description,date,amount,start_date,end_date,month
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    categories = db.relationship('Tblexpense', backref='tblcategory', lazy=True)


class Tblcreditcard(db.Model):
    # id,type,name,description,date,amount,start_date,end_date,month
    id = db.Column(db.Integer, primary_key=True)
    credit_card = db.Column(db.String(80), nullable=False)
    total_credit = db.Column(db.Float(12), nullable=False)
    creditcards = db.relationship('Tblexpense', backref='tblcreditcard', lazy=True)
    credit_payment = db.relationship('Tblccpayment', backref='tblcreditcard', lazy=True)
    credit_borrow = db.relationship('Tblborrow', backref='tblcreditcard', lazy=True)


class Tblexpense(db.Model):
    # id,type,name,description,date,amount,start_date,end_date,month
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12), nullable=True)
    name = db.Column(db.String(80), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('tblcategory.id'), nullable=True)
    mode = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float(12), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey('tblbanks.id'), nullable=True)
    ccid = db.Column(db.Integer, db.ForeignKey('tblcreditcard.id'), nullable=True)
    month = db.Column(db.Integer, nullable=False)

class Tblccpayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ccid = db.Column(db.Integer, db.ForeignKey('tblcreditcard.id'), nullable=True)
    bid = db.Column(db.Integer, db.ForeignKey('tblbanks.id'), nullable=True)
    date = db.Column(db.String(12), nullable=True)
    name = db.Column(db.String(80), nullable=False)
    mode = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float(12), nullable=False)
    description = db.Column(db.String(512), nullable=False)


class Tblbankdeposit(db.Model):
    # id,type,name,description,date,amount,start_date,end_date,month
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey('tblbanks.id'), nullable=True)
    amount = db.Column(db.Float(12), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Tbltransfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12), nullable=True)
    payee = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    sending_amount = db.Column(db.Float(12), nullable=False)
    rate = db.Column(db.Float(12), nullable=False)
    received_amount = db.Column(db.Float(12), nullable=False)
    description = db.Column(db.String(512), nullable=False)


class Tblborrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12), nullable=True)
    trans_no = db.Column(db.Float(12), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    borrower = db.Column(db.String(80), nullable=False)
    lender = db.Column(db.String(80), nullable=False)
    ccid = db.Column(db.Integer, db.ForeignKey('tblcreditcard.id'), nullable=True)
    bid = db.Column(db.Integer, db.ForeignKey('tblbanks.id'), nullable=True)
    borrow_amount = db.Column(db.Float(12), nullable=False)
    repay_amount = db.Column(db.Float(12), nullable=False)
    balance = db.Column(db.Float(12), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    mode = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)


class Tblrepay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12), nullable=True)
    trans_no = db.Column(db.Float(12), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    borrower = db.Column(db.String(80), nullable=False)
    lender = db.Column(db.String(80), nullable=False)
    borrow_amount = db.Column(db.Float(12), nullable=False)
    repay_amount = db.Column(db.Float(12), nullable=False)
    balance = db.Column(db.Float(12), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    mode = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)






@app.route("/forget_password",methods=['GET','POST'])
def forget_password():
    if request.method=='POST':
        username=request.form.get("uname")
        password=request.form.get("upass")
        users = Tbluser.query.filter_by().all()
        user_list=[]
        for u in users:
            user_list.append(u.username)
        if username not in user_list:
            flash("User does not exist !!! Try different name","danger")
            return render_template("forget_password.html")
        else:
            user = Tbluser.query.filter_by(username=username).first()
            user.password = password
            db.session.commit()
            flash("Password updated successfully !!!","success")
            return redirect("/")
    return render_template("forget_password.html")


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get("uname")
        firstname=request.form.get("firstname")
        lastname=request.form.get("lastname")
        password=request.form.get("upass")
        users = Tbluser.query.filter_by().all()
        user_list=[]
        for u in users:
            user_list.append(u.username)
        if username in user_list:
            flash("User already exist !!! Try different name","danger")
            return render_template("registration.html")
        else:
            entry = Tbluser(username=username, firstname=firstname, lastname=lastname, password=password)
            db.session.add(entry)
            db.session.commit()
            flash("New user added successfully !!! Login now","success")
            return redirect("/")
    return render_template("registration.html")
#logout
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/")

# dashboard
@app.route("/",methods=["GET","POST"])
def index():
    username = request.form.get('uname')
    if 'user' in session and session['user']:
        username=(session['user'])
        labels=[]
        today = date.today()
        m = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV',
             'DEC']

        pos = today.month
        pos_year = today.year
        prev_year = today.year-1
        for i in range(pos, pos - 12, -1):
            if i >= 1:
                labels.append(m[i - 1]+" "+ str(today.year))  # in real m[pos] == July . so m[pos-1] == June
            else:
                labels.append(m[i - 1] + " " + str(today.year-1))

        income_current_year = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                                         (Tblincome.month),
                                                         func.year(Tblincome.date).label('year')).group_by(Tblincome.month,
                                                         func.year(Tblincome.date)).filter(func.year(Tblincome.date) == pos_year).order_by(Tblincome.date.desc()).all()
        expense_current_year = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                        Tblexpense.month,
                                                        func.year(Tblexpense.date).label('year')).group_by(Tblexpense.month,
                                                        func.year(Tblexpense.date)).filter(func.year(Tblexpense.date) == pos_year).order_by(
                                                        Tblexpense.date.desc()).all()

        income_current_year_length = len(income_current_year)
        current_year_month_list = []
        for i in (income_current_year):
            month_num = (i[1])
            from datetime import datetime
            datetime_object = datetime.strptime(str(month_num), "%m")
            #
            month_name = datetime_object.strftime("%B")
            current_year_month_list.append(month_name)

        income_prev_year =Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                                   (Tblincome.month),
                                                   func.year(Tblincome.date).label('year')).group_by(Tblincome.month,
                                                   func.year(Tblincome.date)).filter( func.year(Tblincome.date) == prev_year).order_by(Tblincome.date.desc()).all()
        expense_prev_year = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                     Tblexpense.month,
                                                     func.year(Tblexpense.date).label('year')).group_by(Tblexpense.month,
                                                     func.year(Tblexpense.date)).filter( func.year(Tblexpense.date) == prev_year).order_by(Tblexpense.date.desc()).all()

        income_prev_year_length = len(income_prev_year)
        prev_year_month_list=[]
        for i in (income_prev_year):
            month_num = (i[1])
            from datetime import datetime
            datetime_object = datetime.strptime(str(month_num), "%m")
            #
            month_name = datetime_object.strftime("%B")
            prev_year_month_list.append(month_name)

        income_sav = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                                   Tblincome.month,
                                                   func.year(Tblincome.date).label('year')).group_by(Tblincome.month,
                                                   func.year(Tblincome.date)).order_by(Tblincome.date.desc()).all()
        expense_sav = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                     Tblexpense.month,
                                                     func.year(Tblexpense.date).label('year')).group_by(Tblexpense.month,
                                                     func.year(Tblexpense.date)).order_by(Tblexpense.date.desc()).all()
        count=12
        income_dash=[]
        for si in income_sav:
            count=count-1
            if count >= 0:
                if si.month!=pos and si.year==pos_year:
                    if len(income_dash)==0 :
                        income_dash.append(0)
                        pass
                income_dash.append(si.total)
            else:
                break

        count = 12
        expense_dash = []
        for se in expense_sav:
            count = count - 1
            if count >= 0:
                if se.month!=pos and se.year==pos_year:
                    if len(expense_dash)==0 :
                        expense_dash.append(0)
                        pass
                expense_dash.append(se.total)
            else:
                break
        saving_dash=[]
        for i in range(12):
            saving_dash.append(income_dash[i]-expense_dash[i])

        # income = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total_income')).all()
        income = Tblincome.query.filter_by().all()
        expense = Tblexpense.query.filter_by(mode="Cash").all()
        transfer = Tbltransfer.query.filter_by(type="Cash").all()
        bank = Tblbankdeposit.query.filter_by().all()
        borrow_add = Tblborrow.query.filter(Tblborrow.mode=="Cash",Tblborrow.status=="add").all()
        borrow_subtract = Tblborrow.query.filter(Tblborrow.mode=="Cash",Tblborrow.status=="subtract").all()
        repay_add = Tblrepay.query.filter(Tblrepay.mode=="Cash",Tblrepay.status=="add").all()
        repay_subtract = Tblrepay.query.filter(Tblrepay.mode=="Cash",Tblrepay.status=="subtract").all()
        expense_bank = Tblexpense.query.filter_by(mode="Bank").all()
        ccpayment_bank = Tblccpayment.query.filter_by(mode="Bank").all()
        transfer_bank = Tbltransfer.query.filter_by(type="Bank").all()
        expense_card = Tblexpense.query.filter_by(mode="Credit card").all()
        ccpayment = Tblccpayment.query.filter_by().all()
        ccpayment_borrow = Tblborrow.query.filter_by(mode="Credit card").all()

        return render_template("dashboard.html",username=username,income=income,expense=expense,bank=bank,transfer=transfer,borrow_add=borrow_add,borrow_subtract=borrow_subtract
                               ,repay_add=repay_add,repay_subtract=repay_subtract,labels=labels,income_dash=income_dash,expense_dash=expense_dash
                               ,saving_dash=saving_dash,expense_bank=expense_bank,ccpayment_bank=ccpayment_bank,transfer_bank=transfer_bank,expense_card=expense_card,
                               ccpayment=ccpayment,ccpayment_borrow=ccpayment_borrow,pos_year=pos_year,prev_year=prev_year,income_prev_year=income_prev_year,
                               prev_year_month_list=prev_year_month_list,income_prev_year_length=income_prev_year_length,expense_prev_year=expense_prev_year,
                               income_current_year=income_current_year,current_year_month_list=current_year_month_list,income_current_year_length=income_current_year_length,
                               expense_current_year=expense_current_year)

    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('upass')
        user_list=[]
        all_user = Tbluser.query.filter_by().all()
        for u in all_user:
            user_list.append(u.username)
        if username not in user_list:
            flash("User does not exist !! Register first ", "danger")
            return render_template("login.html")
        else:
            user=(Tbluser.query.filter_by(username=username).first())
            if username == user.username and password == user.password:
                session['user'] = username
                labels = []
                today = date.today()
                m = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV',
                     'DEC']

                pos = today.month
                pos_year = today.year
                prev_year = today.year - 1
                for i in range(pos, pos - 12, -1):
                    if i >= 1:
                        labels.append(m[i - 1] + " " + str(today.year))  # in real m[pos] == July . so m[pos-1] == June
                    else:
                        labels.append(m[i - 1] + " " + str(today.year - 1))

                income_current_year = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                                                    (Tblincome.month),
                                                                    func.year(Tblincome.date).label('year')).group_by(
                    Tblincome.month,
                    func.year(Tblincome.date)).filter(func.year(Tblincome.date) == pos_year).order_by(
                    Tblincome.date.desc()).all()
                expense_current_year = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                                      Tblexpense.month,
                                                                      func.year(Tblexpense.date).label('year')).group_by(
                    Tblexpense.month,
                    func.year(Tblexpense.date)).filter(func.year(Tblexpense.date) == pos_year).order_by(
                    Tblexpense.date.desc()).all()

                income_current_year_length = len(income_current_year)
                current_year_month_list = []
                for i in (income_current_year):
                    month_num = (i[1])
                    from datetime import datetime
                    datetime_object = datetime.strptime(str(month_num), "%m")
                    #
                    month_name = datetime_object.strftime("%B")
                    current_year_month_list.append(month_name)

                income_prev_year = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                                                 (Tblincome.month),
                                                                 func.year(Tblincome.date).label('year')).group_by(
                    Tblincome.month,
                    func.year(Tblincome.date)).filter(func.year(Tblincome.date) == prev_year).order_by(
                    Tblincome.date.desc()).all()
                expense_prev_year = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                                   Tblexpense.month,
                                                                   func.year(Tblexpense.date).label('year')).group_by(
                    Tblexpense.month,
                    func.year(Tblexpense.date)).filter(func.year(Tblexpense.date) == prev_year).order_by(
                    Tblexpense.date.desc()).all()

                income_prev_year_length = len(income_prev_year)
                prev_year_month_list = []
                for i in (income_prev_year):
                    month_num = (i[1])
                    from datetime import datetime
                    datetime_object = datetime.strptime(str(month_num), "%m")
                    #
                    month_name = datetime_object.strftime("%B")
                    prev_year_month_list.append(month_name)

                income_sav = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                                           Tblincome.month,
                                                           func.year(Tblincome.date).label('year')).group_by(
                    Tblincome.month,
                    func.year(Tblincome.date)).order_by(Tblincome.date.desc()).all()
                expense_sav = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                             Tblexpense.month,
                                                             func.year(Tblexpense.date).label('year')).group_by(
                    Tblexpense.month,
                    func.year(Tblexpense.date)).order_by(Tblexpense.date.desc()).all()
                count = 12
                income_dash = []
                for si in income_sav:
                    count = count - 1
                    if count >= 0:
                        if si.month != pos and si.year == pos_year:
                            if len(income_dash) == 0:
                                income_dash.append(0)
                                pass
                        income_dash.append(si.total)
                    else:
                        break

                count = 12
                expense_dash = []
                for se in expense_sav:
                    count = count - 1
                    if count >= 0:
                        if se.month != pos and se.year == pos_year:
                            if len(expense_dash) == 0:
                                expense_dash.append(0)
                                pass
                        expense_dash.append(se.total)
                    else:
                        break
                saving_dash = []
                for i in range(12):
                    saving_dash.append(income_dash[i] - expense_dash[i])

                # income = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total_income')).all()
                income = Tblincome.query.filter_by().all()
                expense = Tblexpense.query.filter_by(mode="Cash").all()
                transfer = Tbltransfer.query.filter_by(type="Cash").all()
                bank = Tblbankdeposit.query.filter_by().all()
                borrow_add = Tblborrow.query.filter(Tblborrow.mode == "Cash", Tblborrow.status == "add").all()
                borrow_subtract = Tblborrow.query.filter(Tblborrow.mode == "Cash", Tblborrow.status == "subtract").all()
                repay_add = Tblrepay.query.filter(Tblrepay.mode == "Cash", Tblrepay.status == "add").all()
                repay_subtract = Tblrepay.query.filter(Tblrepay.mode == "Cash", Tblrepay.status == "subtract").all()
                expense_bank = Tblexpense.query.filter_by(mode="Bank").all()
                ccpayment_bank = Tblccpayment.query.filter_by(mode="Bank").all()
                transfer_bank = Tbltransfer.query.filter_by(type="Bank").all()
                expense_card = Tblexpense.query.filter_by(mode="Credit card").all()
                ccpayment = Tblccpayment.query.filter_by().all()
                ccpayment_borrow = Tblborrow.query.filter_by(mode="Credit card").all()

                flash("Welcome to Desi hisab admin panel", "success")
                return render_template("dashboard.html",username=username, income=income, expense=expense, bank=bank, transfer=transfer,
                                       borrow_add=borrow_add, borrow_subtract=borrow_subtract
                                       , repay_add=repay_add, repay_subtract=repay_subtract, labels=labels,
                                       income_dash=income_dash, expense_dash=expense_dash
                                       , saving_dash=saving_dash, expense_bank=expense_bank, ccpayment_bank=ccpayment_bank,
                                       transfer_bank=transfer_bank, expense_card=expense_card,
                                       ccpayment=ccpayment, ccpayment_borrow=ccpayment_borrow, pos_year=pos_year,
                                       prev_year=prev_year, income_prev_year=income_prev_year,
                                       prev_year_month_list=prev_year_month_list,
                                       income_prev_year_length=income_prev_year_length, expense_prev_year=expense_prev_year,
                                       income_current_year=income_current_year,
                                       current_year_month_list=current_year_month_list,
                                       income_current_year_length=income_current_year_length,
                                       expense_current_year=expense_current_year)
            else:
                flash("Incorrect password !! Try again","danger")
                return render_template("login.html")
    return render_template("login.html")

# income ----------------------------------------------->

@app.route("/income_analysis",methods=['GET','POST'])
def income_analysis():

    today = date.today()
    first_day = today.replace(day=1)
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    last_day = next_month - datetime.timedelta(days=next_month.day)
    inc = Tblincome.query.filter_by().all()
    income = Tblincome.query.filter(Tblincome.date.between(first_day,last_day)).order_by(Tblincome.date).all()
    name_list=[]
    for i in inc:
        name=str(i.name).lower()
        print(name)
        if name not in name_list:

            name_list.append(name)

    if request.method == 'POST':
        first_day=request.form.get('first_day')
        last_day=request.form.get('last_day')
        name= request.form.get("name")
        income = Tblincome.query.filter(Tblincome.date.between(first_day,last_day),Tblincome.name==name).order_by(Tblincome.date.desc()).all()
        return render_template("income_analysis.html", income=income, first_day=first_day, last_day=last_day,name_list=name_list)
    return render_template("income_analysis.html",income=income,first_day=first_day,last_day=last_day,name_list=name_list)


#view
@app.route("/income",methods=['GET','POST'])
def income():

    today = date.today()
    first_day = today.replace(day=1)
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    last_day = next_month - datetime.timedelta(days=next_month.day)
    income = Tblincome.query.filter(Tblincome.date.between(first_day,last_day)).order_by(Tblincome.date.desc()).all()

    if request.method == 'POST':
        first_day=request.form.get('first_day')
        last_day=request.form.get('last_day')
        income = Tblincome.query.filter(Tblincome.date.between(first_day,last_day)).order_by(Tblincome.date.desc()).all()
        return render_template("income.html", income=income, first_day=first_day, last_day=last_day)
    return render_template("income.html",income=income,first_day=first_day,last_day=last_day)


# add

@app.route("/income/add",methods=['GET','POST'])
def addincome():

    # id,type,name,description,date,amount,start_date,end_date,month
    # today = date.today()
    # income = Tblincome.query.filter(Tblincome.date.between(first_day, last_day)).all()

    if (request.method=='POST'):
        type=request.form.get('type')
        name=request.form.get('name')
        description=request.form.get('description')
        amount=request.form.get('amount')
        date=request.form.get('date')
        start_date=request.form.get('start_date')
        end_date=request.form.get('end_date')
        from datetime import datetime
        temp_date=datetime.strptime(date, '%Y-%m-%d').date()
        month = temp_date.month

        entry = Tblincome(type=type,name=name,description=description,date=date,amount=amount,start_date=start_date,end_date=end_date,month=month)
        db.session.add(entry)
        db.session.commit()
        flash("Income added successfully !!!")

    from datetime import date
    today = date.today()
    first_day = today.replace(day=1)
    import datetime
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    last_day = next_month - datetime.timedelta(days=next_month.day)
    income = Tblincome.query.filter(Tblincome.date.between(first_day, last_day)).order_by(Tblincome.date.desc()).all()
    return render_template("income.html",income=income,first_day=first_day,last_day=last_day,submit=True)



# edit/update

@app.route("/income/update",methods=['GET','POST'])
def updateincome():
    if request.method=='POST':
        income = Tblincome.query.filter_by(id=request.form.get('id')).first()
        income.type = request.form.get('type')
        income.name = request.form.get('name')
        income.description = request.form.get('description')
        income.amount = request.form.get('amount')
        income.date = request.form.get('date')
        income.start_date = request.form.get('start_date')
        income.end_date = request.form.get('end_date')
        from datetime import datetime
        temp_date = datetime.strptime(income.date, '%Y-%m-%d').date()
        income.month = temp_date.month
        db.session.commit()
        flash("Income updated successfully !!!")
        return redirect("/income")

# delete

@app.route("/delete/income/<string:id>", methods=['GET','POST'])
def deleteincome(id):

    income = Tblincome.query.filter_by(id=id).first()
    db.session.delete(income)
    db.session.commit()
    flash("Income deleted successfully !!!")
    return redirect("/income")

# expense ----------------------------------------------->

#view

@app.route("/expense",methods=['GET','POST'])
def expense():

    today = date.today()
    first_day = today.replace(day=1)
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    last_day = next_month - datetime.timedelta(days=next_month.day)
    expense = Tblexpense.query.filter(Tblexpense.date.between(first_day,last_day)).order_by(Tblexpense.date.desc()).all()
    bank = Tblbanks.query.filter_by().all()
    credit = Tblcreditcard.query.filter_by().all()
    category = Tblcategory.query.filter_by().all()

    if request.method == 'POST':
        first_day=request.form.get('first_day')
        last_day=request.form.get('last_day')
        expense = Tblexpense.query.filter(Tblexpense.date.between(first_day,last_day)).order_by(Tblexpense.date.desc()).all()

        return render_template("expense.html", expense=expense, first_day=first_day, last_day=last_day,bank=bank,category=category,credit=credit)
    return render_template("expense.html",expense=expense,first_day=first_day,last_day=last_day,bank=bank,category=category,credit=credit)


# add

@app.route("/expense/add",methods=['GET','POST'])
def addexpense():
    # date,name,cid,mode,amount,description,bid,ccid,month
    # today = date.today()
    # income = Tblincome.query.filter(Tblincome.date.between(first_day, last_day)).all()

    if (request.method=='POST'):
        date=request.form.get('date')
        name = request.form.get('name')
        cid = request.form.get('cid')
        mode=request.form.get('mode')
        amount=request.form.get('amount')
        description=request.form.get('description')
        bid=request.form.get('bid')
        ccid=request.form.get('ccid')
        from datetime import datetime
        temp_date=datetime.strptime(date, '%Y-%m-%d').date()
        month = temp_date.month

        entry = Tblexpense(date=date,name=name,cid=cid,mode=mode,amount=amount,description=description,bid=bid,ccid=ccid,month=month)
        db.session.add(entry)
        db.session.commit()
        flash("Expense added successfully !!!")

    from datetime import date
    today = date.today()
    first_day = today.replace(day=1)
    import datetime
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    last_day = next_month - datetime.timedelta(days=next_month.day)
    expense = Tblexpense.query.filter(Tblexpense.date.between(first_day, last_day)).order_by(Tblexpense.date.desc()).all()
    bank = Tblbanks.query.filter_by().all()
    credit = Tblcreditcard.query.filter_by().all()
    category = Tblcategory.query.filter_by().all()
    return render_template("expense.html",submit=True,expense=expense,first_day=first_day,last_day=last_day,bank=bank,category=category,credit=credit)


# edit/update

@app.route("/expense/update",methods=['GET','POST'])
def updateexpense():
    if request.method=='POST':
        expense = Tblexpense.query.filter_by(id=request.form.get('id')).first()
        expense.date = request.form.get('date')
        expense.name = request.form.get('name')
        expense.cid = request.form.get('cid')
        expense.mode = request.form.get('mode')
        expense.amount = request.form.get('amount')
        expense.description = request.form.get('description')
        expense.bid = request.form.get('bid')
        expense.ccid = request.form.get('ccid')
        from datetime import datetime
        temp_date = datetime.strptime(expense.date, '%Y-%m-%d').date()
        expense.month = temp_date.month
        db.session.commit()
        flash("Expense updated successfully !!!")
        return redirect("/expense")

@app.route("/delete/expense/<string:id>", methods=['GET','POST'])
def deleteexpense(id):

    expense = Tblexpense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully !!!")
    return redirect("/expense")

# saving ----------------------------------------------->


@app.route("/saving", methods=['GET','POST'])
def saving():
    income_sav = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                               Tblincome.month,
                                               func.year(Tblincome.date).label('year')).group_by(Tblincome.month,
                                               func.year(Tblincome.date)).order_by(Tblincome.date.desc()).all()
    expense_sav = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                 Tblexpense.month,
                                                 func.year(Tblexpense.date).label('year')).group_by(Tblexpense.month,
                                                 func.year(Tblexpense.date)).order_by(Tblexpense.date.desc()).all()

    month_list = []
    year_list = []
    inc_size=len(income_sav)
    exp_size=len(expense_sav)

    size=len(income_sav)
    if size < len(expense_sav):
        for y in expense_sav:
            if y.year not in year_list:
                year_list.append(y.year)

        for i in expense_sav:
            month_num = (i.month)
            from datetime import datetime
            datetime_object = datetime.strptime(str(month_num), "%m")
            #
            month_name = datetime_object.strftime("%B")
            month_list.append(month_name)
    else:
        for y in income_sav:
            if y.year not in year_list:
                year_list.append(y.year)


        for i in income_sav:
            month_num = (i.month)
            from datetime import datetime
            datetime_object = datetime.strptime(str(month_num), "%m")
            #
            month_name = datetime_object.strftime("%B")
            month_list.append(month_name)

        if request.method == 'POST':
            print("post")
            year = request.form.get("year")
            print(year)
            if year=="0":
                return redirect("/saving")
            else:
                income_sav = Tblincome.query.with_entities(func.sum(Tblincome.amount).label('total'),
                                                           Tblincome.month,
                                                           func.year(Tblincome.date).label('year')).filter(func.year(Tblincome.date)==year).group_by(Tblincome.month,
                                                           func.year(Tblincome.date)).order_by(Tblincome.date.desc()).all()
                expense_sav = Tblexpense.query.with_entities(func.sum(Tblexpense.amount).label('total'),
                                                             Tblexpense.month,
                                                             func.year(Tblexpense.date).label('year')).filter(func.year(Tblexpense.date)==year).group_by(Tblexpense.month,
                                                             func.year(Tblexpense.date)).order_by(Tblexpense.date.desc()).all()
                size = len(income_sav)

                inc_size = len(income_sav)
                exp_size = len(expense_sav)
                print(inc_size)
                print(exp_size)
                month_list = []
                for i in income_sav:
                    month_num = (i.month)
                    from datetime import datetime
                    datetime_object = datetime.strptime(str(month_num), "%m")
                    #
                    month_name = datetime_object.strftime("%B")
                    month_list.append(month_name)

                return render_template("saving.html", income_sav=income_sav, year_list=year_list, expense_sav=expense_sav,
                                   month_list=month_list, size=size,inc_size=inc_size,exp_size=exp_size)
    return render_template("saving.html",income_sav=income_sav,year_list=year_list,expense_sav=expense_sav,month_list=month_list,size=size,inc_size=inc_size,exp_size=exp_size)


# category ----------------------------------------------->

# view/add

@app.route("/category", methods=['GET','POST'])
def category():

    if request.method=='POST':
        category = request.form.get("category")
        entry = Tblcategory(category=category)
        db.session.add(entry)
        db.session.commit()
        flash("Category added successfully !!!")
        # category = Tblcategory.query.filter_by().all()
        return redirect("/expense")

#delete

@app.route("/delete/category/<string:id>", methods=['GET','POST'])
def deletecategory(id):

    category = Tblcategory.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully !!!")
    return redirect("/expense")


# banks ----------------------------------------------->

@app.route("/bank", methods=['GET','POST'])
def bank():
    bank = Tblbanks.query.filter_by().all()
    bank_deposit = Tblbankdeposit.query.filter_by().order_by(Tblbankdeposit.date.desc()).all()
    year_list = []
    for b in bank_deposit[:-1]:
        tod = (b.date)
        from datetime import datetime
        datetime_object = datetime.strptime(str(tod), "%Y-%m-%d")
        if datetime_object.year not in year_list:
            year_list.append(datetime_object.year)
    if request.method == 'POST':
        year=request.form.get("year")
        bank_list = request.form.get("bank_list")

        if(year=="0" and bank_list=="0"):
            return redirect("/bank")

        elif(year!="0" and bank_list=="0"):
            bank = Tblbanks.query.filter_by().all()
            bank_deposit = Tblbankdeposit.query.filter(func.year(Tblbankdeposit.date)==year).order_by(Tblbankdeposit.date.desc()).all()
            return render_template("bank.html", bank=bank, bank_deposit=bank_deposit, year_list=year_list)

        elif (year == "0" and bank_list != "0"):
            bank = Tblbanks.query.filter_by().all()
            bank_deposit = Tblbankdeposit.query.filter(Tblbankdeposit.bid == bank_list).order_by(
                Tblbankdeposit.date.desc()).all()
            return render_template("bank.html", bank=bank, bank_deposit=bank_deposit, year_list=year_list)

        elif (year != "0" and bank_list != "0"):
            bank = Tblbanks.query.filter_by().all()
            bank_deposit = Tblbankdeposit.query.filter(func.year(Tblbankdeposit.date)==year,Tblbankdeposit.bid == bank_list).order_by(
                Tblbankdeposit.date.desc()).all()
            return render_template("bank.html", bank=bank, bank_deposit=bank_deposit, year_list=year_list)
        else:
            return redirect("/bank")

    return render_template("bank.html",bank=bank,bank_deposit=bank_deposit,year_list=year_list)


@app.route("/bank/add", methods=['GET','POST'])
def addbank():
    if request.method=='POST':
        bank = request.form.get("bank")
        entry = Tblbanks(bank=bank)
        db.session.add(entry)
        db.session.commit()
        flash("Bank added successfully !!!")
        # category = Tblcategory.query.filter_by().all()
        return redirect("/bank")

@app.route("/delete/bank/<string:id>", methods=['GET','POST'])
def deletebank(id):

    bank = Tblbanks.query.filter_by(id=id).first()
    db.session.delete(bank)
    db.session.commit()
    flash("Bank deleted successfully !!!")
    return redirect("/bank")


# banks deposit----------------------------------------------->

#add
@app.route("/deposit/add", methods=['GET','POST'])
def adddeposit():
    if request.method=='POST':
        date = request.form.get("date")
        bid = request.form.get("bid")
        amount = request.form.get("amount")
        description = request.form.get("description")
        entry = Tblbankdeposit(date=date,bid=bid,amount=amount,description=description)
        db.session.add(entry)
        db.session.commit()
        flash("Bank deposit added successfully !!!")
        # category = Tblcategory.query.filter_by().all()
        return redirect("/bank")

#update
@app.route("/deposit/update", methods=['GET','POST'])
def updatedeposit():
    if request.method=='POST':
        bank_deposit = Tblbankdeposit.query.filter_by(id=request.form.get('id')).first()
        bank_deposit.date = request.form.get("date")
        bank_deposit.bid = request.form.get("bid")
        bank_deposit.amount = request.form.get("amount")
        bank_deposit.description = request.form.get("description")
        db.session.commit()
        flash("Bank deposit updated successfully !!!")
        return redirect("/bank")

#delete
@app.route("/delete/deposit/<string:id>", methods=['GET','POST'])
def deletedeposit(id):

    bank_deposit = Tblbankdeposit.query.filter_by(id=id).first()
    db.session.delete(bank_deposit)
    db.session.commit()
    flash("Bank deposit deleted successfully !!!")
    return redirect("/bank")


# Credit card----------------------------------------------->


@app.route("/creditcard",methods=['GET','POST'])
def creditcard():
    c_card = Tblcreditcard.query.filter_by().all()
    bank = Tblbanks.query.filter_by().all()
    payment = Tblccpayment.query.filter_by().order_by(Tblccpayment.date.desc()).all()
    pt = Tblccpayment.query.with_entities(func.year(Tblccpayment.date).label("year")).filter_by().order_by(Tblccpayment.date.desc()).all()
    cc_expense_total = Tblexpense.query.with_entities(Tblexpense.ccid,func.sum(Tblexpense.amount).label("cc_exp")).group_by(Tblexpense.ccid)
    cc_payment_total = Tblccpayment.query.with_entities(Tblccpayment.ccid,func.sum(Tblccpayment.amount).label("cc_pay")).group_by(Tblccpayment.ccid)
    cc_borrow_total = Tblborrow.query.with_entities(Tblborrow.ccid,func.sum(Tblborrow.borrow_amount).label("cc_borrow")).group_by(Tblborrow.ccid)

    cc_id=[]
    year_list=[]
    for p in pt:
        if p.year not in year_list:
            year_list.append(p.year)

    for cc in c_card:
        cc_id.append(cc.id)

    borrow_dict={}
    exp_dict={}
    pay_dict={}
    for i in cc_borrow_total:
        borrow_dict[i.ccid]=i.cc_borrow
    for i in cc_payment_total:
        pay_dict[i.ccid]=i.cc_pay
    for i in cc_expense_total:
        exp_dict[i.ccid]=i.cc_exp

    final_dict={}
    for n in (cc_id):
        if n in borrow_dict.keys():
            if n in exp_dict.keys():
                final_dict[n]=borrow_dict[n]+exp_dict[n]
            else:
                final_dict[n] = borrow_dict[n] + 0

        elif n not in borrow_dict.keys():
            if n in exp_dict.keys():
                final_dict[n]=exp_dict[n]
            else:
                final_dict[n]=0



    ccdict={}
    for c in cc_id:
        if c not in pay_dict.keys():
            ccdict[c] = (final_dict[c] - 0)
        else:
            ccdict[c]=(final_dict[c]-pay_dict[c])


    if request.method == 'POST':
        year=request.form.get("year")
        card_list = request.form.get("card_list")

        if(year=="0" and card_list=="0"):
            return redirect("/creditcard")
    #
        elif(year!="0" and card_list=="0"):
            payment = Tblccpayment.query.filter(func.year(Tblccpayment.date)==year).order_by(Tblccpayment.date.desc()).all()
            return render_template("credicard.html",year_list=year_list,c_card=c_card,payment=payment,bank=bank,cc_expense_total=cc_expense_total,ccdict=json.dumps(ccdict))

        elif (year == "0" and card_list != "0"):
            payment = Tblccpayment.query.filter(Tblccpayment.ccid == card_list).order_by(
                        Tblccpayment.date.desc()).all()
            return render_template("credicard.html",year_list=year_list,c_card=c_card,payment=payment,bank=bank,cc_expense_total=cc_expense_total,ccdict=json.dumps(ccdict))

        elif (year != "0" and card_list != "0"):
            payment = Tblccpayment.query.filter(func.year(Tblccpayment.date)==year,Tblccpayment.ccid == card_list).order_by(
                Tblccpayment.date.desc()).all()
            return render_template("credicard.html",year_list=year_list,c_card=c_card,payment=payment,bank=bank,cc_expense_total=cc_expense_total,ccdict=json.dumps(ccdict))
        else:
            return redirect("/creditcard")

    return render_template("credicard.html",year_list=year_list,c_card=c_card,payment=payment,bank=bank,cc_expense_total=cc_expense_total,ccdict=json.dumps(ccdict))

# add credit card

@app.route("/creditcard/add",methods=['GET','POST'])
def addcreditcard():
    c_card=Tblcreditcard.query.filter_by().all()
    if request.method == 'POST':
        credit_card=request.form.get('credit_card')
        total_credit=request.form.get('total_credit')
        entry=Tblcreditcard(credit_card=credit_card,total_credit=total_credit)
        db.session.add(entry)
        db.session.commit()
        flash("Credit card added successfully !!!")
        return redirect("/creditcard")

    return render_template("addcreditcard.html",c_card=c_card)


#update
@app.route("/creditcard/update", methods=['GET','POST'])
def updatecreditcard():
    if request.method=='POST':
        creditcard = Tblcreditcard.query.filter_by(id=request.form.get('id')).first()
        creditcard.credit_card = request.form.get("credit_card")
        creditcard.total_credit = request.form.get("total_credit")
        db.session.commit()
        flash("Credit card updated successfully !!!")
        return redirect("/creditcard/add")


#delete
@app.route("/delete/creditcard/<string:id>", methods=['GET','POST'])
def deletecreditcard(id):

    creditcard = Tblcreditcard.query.filter_by(id=id).first()
    db.session.delete(creditcard)
    db.session.commit()
    flash("Credit card deleted successfully !!!")
    return redirect("/creditcard/add")


# add payment

@app.route("/payment/add",methods=['GET','POST'])
def addpayment():
    if request.method == 'POST':
        ccid = request.form.get('ccid')
        bid = request.form.get('bid')
        date = request.form.get('date')
        name = request.form.get('name')
        mode = request.form.get('mode')
        amount = request.form.get('amount')
        description = request.form.get('description')
        entry = Tblccpayment(ccid=ccid, bid=bid, date=date, name=name, mode=mode, amount=amount,
                             description=description)
        db.session.add(entry)
        db.session.commit()
        flash("Payment added successfully !!!")
        return redirect("/creditcard")


#payment update
@app.route("/payment/update", methods=['GET','POST'])
def updatepayment():
    if request.method=='POST':
        payment = Tblccpayment.query.filter_by(id=request.form.get('id')).first()
        payment.ccid = request.form.get('ccid')
        payment.bid = request.form.get('bid')
        payment.date = request.form.get('date')
        payment.name = request.form.get('name')
        payment.mode = request.form.get('mode')
        payment.amount = request.form.get('amount')
        payment.description = request.form.get('description')
        db.session.commit()
        flash("Payment updated successfully !!!")
        return redirect("/creditcard")


#payment delete
@app.route("/delete/payment/<string:id>", methods=['GET','POST'])
def deletepayment(id):

    payment = Tblccpayment.query.filter_by(id=id).first()
    db.session.delete(payment)
    db.session.commit()
    flash("Payment deleted successfully !!!")
    return redirect("/creditcard")


# Transfer----------------------------------------------->

@app.route("/transfer",methods=['GET','POST'])
def transfer():

    countryList = [
        "Afghanistan",
        "Åland Islands",
        "Albania",
        "Algeria",
        "American Samoa",
        "Andorra",
        "Angola",
        "Anguilla",
        "Antarctica",
        "Antigua and Barbuda",
        "Argentina",
        "Armenia",
        "Aruba",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Bahamas (the)",
        "Bahrain",
        "Bangladesh",
        "Barbados",
        "Belarus",
        "Belgium",
        "Belize",
        "Benin",
        "Bermuda",
        "Bhutan",
        "Bolivia (Plurinational State of)",
        "Bonaire, Sint Eustatius and Saba",
        "Bosnia and Herzegovina",
        "Botswana",
        "Bouvet Island",
        "Brazil",
        "British Indian Ocean Territory (the)",
        "Brunei Darussalam",
        "Bulgaria",
        "Burkina Faso",
        "Burundi",
        "Cabo Verde",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Cayman Islands (the)",
        "Central African Republic (the)",
        "Chad",
        "Chile",
        "China",
        "Christmas Island",
        "Cocos (Keeling) Islands (the)",
        "Colombia",
        "Comoros (the)",
        "Congo (the Democratic Republic of the)",
        "Congo (the)",
        "Cook Islands (the)",
        "Costa Rica",
        "Croatia",
        "Cuba",
        "Curaçao",
        "Cyprus",
        "Czechia",
        "Côte d'Ivoire",
        "Denmark",
        "Djibouti",
        "Dominica",
        "Dominican Republic (the)",
        "Ecuador",
        "Egypt",
        "El Salvador",
        "Equatorial Guinea",
        "Eritrea",
        "Estonia",
        "Eswatini",
        "Ethiopia",
        "Falkland Islands (the) [Malvinas]",
        "Faroe Islands (the)",
        "Fiji",
        "Finland",
        "France",
        "French Guiana",
        "French Polynesia",
        "French Southern Territories (the)",
        "Gabon",
        "Gambia (the)",
        "Georgia",
        "Germany",
        "Ghana",
        "Gibraltar",
        "Greece",
        "Greenland",
        "Grenada",
        "Guadeloupe",
        "Guam",
        "Guatemala",
        "Guernsey",
        "Guinea",
        "Guinea-Bissau",
        "Guyana",
        "Haiti",
        "Heard Island and McDonald Islands",
        "Holy See (the)",
        "Honduras",
        "Hong Kong",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Iran (Islamic Republic of)",
        "Iraq",
        "Ireland",
        "Isle of Man",
        "Israel",
        "Italy",
        "Jamaica",
        "Japan",
        "Jersey",
        "Jordan",
        "Kazakhstan",
        "Kenya",
        "Kiribati",
        "Korea (the Democratic People's Republic of)",
        "Korea (the Republic of)",
        "Kuwait",
        "Kyrgyzstan",
        "Lao People's Democratic Republic (the)",
        "Latvia",
        "Lebanon",
        "Lesotho",
        "Liberia",
        "Libya",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Macao",
        "Madagascar",
        "Malawi",
        "Malaysia",
        "Maldives",
        "Mali",
        "Malta",
        "Marshall Islands (the)",
        "Martinique",
        "Mauritania",
        "Mauritius",
        "Mayotte",
        "Mexico",
        "Micronesia (Federated States of)",
        "Moldova (the Republic of)",
        "Monaco",
        "Mongolia",
        "Montenegro",
        "Montserrat",
        "Morocco",
        "Mozambique",
        "Myanmar",
        "Namibia",
        "Nauru",
        "Nepal",
        "Netherlands (the)",
        "New Caledonia",
        "New Zealand",
        "Nicaragua",
        "Niger (the)",
        "Nigeria",
        "Niue",
        "Norfolk Island",
        "Northern Mariana Islands (the)",
        "Norway",
        "Oman",
        "Pakistan",
        "Palau",
        "Palestine, State of",
        "Panama",
        "Papua New Guinea",
        "Paraguay",
        "Peru",
        "Philippines (the)",
        "Pitcairn",
        "Poland",
        "Portugal",
        "Puerto Rico",
        "Qatar",
        "Republic of North Macedonia",
        "Romania",
        "Russian Federation (the)",
        "Rwanda",
        "Réunion",
        "Saint Barthélemy",
        "Saint Helena, Ascension and Tristan da Cunha",
        "Saint Kitts and Nevis",
        "Saint Lucia",
        "Saint Martin (French part)",
        "Saint Pierre and Miquelon",
        "Saint Vincent and the Grenadines",
        "Samoa",
        "San Marino",
        "Sao Tome and Principe",
        "Saudi Arabia",
        "Senegal",
        "Serbia",
        "Seychelles",
        "Sierra Leone",
        "Singapore",
        "Sint Maarten (Dutch part)",
        "Slovakia",
        "Slovenia",
        "Solomon Islands",
        "Somalia",
        "South Africa",
        "South Georgia and the South Sandwich Islands",
        "South Sudan",
        "Spain",
        "Sri Lanka",
        "Sudan (the)",
        "Suriname",
        "Svalbard and Jan Mayen",
        "Sweden",
        "Switzerland",
        "Syrian Arab Republic",
        "Taiwan (Province of China)",
        "Tajikistan",
        "Tanzania, United Republic of",
        "Thailand",
        "Timor-Leste",
        "Togo",
        "Tokelau",
        "Tonga",
        "Trinidad and Tobago",
        "Tunisia",
        "Turkey",
        "Turkmenistan",
        "Turks and Caicos Islands (the)",
        "Tuvalu",
        "Uganda",
        "Ukraine",
        "United Arab Emirates (the)",
        "United Kingdom of Great Britain and Northern Ireland (the)",
        "United States Minor Outlying Islands (the)",
        "United States of America (the)",
        "Uruguay",
        "Uzbekistan",
        "Vanuatu",
        "Venezuela (Bolivarian Republic of)",
        "Viet Nam",
        "Virgin Islands (British)",
        "Virgin Islands (U.S.)",
        "Wallis and Futuna",
        "Western Sahara",
        "Yemen",
        "Zambia",
        "Zimbabwe"
    ]
    transfer=Tbltransfer.query.filter_by().order_by(Tbltransfer.date.desc()).all()
    t_year=Tbltransfer.query.with_entities(func.year(Tbltransfer.date).label('year')).filter_by().order_by(Tbltransfer.date.desc()).all()
    year_list=[]
    for y in t_year:
        if y.year not in year_list:
            year_list.append(y.year)
    if request.method == 'POST':
        year = request.form.get("year")
        if year=="0":
            return redirect("/transfer")
        else:
            transfer = Tbltransfer.query.filter(func.year(Tbltransfer.date)==year).order_by(Tbltransfer.date.desc()).all()
            return render_template("transfer.html", transfer=transfer,year_list=year_list,countryList=countryList)
    return render_template("transfer.html",transfer=transfer,year_list=year_list,countryList=countryList)


# add transfer

@app.route("/transfer/add",methods=['GET','POST'])
def addtransfer():
    if request.method == 'POST':
        date = request.form.get('date')
        payee = request.form.get('payee')
        receiver = request.form.get('receiver')
        country = request.form.get('country')
        type = request.form.get('type')
        sending_amount = request.form.get('sending_amount')
        rate = request.form.get('rate')
        received_amount = request.form.get('received_amount')
        description = request.form.get('description')
        entry=Tbltransfer(date=date,payee=payee,receiver=receiver,country=country,type=type,sending_amount=sending_amount,rate=rate,received_amount=received_amount,description=description)
        db.session.add(entry)
        db.session.commit()
        flash("Transfer added successfully !!!")
        return redirect("/transfer")


#transfer update
@app.route("/transfer/update", methods=['GET','POST'])
def updatetransfer():
    if request.method=='POST':
        transfer = Tbltransfer.query.filter_by(id=request.form.get('id')).first()
        transfer.date = request.form.get('date')
        transfer.payee = request.form.get('payee')
        transfer.receiver = request.form.get('receiver')
        transfer.country = request.form.get('country')
        transfer.type = request.form.get('type')
        transfer.sending_amount = request.form.get('sending_amount')
        transfer.rate = request.form.get('rate')
        transfer.received_amount = request.form.get('received_amount')
        transfer.description = request.form.get('description')
        db.session.commit()
        flash("Transfer updated successfully !!!")
        return redirect("/transfer")


#transfer delete
@app.route("/delete/transfer/<string:id>", methods=['GET','POST'])
def deletetransfer(id):

    transfer = Tbltransfer.query.filter_by(id=id).first()
    db.session.delete(transfer)
    db.session.commit()
    flash("Transfer deleted successfully !!!")
    return redirect("/transfer")



# Borrow/Lending----------------------------------------------->

@app.route("/borrow_lending",methods=['GET','POST'])
def borrow_lending():
    # entry = Tblborrow(
    ROWS_PER_PAGE = 20
    page = request.args.get('page', 1, type=int)
    borrow=Tblborrow.query.filter_by().order_by(Tblborrow.trans_no.desc()).all()

    borr=Tblborrow.query.order_by(Tblborrow.trans_no.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    # year=request.form.get("year")
    # status = False
    # print(status)
    cards= Tblcreditcard.query.filter_by().all()
    banks= Tblbanks.query.filter_by().all()

    b_year=Tblborrow.query.with_entities(func.year(Tblborrow.date).label('year')).filter_by().order_by(Tblborrow.date.desc()).all()
    year_list=[]
    type_list=[]
    trans_list=[]
    for y in b_year:
        if y.year not in year_list:
            year_list.append(y.year)
    for t in borrow:
        trans_list.append(t.trans_no)
    last_trans=(max(trans_list))
    next_trans_no=(int(last_trans)+1)
    if request.method == 'POST':
        year = request.form.get("year")
        filter_type = request.form.get("filter_type")
        if (year == "0" and filter_type == "0"):
            return redirect("/borrow_lending")
            #
        elif (year != "0" and filter_type == "0"):
            borrow=Tblborrow.query.filter(func.year(Tblborrow.date) == year).order_by(Tblborrow.trans_no.desc()).all()
            ROWS_PER_PAGE = len(borrow)
            borr = Tblborrow.query.filter(func.year(Tblborrow.date) == year).order_by(Tblborrow.trans_no.desc()).paginate(page=page,per_page=ROWS_PER_PAGE)

            return render_template("borrow_lending.html",borr=borr,cards=cards,banks=banks,year_list=year_list,next_trans_no=next_trans_no)

        elif (year == "0" and filter_type != "0"):
            borrow = Tblborrow.query.filter(Tblborrow.type==filter_type).order_by(Tblborrow.trans_no.desc()).all()
            ROWS_PER_PAGE = len(borrow)
            borr = Tblborrow.query.filter(Tblborrow.type==filter_type).order_by(Tblborrow.trans_no.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
            return render_template("borrow_lending.html",borr=borr,cards=cards,banks=banks,year_list=year_list,next_trans_no=next_trans_no)

        elif (year != "0" and filter_type != "0"):
            borrow = Tblborrow.query.filter(func.year(Tblborrow.date) == year,Tblborrow.type==filter_type).order_by(Tblborrow.trans_no.desc()).all()
            ROWS_PER_PAGE = len(borrow)
            borr = Tblborrow.query.filter(func.year(Tblborrow.date) == year,Tblborrow.type==filter_type).order_by(Tblborrow.trans_no.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
            return render_template("borrow_lending.html", borr=borr,cards=cards,banks=banks, year_list=year_list,
                                   next_trans_no=next_trans_no)
        else:
            return redirect("/borrow_lending")
    return render_template("borrow_lending.html",borr=borr,borrow=borrow,cards=cards,banks=banks,year_list=year_list,next_trans_no=next_trans_no)


# add transaction

@app.route("/borrower/add",methods=['GET','POST'])
def addtransaction():
    if request.method == 'POST':
        date = request.form.get('date')
        trans_no = request.form.get('trans_no')
        description = request.form.get('description')
        borrower = request.form.get('borrower')
        lender = request.form.get('lender')
        bid = request.form.get('bid')
        ccid = request.form.get('ccid')
        borrow_amount = request.form.get('borrow_amount')
        repay_amount = 0.00
        balance = request.form.get('borrow_amount')
        type = request.form.get('type')
        mode = request.form.get('mode')
        status = request.form.get('status')
        entry=Tblborrow(date=date,trans_no=trans_no,description=description,
                          borrower=borrower,lender=lender,bid=bid,ccid=ccid,
                        borrow_amount=borrow_amount,repay_amount=repay_amount,balance=balance,
                          type=type,mode=mode,status=status)

        db.session.add(entry)
        db.session.commit()
        flash("Transaction added successfully !!!")
        return redirect("/borrow_lending")


#transaction update
@app.route("/borrower/update", methods=['GET','POST'])
def updatetransaction():
    if request.method=='POST':
        borrower = Tblborrow.query.filter_by(id=request.form.get('id')).first()
        borrower.date = request.form.get('date')
        borrower.trans_no = request.form.get('trans_no')
        borrower.description = request.form.get('description')
        borrower.borrower = request.form.get('borrower')
        borrower.lender = request.form.get('lender')
        borrower.bid = request.form.get('bid')
        borrower.ccid = request.form.get('ccid')
        borrower.borrow_amount = request.form.get('borrow_amount')
        borrower.repay_amount = 0.00
        borrower.balance = request.form.get('borrow_amount')
        borrower.type = request.form.get('type')
        borrower.mode = request.form.get('mode')
        borrower.status = request.form.get('status')
        db.session.commit()
        flash("Transaction updated successfully !!!")
        return redirect("/borrow_lending")


#transaction delete
@app.route("/delete/borrower/<string:id>", methods=['GET','POST'])
def deletetransaction(id):

    borrower = Tblborrow.query.filter_by(id=id).first()
    db.session.delete(borrower)
    db.session.commit()
    flash("Transaction deleted successfully !!!")
    return redirect("/borrow_lending")



# Repay----------------------------------------------->

@app.route("/repay",methods=['GET','POST'])
def repay():
    borrow = Tblborrow.query.filter_by().order_by(Tblborrow.trans_no.desc()).all()
    b_year = Tblborrow.query.with_entities(func.year(Tblborrow.date).label('year')).filter_by().order_by(
        Tblborrow.date.desc()).all()

    year_list = []
    type_list = []
    trans_list = []
    for y in b_year:
        if y.year not in year_list:
            year_list.append(y.year)
    for t in borrow:
        trans_list.append(t.trans_no)
    last_trans = (max(trans_list))
    next_trans_no = (int(last_trans) + 1)
    if request.method == 'POST':
        year = request.form.get("year")
        filter_type = request.form.get("filter_type")
        if (year == "0" and filter_type == "0"):
            return redirect("/repay")
            #
        elif (year != "0" and filter_type == "0"):
            borrow = Tblborrow.query.filter(func.year(Tblborrow.date) == year).order_by(Tblborrow.date.desc()).all()
            return render_template("repay.html", borrow=borrow, year_list=year_list,
                                   next_trans_no=next_trans_no)

        elif (year == "0" and filter_type != "0"):
            borrow = Tblborrow.query.filter(Tblborrow.type == filter_type).order_by(Tblborrow.date.desc()).all()
            return render_template("repay.html", borrow=borrow, year_list=year_list,
                                   next_trans_no=next_trans_no)

        elif (year != "0" and filter_type != "0"):
            borrow = Tblborrow.query.filter(func.year(Tblborrow.date) == year, Tblborrow.type == filter_type).order_by(
                Tblborrow.date.desc()).all()
            return render_template("repay.html", borrow=borrow, year_list=year_list,
                                   next_trans_no=next_trans_no)
        else:
            return redirect("/repay")
    return render_template("repay.html", borrow=borrow, year_list=year_list, next_trans_no=next_trans_no)



# add transaction

@app.route("/repay/add",methods=['GET','POST'])
def addrepay():
    if request.method == 'POST':
        date = request.form.get('date')
        trans_no = request.form.get('trans_no')
        description = request.form.get('description')
        borrower = request.form.get('borrower')
        lender = request.form.get('lender')
        borrow_amount = request.form.get('borrow_amount')
        repay_amount = request.form.get('repay_amount')
        form_balance = request.form.get('balance')
        balance = float(form_balance)-float(repay_amount)
        type = request.form.get('type')
        mode = request.form.get('mode')
        status = request.form.get('status')
        entry=Tblrepay(date=date,trans_no=trans_no,description=description,
                          borrower=borrower,lender=lender,
                       borrow_amount=borrow_amount,repay_amount=repay_amount,balance=balance,
                          type=type,mode=mode,status=status)

        db.session.add(entry)
        borrower = Tblborrow.query.filter_by(id=request.form.get('id')).first()
        borrower.borrow_amount = request.form.get('borrow_amount')
        borrower.repay_amount = request.form.get('repay_amount')
        borrower.balance = request.form.get('balance')
        borrower.balance = float(borrower.balance) - float(borrower.repay_amount)
        db.session.commit()
        flash("Transaction added successfully !!!")
        return redirect("/repay")


@app.route("/repay/detail/<string:trans_no>")
def repaydetail(trans_no):
    repaydetail = Tblrepay.query.filter_by(trans_no=trans_no).order_by(Tblrepay.date).all()
    return render_template("repaydetail.html",repaydetail=repaydetail)

#repay update

@app.route("/detail/update",methods=['GET','POST'])
def updatedetail():
    if request.method == 'POST':
        repay = Tblrepay.query.filter_by(id=request.form.get("id")).first()
        trans_no=str(repay.trans_no)
        repay.description = request.form.get("description")
        repay.repay_amount = request.form.get("repay_amount")
        repay.date =request.form.get("date")
        db.session.commit()

        borrower = Tblborrow.query.filter_by(trans_no=repay.trans_no).first()
        repaydetail = Tblrepay.query.filter_by(trans_no=repay.trans_no).all()
        repay_amount = 0
        for r in repaydetail:
            if r is not None:
                repay_amount = repay_amount + float(r.repay_amount)
                borrower.repay_amount = r.repay_amount
            else:
                borrower.repay_amount = 0.00
        borrower.balance = float(repay.borrow_amount) - float(repay_amount)

        for r in range(len(repaydetail)):
            if repaydetail[r] is not None:
                if r == 0:
                    repaydetail[r].balance = float(repaydetail[r].borrow_amount) - float(repaydetail[r].repay_amount)
                else:
                    repaydetail[r].balance = float(repaydetail[r - 1].balance) - float(repaydetail[r].repay_amount)
        db.session.commit()
        flash("Repay transaction updated successfully !!!")
        return redirect("/repay/detail/"+ trans_no)


#repay delete
@app.route("/delete/repay/<string:id>", methods=['GET','POST'])
def deleterepay(id):

    repay = Tblrepay.query.filter_by(id=id).first()
    trans_no = str(repay.trans_no)
    db.session.delete(repay)
    repaydetail = Tblrepay.query.filter_by(trans_no=repay.trans_no).order_by(Tblrepay.date).all()
    borrower = Tblborrow.query.filter_by(trans_no=repay.trans_no).first()
    repay_amount=0
    for r in repaydetail:
        if r is not None:
            repay_amount=repay_amount+float(r.repay_amount)
            borrower.repay_amount = r.repay_amount
        else:
            borrower.repay_amount = 0.00
    borrower.balance = float(repay.borrow_amount)-float(repay_amount)

    for r in range(len(repaydetail)):
        if repaydetail[r] is not None:
            if r==0:
                repaydetail[r].balance = float(repaydetail[r].borrow_amount)-float(repaydetail[r].repay_amount)
            else:
                repaydetail[r].balance = float(repaydetail[r-1].balance)-float(repaydetail[r].repay_amount)

    db.session.commit()
    flash("Repay transaction deleted successfully !!!")
    return redirect("/repay/detail/"+trans_no)


#borrow_lending add to cash balance
@app.route("/borrow/addtocash/<string:id>")
def borrowaddtocash(id):
    borrow = Tblborrow.query.filter_by(id=id).first()
    borrow.status = "add"
    db.session.commit()
    flash("Amount added successfully to cash balance")
    return redirect("/borrow_lending")

#borrow_lending subtract from cash balance
@app.route("/borrow/subtracttocash/<string:id>")
def borrowsubtractfromcash(id):
    borrow = Tblborrow.query.filter_by(id=id).first()
    borrow.status = "subtract"
    db.session.commit()
    flash("Amount subtract successfully from cash balance")
    return redirect("/borrow_lending")

#repay add to cash balance
@app.route("/repay/addtocash/<string:id>")
def repayaddtocash(id):
    repay = Tblrepay.query.filter_by(id=id).first()
    trans_no = str(repay.trans_no)
    repay.status = "add"
    db.session.commit()
    flash("Amount added successfully to cash balance")
    return redirect("/repay/detail/"+trans_no)

#repay subtract from cash balance
@app.route("/repay/subtracttocash/<string:id>")
def repaysubtractfromcash(id):
    repay = Tblrepay.query.filter_by(id=id).first()
    trans_no = str(repay.trans_no)
    repay.status = "subtract"
    db.session.commit()
    flash("Amount subtract successfully from cash balance")
    return redirect("/repay/detail/"+trans_no)




if __name__ =="__main__":
    app.run(debug=True)