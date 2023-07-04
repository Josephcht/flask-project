import sys

from flask import Flask, render_template,request,redirect,url_for, flash, session
from Forms import CreateUserForm, LoginForm, DeleteForm, ChangePINForm, UpdateForm, ForgetPIN, LockCardForm, CreateRecipientForm, testform,transferform, ReportForm,UpdateCardType, UnlockCardForm
import shelve,User,Feedback,datetime
app = Flask(__name__)
app.secret_key = 'any_random_string'



def logins():
    try:
        login_dict = {}
        db = shelve.open('login.db', 'c')
        login_dict = db['Login']
        db.close()
        login = login_dict.get(1)
        print(login.get_logged_in())
        return login.get_logged_in()
    except:
        print('Error')

def admin():
    try:
        login_dict = {}
        db = shelve.open('login.db', 'c')
        login_dict = db['Login']
        db.close()
        login = login_dict.get(1)
        if login.get_username() == 'Admin' and login.get_PIN() == '123456':
            admin = True
        else:
            admin = False
        return admin
    except:
        print('Error')


@app.route('/')
def home():
    return render_template('home.html', login = logins(), admin=admin())
@app.route('/mainHome')
def mainHome():
    return render_template('mainHome.html',login = logins(), admin=admin())

@app.route('/base')
def base():
    login_dict = {}
    db = shelve.open('login.db', 'c')
    login_dict = db['Login']
    db.close()
    login = login_dict.get(1)
    return render_template('base.html', login=login.get_logged_in(),admin=admin())


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    error = None
    userid=1

    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        if users_dict == {}:
            user = User.User(create_user_form.first_name.data.capitalize(), create_user_form.last_name.data.capitalize(),
                             create_user_form.gender.data, create_user_form.identity_no.data,
                             create_user_form.identity_type.data, create_user_form.date_of_birth.data,create_user_form.age.data,
                             create_user_form.address.data, create_user_form.phone_no.data, create_user_form.email.data,
                             create_user_form.username.data,
                             create_user_form.PIN.data,create_user_form.region.data,create_user_form.card_type.data)
            for id in users_dict:
                if id >= userid:
                    userid = id
                    userid += 1
            user.set_user_id(userid)
            users_dict[user.get_user_id()] = user

            db['Users'] = users_dict
            db.close()
            return redirect(url_for('login'))
        else:

            users_list = []
            for key in users_dict:
                user = users_dict.get(key)
                users_list.append(user)
            for user in users_list:
                if user.get_username() != create_user_form.username.data:
                    user = User.User(create_user_form.first_name.data.capitalize(), create_user_form.last_name.data.capitalize(),
                                     create_user_form.gender.data, create_user_form.identity_no.data, create_user_form.identity_type.data,create_user_form.date_of_birth.data, create_user_form.age.data,
                                     create_user_form.address.data,create_user_form.phone_no.data,create_user_form.email.data,create_user_form.username.data,
                                     create_user_form.PIN.data,create_user_form.region.data,create_user_form.card_type.data)
                    for id in users_dict:
                        if id >= userid:
                            userid = id
                            userid+=1
                    user.set_user_id(userid)
                    users_dict[user.get_user_id()] = user

                    db['Users'] = users_dict
                    db.close()
                    return redirect(url_for('login'))
                else:
                    error = 'Username already taken'
    return render_template('createUser.html', form=create_user_form, error = error)

@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('storage.db', 'c')
    users_dict = db['Users']
    db.close()
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
    login_dict = {}
    login_db = shelve.open('login.db','c')
    login_dict = login_db['Login']
    login_db.close()
    login = login_dict.get(1)
    if login.get_username() == 'Admin' and login.get_PIN() == '123456':
        return render_template('retrieveUsers.html', count=len(users_list), user_list=users_list, login=logins(),
                               admin=True)
    elif login.get_username() != 'Admin' and login.get_PIN() != '123456':
        for user in users_list:
            if user.get_username() == login.get_username() and user.get_PIN() == login.get_PIN():
                return render_template('retrieveUsers.html', count=len(users_list), user=user, login=logins(),
                                       admin=False)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')
        users_dict = db['Users']
        db.close()
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        for user in users_list:
            if user.get_username() == login_form.username.data and user.get_PIN() == login_form.PIN.data:
                login_dict = {}
                db = shelve.open('login.db','c')
                try:
                    login_dict = db['Login']
                except:
                    print("Error in retrieving Users from storage.db.")
                id = user.get_user_id()
                login = User.Login(login_form.username.data,login_form.PIN.data,id)
                login.set_logged_in(True)
                login_dict[login.get_id()] = login
                db['Login'] = login_dict

                db.close()
                return redirect(url_for('mainHome'))
            elif login_form.username.data == 'Admin' and login_form.PIN.data == '123456':
                login_dict = {}
                db = shelve.open('login.db', 'c')
                try:
                    login_dict = db['Login']
                except:
                    print("Error in retrieving Users from storage.db.")
                id = user.get_user_id()
                login = User.Login(login_form.username.data, login_form.PIN.data, id)
                login.set_logged_in(True)
                login_dict[login.get_id()] = login
                db['Login'] = login_dict

                db.close()
                return redirect(url_for('mainHome'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error, form=login_form, admin=admin())


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = UpdateForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        login_db = shelve.open('login.db','w')
        login_dict = login_db['Login']
        login = login_dict.get(1)
        if login.get_username() != 'Admin' and login.get_PIN() != '123456':
            login.set_username(update_user_form.username.data)

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data.capitalize())
        user.set_last_name(update_user_form.last_name.data.capitalize())
        user.set_identity_type(update_user_form.identity_type.data)
        user.set_identity_no(update_user_form.identity_no.data)
        user.set_date_of_birth(update_user_form.date_of_birth.data)
        user.set_address(update_user_form.address.data)
        user.set_region(update_user_form.region.data)
        user.set_phone_no(update_user_form.phone_no.data)
        user.set_email(update_user_form.email.data)
        user.set_username(update_user_form.username.data)

        users_list = []
        for key in users_dict:
            urecipient = users_dict.get(key)
            users_list.append(urecipient)

        for u in users_list:
            urlist = u.get_recipients()
            for recipient in urlist:
                if user.get_user_id() == recipient.get_user_id():
                    recipient.set_first_name(update_user_form.first_name.data.capitalize())
                    recipient.set_last_name(update_user_form.last_name.data.capitalize())
                    recipient.set_phone(update_user_form.phone_no.data)
                    recipient.set_email(update_user_form.email.data)

        login_db['Login'] = login_dict
        db['Users'] = users_dict
        db.close()
        login_db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('storage.db','r')
        users_dict = db['Users']
        db.close()
        user=users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.identity_type.data = user.get_identity_type()
        update_user_form.identity_no.data = user.get_identity_no()
        update_user_form.date_of_birth.data = user.get_date_of_birth()
        update_user_form.address.data = user.get_address()
        update_user_form.region.data = user.get_region()
        update_user_form.phone_no.data = user.get_phone_no()
        update_user_form.email.data = user.get_email()
        update_user_form.username.data = user.get_username()
        return render_template('updateUser.html', form=update_user_form,login = logins(), admin=admin())

@app.route('/deleteAccount', methods=['GET', 'POST'])
def Delete():
    error = None
    delete_form = DeleteForm(request.form)
    if request.method == 'POST' and delete_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        for user in users_list:
            if user.get_username() == delete_form.username.data and user.get_PIN() == delete_form.PIN.data:
                id = user.get_user_id()
                users_dict.pop(id)
                db['Users'] = users_dict
                db.close()
                login_dict = {}
                login_db = shelve.open('login.db', 'c')
                login_dict = login_db['Login']
                login = login_dict.get(1)
                login.set_logged_in(False)
                login_db['Login'] = login_dict
                login_db.close()
                return redirect(url_for('home'))
        else:
            error = 'Wrong Password or Username. Please try again.'

    return render_template('deleteAccount.html', error=error, form=delete_form, login = logins())

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))

@app.route('/lockCard',methods=['GET', 'POST'])
def lockCard():
    error = None
    lock_card_form = LockCardForm(request.form)
    if request.method == 'POST' and lock_card_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        for user in users_list:
            if user.get_username() == lock_card_form.username.data and user.get_PIN() == lock_card_form.PIN.data:
                user.set_active(False)
                db['Users'] = users_dict
                db.close()
                return redirect(url_for('mainHome'))
        else:
            error = 'Wrong Password or Username. Please try again.'

    return render_template('lockCard.html', error=error, form=lock_card_form, login=logins(),admin=admin())
@app.route('/changePIN',methods=['GET', 'POST'])
def changePIN():
    error = None
    change_PIN_form = ChangePINForm(request.form)
    if request.method == 'POST' and change_PIN_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        for user in users_list:
            if user.get_PIN() == change_PIN_form.initial.data and user.get_username() == change_PIN_form.username.data:
                login_db = shelve.open('login.db', 'w')
                login_dict = login_db['Login']
                login = login_dict.get(1)
                login.set_PIN(change_PIN_form.PIN.data)
                login_db['Login'] = login_dict
                id = user.get_user_id()
                users = users_dict.get(id)
                users.set_PIN(change_PIN_form.PIN.data)
                db['Users'] = users_dict
                db.close()
                login_db.close()
                return redirect(url_for('mainHome'))
        else:
            error = 'Wrong PIN. Please try again.'
    return render_template('changePIN.html',error = error,form=change_PIN_form,login = logins())

@app.route('/forgetPass',methods=['GET', 'POST'])
def forgetPIN():
    error = None
    forget_PIN_form = ForgetPIN(request.form)
    if request.method == 'POST' and forget_PIN_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        for user in users_list:
            if user.get_username() == forget_PIN_form.username.data and user.get_date_of_birth() == forget_PIN_form.date_of_birth.data and user.get_identity_no() == forget_PIN_form.identity_no.data:
                login_db = shelve.open('login.db', 'w')
                login_dict = login_db['Login']
                login = login_dict.get(1)
                login.set_PIN(forget_PIN_form.PIN.data)
                login_db['Login'] = login_dict
                id = user.get_user_id()
                users = users_dict.get(id)
                users.set_PIN(forget_PIN_form.PIN.data)
                db['Users'] = users_dict
                db.close()
                login_db.close()
                return redirect(url_for('home'))
        else:
            error = 'Wrong particulars. Please try again.'
    return render_template('forgetPass.html',error = error,form=forget_PIN_form,login = logins())

@app.route('/logout')
def logout():
    login_dict = {}
    db = shelve.open('login.db', 'c')
    login_dict = db['Login']
    login = login_dict.get(1)
    login.set_logged_in(False)
    db['Login'] = login_dict
    db.close()
    return redirect(url_for('home'))





































@app.route('/add_recipient', methods=['GET', 'POST'])
def add_recipient():
    create_user_form = CreateRecipientForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','w')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")


        db.close()
        recipients = User.recipient(create_user_form.first_name.data.capitalize(), create_user_form.last_name.data.capitalize(), create_user_form.gender.data, create_user_form.email.data, create_user_form.phone.data, create_user_form.remarks.data)
        login = login_dict.get(1)
        curruser = login.get_user_id()
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

        for user in users_list:
            user.check_if_recipient(recipients)
            if user.get_user_id() == curruser:
                user.add_recipients(recipients)
        if recipients.get_user_id() == None:
            session['not_added'] = "User does not exist"
        else:
            session['Recipient_Added'] = recipients.get_first_name() + ' ' + recipients.get_last_name()
            db2['Users'] = users_dict
            db2.close()

        return redirect(url_for('recipient_list'))
    return render_template('add_recipient.html', form=create_user_form, login=logins())



@app.route('/recipient_list')
def recipient_list():
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','w')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        db.close()
        login = login_dict.get(1)
        curruser = login.get_user_id()
        user = users_dict.get(curruser)
        recipients = user.get_recipients()
        db2['Users'] = users_dict
        db2.close()

        return render_template('recipient_list.html', count=len(recipients), users_list=recipients, login=logins())

@app.route('/update_recipient/<int:id>/', methods=['GET', 'POST'])
def update_recipient(id):
    update_user_form = CreateRecipientForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','w')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")


        db.close()
        login = login_dict.get(1)
        curruser = login.get_user_id()
        user = users_dict.get(curruser)
        recipients = user.get_recipients()
        for i in recipients:
            if i.get_user_id() == id:
                reci = i
                session['user_updated'] = reci.get_first_name() + ' ' + reci.get_last_name()
                reci.set_remarks(update_user_form.remarks.data)

        db2['Users'] = users_dict
        db2.close()



        return redirect(url_for('recipient_list'))
    else:
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','w')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        db.close()
        db2.close()
        login = login_dict.get(1)
        curruser = login.get_user_id()
        user = users_dict.get(curruser)
        recipients = user.get_recipients()
        for i in recipients:
            if i.get_user_id() == id:
                reci = i
                update_user_form.first_name.data = reci.get_first_name()
                update_user_form.last_name.data = reci.get_last_name()
                update_user_form.gender.data = reci.get_gender()
                update_user_form.email.data = reci.get_email()
                update_user_form.phone.data = reci.get_phone()
                update_user_form.remarks.data = reci.get_remarks()

        return render_template('update_recipient.html', form=update_user_form, login=logins())

@app.route('/delete_recipient/<int:id>', methods=['GET','POST'])
def delete_recipient(id):
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','w')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")


        db.close()
        login = login_dict.get(1)
        curruser = login.get_user_id()

        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        for user in users_list:
            if user.get_user_id() == curruser:
                recipient = user.get_recipients()
                for i in recipient:
                    if i.get_user_id() == id:
                         reci = i
                         session['user_deleted'] = reci.get_first_name() + ' ' + reci.get_last_name()
                         recipient.remove(i)

        db2['Users'] = users_dict
        db2.close()
        return redirect(url_for('recipient_list'))

@app.route('/balancem', methods=['POST','GET'])
def balancem():
    #testing before integration
    balance_form = testform(request.form)
    if request.method == "POST" and balance_form.validate():
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','w')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        db.close()
        login = login_dict.get(1)
        curruserid = login.get_user_id()
        curruser = users_dict.get(curruserid)

        deposit = User.Deposit(balance_form.balance.data,curruserid,curruserid)
        deposit.addbalance(curruser)
        deposit.set_time(datetime.datetime.today().strftime('%Y-%m-%d'))
        curruser.add_transactions(deposit)
        db2['Users'] = users_dict
        db2.close()

        return redirect(url_for('balancem'))

    else:
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','r')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")


        db.close()
        db2.close()
        login = login_dict.get(1)
        curruserid = login.get_user_id()
        curruser = users_dict.get(curruserid)






    return render_template('balancem.html', form=balance_form, user=curruser, login=logins(),transaction_list=curruser.get_transactions())

@app.route("/transfer", methods=['GET','POST'])
def transfer():
        transfer = transferform(request.form)
        confirmation = CreateRecipientForm(request.form)


        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','r')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")


        db.close()
        login = login_dict.get(1)
        curruserid = login.get_user_id()
        curruser = users_dict.get(curruserid)
        users_list = []
        rrlist=[]
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

        for user in users_list:
            if user.get_user_id() == curruserid:
                recipients = user.get_recipients()
                for i in recipients:
                  a = i.get_user_id()
                  b = i.get_first_name() + i.get_last_name()
                  rrlist.append((a,b))

        transfer.recipient.choices = rrlist
        test = curruser.get_balance()
        transfer.amount.max = test
        print("rrlist =",rrlist)


        if request.method == "POST" and transfer.validate():
            users_dict = {}
            login_dict = {}
            transfer_dict = {}
            db = shelve.open('login.db', 'r')
            db2 = shelve.open('storage.db','w')
            db3 = shelve.open('transferstorage.db','c')

            try:
                login_dict = db['Login']

            except:
                print("Error in retrieving Users from login.db.")

            try:
                users_dict = db2['Users']
            except:
                print("Error in retrieving Users from storage.db.")
            try:
                transfer_dict = db3['Transfer']
            except:
                print("Error in retirieving Transaction from transferstorage.db.")


            db.close()
            login = login_dict.get(1)
            curruserid = login.get_user_id()
            curruser = users_dict.get(curruserid)


            rlist = []
            for i in curruser.get_recipients():
                rlist.append(i.get_user_id())


            transfer.sender_id = curruserid

            transac = User.Transfer(transfer.amount.data, transfer.sender_id, transfer.recipient.data)
            recipients = curruser.get_recipients()
            for i in recipients:
                if i.get_user_id() == transac.get_recipient_id():
                    reci = i
                    confirmation.first_name.data = reci.get_first_name()
                    confirmation.last_name.data = reci.get_last_name()
                    confirmation.gender.data = reci.get_gender()
                    confirmation.email.data = reci.get_email()
                    confirmation.phone.data = reci.get_phone()
                    confirmation.remarks.data = reci.get_remarks()
            transfer_dict[curruserid] = transac
            db3['Transfer'] = transfer_dict
            db3.close()
            transfervalid = True
        else:
            transfervalid = False




        return render_template("transfer.html", form=confirmation, transfer_form=transfer, login=logins(),transfervalid=transfervalid)

@app.route("/tvalidate", methods=['POST','GET'])
def tvalidate():
        validf = LoginForm(request.form)
        if request.method == "POST":
            login_dict = {}

            db = shelve.open('login.db', 'r')
            try:
                login_dict = db['Login']

            except:
                print("Error in retrieving Users from login.db.")

            login = login_dict.get(1)
            if login.get_username() == validf.username.data and login.get_PIN() == validf.PIN.data:
                return redirect(url_for('transfer'))



            else:
                session['unveri'] = "Incorrect Credentials"

        return render_template("tvalidate.html",login=logins(),form=validf)

@app.route("/tconfirm", methods=['GET','POST'])
def tconfirm():
        transfer = transferform(request.form)
        validf = LoginForm(request.form)
        confirmation = CreateRecipientForm(request.form)


        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db','r')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")


        db.close()
        login = login_dict.get(1)
        curruserid = login.get_user_id()
        curruser = users_dict.get(curruserid)
        users_list = []
        rrlist=[]
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

        for user in users_list:
            if user.get_user_id() == curruserid:
                recipients = user.get_recipients()
                for i in recipients:
                  a = i.get_user_id()
                  b = i.get_first_name() + i.get_last_name()
                  rrlist.append((a,b))

        transfer.recipient.choices = rrlist
        test = curruser.get_balance()
        transfer.amount.max = test
        valid = False


        if request.method == "POST" and confirmation.validate():
            users_dict = {}
            login_dict = {}
            transfer_dict = {}
            db = shelve.open('login.db', 'r')
            db2 = shelve.open('storage.db','w')
            db3 = shelve.open('transferstorage.db','r')

            try:
                login_dict = db['Login']

            except:
                print("Error in retrieving Users from login.db.")

            try:
                users_dict = db2['Users']
            except:
                print("Error in retrieving Users from storage.db.")
            try:
                transfer_dict = db3['Transfer']
            except:
                print("Error in retrieving Users from tranferstorage.db.")


            db.close()
            db3.close()
            login = login_dict.get(1)
            curruserid = login.get_user_id()
            curruser = users_dict.get(curruserid)
            recipients = curruser.get_recipients()
            transac = transfer_dict.get(curruserid)
            for i in recipients:
                if i.get_user_id() == transac.get_recipient_id():
                    reci = i
                    confirmation.first_name.data = reci.get_first_name()
                    confirmation.last_name.data = reci.get_last_name()
                    confirmation.gender.data = reci.get_gender()
                    confirmation.email.data = reci.get_email()
                    confirmation.phone.data = reci.get_phone()
                    confirmation.remarks.data = reci.get_remarks()

            rlist = []
            for i in curruser.get_recipients():
                rlist.append(i.get_user_id())
            transac.deductsender(curruser)
            transac.addreceive(rlist,users_dict)
            transac.set_time(datetime.datetime.today().strftime('%Y-%m-%d'))
            curruser.add_transactions(transac)
            receipt = users_dict.get(transac.get_recipient_id())
            receipt.add_transactions(transac)
            db2['Users'] = users_dict
            db2.close()
            transfervalid = True

            session['transferred'] = '$'+str(transac.get_amount())+ ' has been transferred to ' + receipt.get_first_name() + receipt.get_last_name()
        else:
            transfervalid = False




        return render_template("transfer.html", form=confirmation,transfer_form=transfer, login=logins(),validf_form=validf,valid=valid,transfervalid=transfervalid)


@app.route('/dashboard')
def dashboard():
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()
#ACCOUNT MANAGEMENT =======================================================================================================>
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

# CUSTOMER SUPPORT ==================================================================>
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedbacks_dict = db['Feedback']
    db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        user = feedbacks_dict.get(key)
        feedbacks_list.append(user)

    #TRANSACTION PROCESSING ==================================================================================================>
    balance_form = testform(request.form)
    if request.method == "POST" and balance_form.validate():
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db', 'w')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        db.close()
        login = login_dict.get(1)
        curruserid = login.get_user_id()
        curruser = users_dict.get(curruserid)

        deposit = User.Deposit(balance_form.balance.data, curruserid, curruserid)
        deposit.addbalance(curruser)
        curruser.add_transactions(deposit)
        db2['Users'] = users_dict
        db2.close()

        return redirect(url_for('balancem'))

    else:
        users_dict = {}
        login_dict = {}
        db = shelve.open('login.db', 'r')
        db2 = shelve.open('storage.db', 'r')

        try:
            login_dict = db['Login']

        except:
            print("Error in retrieving Users from login.db.")

        try:
            users_dict = db2['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        db.close()
        db2.close()
        login = login_dict.get(1)
        curruserid = login.get_user_id()
        curruser = users_dict.get(curruserid)


    overall_transaction_list = curruser.get_transactions()



# DASHBOARD TEST =============================================================>
    user_age = []
    # 2) storing the lenght of total age data inputted
    age_data = []
    # 3 looping the user in the database list
    for user in users_list:
        # 4 appending the age to the user_age list
        user_age.append(user.get_age())
        # 5 appending the length data of the list to the new list as data
        new_age = len(user_age)

    age_data.append(new_age)

##DASHBOARD 1 =============================================================>

    teen = []
    graduate = []
    working = []
    experienced = []
    retirement = []
    elderly = []

    teen_data = []
    graduate_data = []
    working_data = []
    experienced_data = []
    retirement_data = []
    elderly_data = []

    for user in users_list:
        if user.get_age() >= 18 and user.get_age() <= 25:
            teen.append(user.get_age())
        elif user.get_age() >= 26 and user.get_age() <= 35:
            graduate.append(user.get_age())
        elif user.get_age() >= 36 and user.get_age() <= 45:
            working.append(user.get_age())
        elif user.get_age() >= 46 and user.get_age() <= 55:
            experienced.append(user.get_age())
        elif user.get_age() >= 56 and user.get_age() <= 65:
            retirement.append(user.get_age())
        elif user.get_age() > 65:
            elderly.append(user.get_age())
        else:
            break

        count_teen = len(teen)
        count_graduate = len(graduate)
        count_working = len(working)
        count_experienced = len(experienced)
        count_retirement = len(retirement)
        count_elderly = len(elderly)

    teen_data.append(count_teen)
    graduate_data.append(count_graduate)
    working_data.append(count_working)
    experienced_data.append(count_experienced)
    retirement_data.append(count_retirement)
    elderly_data.append(count_elderly)

    ##DASHBOARD 2 =============================================================>

    north_list = []
    south_list = []
    east_list = []
    west_list = []

    north = []
    south = []
    east = []
    west = []

    for user in users_list:
        if user.get_region() == 'N':
            north_list.append(user.get_region())
        elif user.get_region() == 'S':
            south_list.append(user.get_region())
        elif user.get_region() == 'E':
            east_list.append(user.get_region())
        elif user.get_region() == 'W':
            west_list.append(user.get_region())
        else:
            break

        count_north = len(north_list)
        count_south = len(south_list)
        count_east = len(east_list)
        count_west = len(west_list)

    north.append(count_north)
    south.append(count_south)
    east.append(count_east)
    west.append(count_west)

##DASHBOARD 3 =============================================================>

    debit_list = []
    credit_list = []
    prepaid_list = []
    forex_list = []

    debit = []
    credit = []
    prepaid = []
    forex = []

    for user in users_list:
        if user.get_card_type() == 'D':
            debit_list.append(user.get_card_type())
        elif user.get_card_type() == 'C':
            credit_list.append(user.get_card_type())
        elif user.get_card_type() == 'F':
            forex_list.append(user.get_card_type())
        elif user.get_card_type() == 'P':
            prepaid_list.append(user.get_card_type())
        else:
            break

        count_debit = len(debit_list)
        count_credit = len(credit_list)
        count_forex = len(forex_list)
        count_prepaid = len(prepaid_list)

    debit.append(count_debit)
    credit.append(count_credit)
    prepaid.append(count_prepaid)
    forex.append(count_forex)

    ##DASHBOARD 4 =============================================================>

    singaporean_list  = []
    malaysian_list = []
    passport_list = []

    singaporean = []
    malaysian = []
    passport = []




    for user in users_list:
        if user.get_identity_type() == 'N':
            singaporean_list.append(user.get_identity_type())
        elif user.get_identity_type() == 'M':
            malaysian_list.append(user.get_identity_type())
        elif user.get_identity_type() == 'P':
            passport_list.append(user.get_identity_type())
        else:
            break

        count_singaporean = len(singaporean_list)
        count_malaysian = len(malaysian_list)
        count_passport = len(passport_list)

    singaporean.append(count_singaporean)
    malaysian.append(count_malaysian)
    passport.append(count_passport)

    ##DASHBOARD 5 =============================================================> [ ERROR ]

    total_transaction_list = []
    transactions_data = []

    for user in overall_transaction_list:
        total_transaction_list.append(user.get_transact_id())
        transactions_count = len(total_transaction_list)

    transactions_data.append(transactions_count)



##DASHBOARD 6 =============================================================> [ ERROR ]

    transfer_list = []
    deposit_list = []
    withdraw_list = []

    transfer = []
    deposit = []
    withdraw = []

    for user in overall_transaction_list:
        if user.get_type() == 'D':
            deposit_list.append(user.get_type())
        elif user.get_type() == 'W':
            withdraw_list.append(user.get_type())
        elif user.get_type() == 'T':
            transfer_list.append(user.get_type())
        else:
            break

        count_deposit = len(deposit_list)
        count_withdraw = len(withdraw_list)
        count_transfer = len(transfer_list)

    deposit.append(count_deposit)
    withdraw.append(count_withdraw)
    transfer.append(count_transfer)

##DASHBOARD 8 =============================================================> [ ERROR ]

    reason_1_list = []
    reason_2_list = []
    reason_3_list = []
    reason_4_list = []
    reason_5_list = []

    reason_1 = []
    reason_2 = []
    reason_3 = []
    reason_4 = []
    reason_5 = []


    for feedback in feedbacks_list:
        if feedback.get_reason() == '1':
            reason_1_list.append(feedback.get_reason())
        elif feedback.get_reason() == '2':
            reason_2_list.append(feedback.get_reason())
        elif feedback.get_reason() == '3':
            reason_3_list.append(feedback.get_reason())
        elif feedback.get_reason() == '4':
            reason_4_list.append(feedback.get_reason())
        elif feedback.get_reason() == '5':
            reason_5_list.append(feedback.get_reason())

        else:
            break

        count_reason_1 = len(reason_1_list)
        count_reason_2 = len(reason_2_list)
        count_reason_3 = len(reason_3_list)
        count_reason_4 = len(reason_4_list)
        count_reason_5 = len(reason_5_list)


    reason_1.append(count_reason_1)
    reason_2.append(count_reason_2)
    reason_3.append(count_reason_3)
    reason_4.append(count_reason_4)
    reason_5.append(count_reason_5)

##DASHBOARD 9 =============================================================> [ ERROR ]
    rating_1_list = []
    rating_2_list = []
    rating_3_list = []
    rating_4_list = []
    rating_5_list = []

    rating_1 = []
    rating_2 = []
    rating_3 = []
    rating_4 = []
    rating_5 = []


    for feedback in feedbacks_list:
        if feedback.get_rating() == '1':
            rating_1_list.append(feedback.get_rating())
        elif feedback.get_rating() == '2':
            rating_2_list.append(feedback.get_rating())
        elif feedback.get_rating() == '3':
            rating_3_list.append(feedback.get_rating())
        elif feedback.get_rating() == '4':
            rating_4_list.append(feedback.get_rating())
        elif feedback.get_rating() == '5':
            rating_5_list.append(feedback.get_rating())
        else:
            break

        count_rating_1 = len(rating_1_list)
        count_rating_2 = len(rating_2_list)
        count_rating_3 = len(rating_3_list)
        count_rating_4 = len(rating_4_list)
        count_rating_5 = len(rating_5_list)


    rating_1.append(count_rating_1)
    rating_2.append(count_rating_2)
    rating_3.append(count_rating_3)
    rating_4.append(count_rating_4)
    rating_5.append(count_rating_5)







    #TEST DATA AND LABEL
    values = [12, 19, 3, 5, 2, 3]
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']


    #LABELS
    labelAge = ['18-25', '26-35', '35-45', '46-55', '56-65', '>65']
    labelRegion = ['North', 'South', 'East', 'West']
    labelCard = ['Debit', 'Credit','Prepaid', 'Forex']
    labelNationality = ['Singaporean', 'Malaysian', 'Passport']
    labelYear = ['2020', '2021', '2022']
    labelTransactions = ['Deposit', 'Withdrawal', 'Transfer']
    labelEnquiries = ['Loans','Fees','E-service', 'Customer Service', 'Others']
    labelRatings = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']

    #DATA
    onlineTransactions1 = ['2']
    onlineTransactions2 = ['10']
    physicalTransaction = ['30', '20', '10']
    transactionTypes = ['100', '200', '300', '150']
    customerEnquiries = ['100','200','300','400','500']
    starRatings = ['500','400','300','200','100']



    return render_template('report.html'
                           #Test Data:
                           ,age = age_data, labels = labels, values = values
                           #DASHBOARD 1 VALUES
                           ,teen = teen_data, graduate = graduate_data, working = working_data, experienced = experienced_data, retirement = retirement_data, elderly = elderly_data
                           ,labelAge = labelAge
                           #DASHBOARD 2 VALUES
                           , north=north, south=south, east=east, west=west
                           , labelRegion=labelRegion
                           # DASHBOARD 3 VALUES
                           ,debit = debit, credit = credit, prepaid = prepaid, forex = forex
                           ,labelCard=labelCard
                           # DASHBOARD 4 VALUES
                           ,singaporean = singaporean, malaysian = malaysian, passport = passport
                           ,labelNationality = labelNationality
                           # DASHBOARD 5 VALUES
                           , transactions_data = transactions_data,onlineTransactions1 = onlineTransactions1, onlineTransactions2 = onlineTransactions2
                           , labelYear = labelYear, physicalTransaction = physicalTransaction
                           # DASHBOARD 6 VALUES
                           ,transactionTypes = transactionTypes, deposit = deposit, withdraw = withdraw, transfer = transfer
                           ,labelTransactions = labelTransactions
                           # DASHBOARD 8 VALUES
                           # ,reason_1 = reason_1, reason_2 = reason_2, reason_3 = reason_3, reason_4 = reason_4, reason_5 = reason_5
                           ,labelEnquiries = labelEnquiries, customerEnquiries = customerEnquiries
                           , reason_1=reason_1, reason_2=reason_2, reason_3=reason_3, reason_4=reason_4,
                           reason_5=reason_5

                           # DASHBOARD 9 VALUES
                           # ,rating_1 = rating_1, rating_2 = rating_2, rating_3 = rating_3, rating_4 = rating_4, rating_5 = rating_5
                            ,labelRatings = labelRatings, starRatings = starRatings
                           , rating_1=rating_1, rating_2=rating_2, rating_3=rating_3, rating_4=rating_4,
                           rating_5=rating_5

                           #LISTS
                           ,count = len(users_list), user_list = users_list,overall_transaction_list = overall_transaction_list, feedback_list = feedbacks_list
                           )
@app.route('/staff_updateUser/<int:id>/', methods=['GET', 'POST'])
def staff_update_user(id):
    staff_update_user_form = UpdateCardType(request.form)
    if request.method == 'POST' and staff_update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_card_type(staff_update_user_form.card_type.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('dashboard'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        staff_update_user_form.card_type.data = user.get_card_type()



        return render_template('staff_updateUser.html', form= staff_update_user_form,login=logins(),admin=admin())



@app.route('/help')
def Help():
    return render_template('help.html',login=logins(),admin=admin())

@app.route('/Report_Feedback', methods=['GET', 'POST'])
def report_feedback():
    report_feedback_form = ReportForm(request.form)
    if request.method == 'POST' and report_feedback_form.validate():
        feedbacks_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedbacks_dict = db['Feedback']
        except:
            print("Error in retrieving Feedbacks from storage.db.")

        feedback = Feedback.Feedback(report_feedback_form.first_name.data, report_feedback_form.last_name.data, report_feedback_form.email.data,report_feedback_form.reason.data,report_feedback_form.report.data, report_feedback_form.rating.data, report_feedback_form.feedback.data)
        feedbacks_dict[feedback.get_Feedback_id()] = feedback
        db['Feedback'] = feedbacks_dict

        db.close()

        return redirect(url_for('home'))
    return render_template('Report_Feedback.html', form=report_feedback_form,login=logins(),admin=admin())

@app.route('/retrieve_Feedbacks')
def retrieve_feedback():
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedbacks_dict = db['Feedback']
    db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        user = feedbacks_dict.get(key)
        feedbacks_list.append(user)



    return render_template('retrieve_Feedbacks.html',count=len(feedbacks_list), feedbacks_list=feedbacks_list,login=logins(),admin=admin())

@app.route('/deleteFeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedbacks_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedbacks_dict = db['Feedback']

    feedbacks_dict.pop(id)

    db['Feedback'] = feedbacks_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))


@app.route('/unlockCard',methods=['GET', 'POST'])
def unlockCard():
    error = None
    unlock_card_form = UnlockCardForm(request.form)
    if request.method == 'POST' and unlock_card_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        for user in users_list:
            if user.get_username() == unlock_card_form.username.data and user.get_identity_no() == unlock_card_form.identity_no.data:
                user.set_active(True)
                db['Users'] = users_dict
                db.close()
                return redirect(url_for('mainHome'))
        else:
            error = 'Wrong Password or Username. Please try again.'

    return render_template('unlockCard.html', error=error, form=unlock_card_form, login=logins(), admin=admin())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

if __name__== '__main__':
    try:
        db = shelve.open('login.db', 'c')
        login_dict = db['Login']
        login = login_dict.get(1)
        login.set_logged_in(False)
        db['Login'] = login_dict
        db.close()
    except:
        print("Error")
    finally:
        app.run()
