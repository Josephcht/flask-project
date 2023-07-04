import random
def generate_cid(length=16):
    cid =""
    for i in range(length):
        cid+=str(random.randint(0,9))
    return cid
class User:
    def __init__(self,first_name,last_name,gender,identity_no,identity_type,date_of_birth,age,address,phone_no,email,username,PIN,region,card_type):
        self.user_id = 0
        self.first_name = first_name
        self.last_name = last_name
        self.identity_type = identity_type
        self.gender = gender
        self.identity_no = identity_no
        self.address = address
        self.date_of_birth = date_of_birth
        self.phone_no = phone_no
        self.email=email
        self.username=username
        self.PIN = PIN
        self.cid = generate_cid()
        self.active = True
        self.__recipients = []
        self.__transactions = []
        self.__balance = 0
        self.region = region
        self.card_type = card_type
        self.__age = age

    def get_age(self):
        return self.__age
    def set_age(self,age):
        self.__age = age

    def get_balance(self):
        return self.__balance
    def set_balance(self,bal):
        self.__balance = bal
    def add_balance(self,amount):
        total = amount + int(self.__balance)
        self.__balance = total
    def get_recipients(self):
        return self.__recipients
    def get_transactions(self):
        return self.__transactions
    def add_recipients(self,recipients):
        self.__recipients.append(recipients)
    def add_transactions(self,transactions):
        self.__transactions.append(transactions)


    def get_user_id(self):
        return self.user_id
    def get_first_name(self):
        return self.first_name
    def get_last_name(self):
        return self.last_name
    def get_gender(self):
        return self.gender
    def get_identity_no(self):
        return self.identity_no
    def get_identity_type(self):
        return self.identity_type
    def get_date_of_birth(self):
        return self.date_of_birth
    def get_address(self):
        return self.address
    def get_phone_no(self):
        return self.phone_no
    def get_email(self):
        return self.email
    def get_username(self):
        return self.username
    def get_PIN(self):
        return self.PIN
    def get_cid(self):
        return self.cid
    def get_active(self):
        return self.active
    def get_region(self):
        return self.region
    def get_card_type(self):
        return self.card_type

    def set_user_id(self,user_id):
        self.user_id = user_id
    def set_first_name(self,first_name):
        self.first_name = first_name
    def set_last_name(self,last_name):
        self.last_name = last_name
    def set_gender(self,gender):
        self.gender = gender
    def set_identity_no(self,identity_no):
        self.identity_no = identity_no
    def set_remarks(self,remarks):
        self.remarks = remarks
    def set_identity_type(self,identity_type):
        self.identity_type = identity_type
    def set_date_of_birth(self,date):
        self.date_of_birth=date
    def set_address(self,address):
        self.address=address
    def set_phone_no(self,phone_no):
        self.phone_no=phone_no
    def set_email(self,email):
        self.email=email
    def set_username(self,username):
        self.username=username
    def set_PIN(self,pin):
        self.PIN=pin
    def set_active(self,active):
        self.active=active
    def set_region(self,region):
        self.region=region
    def set_card_type(self,card):
        self.card_type=card

    def check_if_recipient(self,recipient):
        if recipient.get_first_name() == self.get_first_name() and recipient.get_last_name() == self.get_last_name() and recipient.get_email() == self.get_email():
            id = self.get_user_id()
            recipient.set_user_id(id)


class Login:
    count = 0
    def __init__(self,username,PIN,user_id):
        self.username = username
        self.PIN = PIN
        self.user_id=user_id
        self.id = Login.count+1
        self.logged_in = False
    def set_username(self,username):
        self.username=username
    def get_username(self):
        return self.username
    def set_PIN(self,PIN):
        self.PIN=PIN
    def get_PIN(self):
        return self.PIN
    def get_user_id(self):
        return self.user_id
    def get_id(self):
        return self.id
    def set_logged_in(self,bool):
        self.logged_in=bool
    def get_logged_in(self):
        return self.logged_in



class recipient:
    count_id = 0

    def __init__(self, first_name, last_name, gender, email, phone, remarks):
        recipient.count_id += 1
        self.__user_id = None
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__remarks = remarks
        self.__phone = phone

    def get_phone(self):
        return self.__phone

    def set_phone(self,phone):
        self.__phone = phone

    def set_email(self,email):
        self.__email = email

    def get_email(self):
        return self.__email
    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_remarks(self):
        return self.__remarks

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender
    def set_remarks(self, remarks):
        self.__remarks = remarks


class transaction:
    transfer_id = 0
    transfer_count = 0
    def __init__(self,amount,sender_id,recipient_id):
        transaction.transfer_id += 1
        self.__amount = amount
        self.__sender_id = sender_id
        self.__recipient_id = recipient_id
        self.__transac_id = transaction.transfer_id
        self.increase_count()
        self.__time = None

    def set_time(self,time):
        self.__time = time
    def get_time(self):
        return self.__time

    def set_amount(self,amount):
        self.__amount = amount
    def get_amount(self):
        return self.__amount
    def get_sender_id(self):
        return self.__sender_id
    def set_sender_id(self,sender_id):
        self.__sender_id = sender_id
    def get_recipient_id(self):
        return self.__recipient_id
    def set_recipient_id(self,recipient_id):
        self.__recipient_id = recipient_id
    def get_transact_id(self):
        return self.__transac_id

    def increase_count(self):
        transaction.transfer_count += 1

class Transfer(transaction):
    def __init__(self,amount,sender_id,recipient_id):
        super().__init__(amount,sender_id,recipient_id)
        self.__type = 'T'
        self.__max = 0



    def set_max(self,max):
        self.__max = max
    def get_max(self):
        return self.__max
    def set_type(self,type):
        self.__type = type
    def get_type(self):
        return self.__type

    def deductsender(self,curruser):
        if curruser.get_user_id() == self.get_sender_id():
            balance = curruser.get_balance()
            final = balance - self.get_amount()
            curruser.set_balance(final)
    def addreceive(self,rlist,users_dict):
        if self.get_recipient_id() in rlist:
                receipt = users_dict.get(self.get_recipient_id())
                balance = receipt.get_balance()
                final = balance + self.get_amount()
                receipt.set_balance(final)

class Deposit(transaction):
    def __init__(self,amount,sender_id,recipient_id):
        super().__init__(amount,sender_id,recipient_id)
        self.__type = 'D'

    def set_type(self,type):
        self.__type = type
    def get_type(self):
        return self.__type

    def addbalance(self,curruser):
        if self.get_sender_id() == self.get_recipient_id():
           print("test")
           curruser.add_balance(self.get_amount())

