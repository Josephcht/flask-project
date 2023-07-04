from wtforms import Form, StringField,RadioField, DateField, SelectField, validators, IntegerField, PasswordField, TextAreaField

class CreateUserForm(Form):
    first_name = StringField('First Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender:', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    identity_type = SelectField('Identity Type:', [validators.DataRequired()], choices=[('','Please Select...'),('N',"Singaporean/PR NRIC"),('M','Malaysian IC'),('P',"Passport")], default='')
    identity_no = StringField('Identity Number:', [validators.DataRequired(), validators.Length(min=9,max=9,message='Identity number not valid. Please enter a valid ID')])
    date_of_birth = DateField('Date Of Birth:', [validators.DataRequired()])
    age = IntegerField('Age', [validators.DataRequired(), validators.NumberRange(min=18,max=150,message='Invalid Age.')])
    address = StringField('Address:', [validators.DataRequired()])
    region = SelectField('region:', [validators.DataRequired()], choices=[('','Please Select...'),('N',"North"),('S','South'),('E',"East"),('W',"West")], default='')
    phone_no = IntegerField('Phone Number:', [validators.DataRequired(), validators.NumberRange(min=11111111,max=99999999,message='Invalid phone number. Please enter a valid phone number')])
    email = StringField('Email:', [validators.DataRequired(),validators.Email(message='Invalid email. Please enter a valid email such as Hoe_tuck@gmail.com',allow_empty_local=True)])
    card_type = SelectField('Card Type:', [validators.DataRequired()], choices=[('','Please Select...'),('D',"Debit Card"),('F','Forex Card'),('P',"Prepaid Card"),('C',"Charge Card")], default='')
    username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1,max=50)])
    PIN = PasswordField('PIN:', [validators.DataRequired(), validators.Length(min=6,max=6,message='Please enter a 6 number pin'), validators.EqualTo('confirm', message="Passwords entered don't match")])
    confirm = PasswordField('Re-enter PIN:')

class UpdateForm(Form):
    first_name = StringField('First Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender:', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    identity_type = SelectField('Identity Type:', [validators.DataRequired()],
                                choices=[('', 'Please Select...'), ('N', "Singaporean/PR NRIC"), ('M', 'Malaysian IC'),
                                         ('P', "Passport")], default='')
    identity_no = StringField('Identity Number:', [validators.DataRequired(), validators.Length(min=9, max=9,
                                                                                                message='Identity number not valid. Please enter a valid ID')])
    date_of_birth = DateField('Date Of Birth:', [validators.DataRequired()])
    address = StringField('Address:', [validators.DataRequired()])
    phone_no = IntegerField('Phone Number:', [validators.DataRequired(),
                                              validators.NumberRange(min=11111111, max=99999999,
                                                                     message='Invalid phone number. Please enter a valid phone number')])
    region = SelectField('region:', [validators.DataRequired()], choices=[('','Please Select...'),('N',"North"),('S','South'),('E',"East"),('W',"West")], default='')
    email = StringField('Email:', [validators.DataRequired(), validators.Email(
        message='Invalid email. Please enter a valid email such as Hoe_tuck@gmail.com', allow_empty_local=True)])
    username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1, max=50)])
class LoginForm(Form):
     username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1,max=50)])
     PIN = PasswordField('PIN:', [validators.DataRequired(),
                                 validators.Length(min=6, max=6, message='Please enter a 6 number pin')])
class DeleteForm(Form):
    username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    PIN = PasswordField('PIN:', [validators.DataRequired(),
                                validators.Length(min=6, max=6, message='Please enter a 6 number pin')])
class ChangePINForm(Form):
    username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    initial = PasswordField('Initial PIN:',[validators.DataRequired(),
                                 validators.Length(min=6, max=6, message='Please enter a 6 number pin')])
    PIN = PasswordField('New PIN:', [validators.DataRequired(),
                                 validators.Length(min=6, max=6, message='Please enter a 6 number pin'),
                                 validators.EqualTo('confirm', message="Passwords entered don't match")])
    confirm = PasswordField('Re-enter New PIN:')

class ForgetPIN(Form):
    username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    identity_no = StringField('Identity Number:', [validators.DataRequired(), validators.Length(min=9, max=9,
                                                                                                message='Identity number not valid. Please enter a valid ID')])
    date_of_birth = DateField('Date Of Birth:', [validators.DataRequired()])
    PIN = PasswordField('New PIN:', [validators.DataRequired(),
                                 validators.Length(min=6, max=6, message='Please enter a 6 number pin'),
                                 validators.EqualTo('confirm', message="Passwords entered don't match")])
    confirm = PasswordField('Re-enter New PIN:')

class LockCardForm(Form):
    username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    PIN = PasswordField('PIN:', [validators.DataRequired(),
                                 validators.Length(min=6, max=6, message='Please enter a 6 number pin')])



class CreateRecipientForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField('Email:', [validators.DataRequired(),validators.Email(message='Invalid email. Please enter a valid email such as Hoe_tuck@gmail.com',allow_empty_local=True)])
    phone = IntegerField('Phone Number:', [validators.DataRequired(),
                                              validators.NumberRange(min=11111111, max=99999999,
                                                                     message='Invalid phone number. Please enter a valid phone number')])
    remarks = TextAreaField('Remarks', [validators.Optional()])


class testform(Form):
    balance = IntegerField('Balance',[validators.Optional()])



class transferform(Form):

    recipient = SelectField('Recipient Name', [validators.DataRequired()], coerce=int)
    amount = IntegerField("Amount", [validators.DataRequired()])

    def validate_amount(form,field):
        if field.data > field.max:
            raise validators.ValidationError(message="Value must be lower than current balance")


class ReportForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email',[validators.Length(min=1,max=150), validators.DataRequired()])
    reason = RadioField('Reason',choices=[('1', 'Loans'), ('2', 'Fees'), ('3', 'E-service'), ('4', 'Customer Service'), ('5', 'Others'),('6','None')],default = 'loans')
    report = TextAreaField('Report Issue', [validators.Optional()])
    rating = RadioField('Rating', choices=[('1', '1 - Very Bad'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 - Very Good')],default = '1')
    feedback = TextAreaField('Feedback', [validators.Optional()])

class UpdateCardType(Form):
    card_type = SelectField('Card Type:', [validators.DataRequired()], choices=[('','Please Select...'),('D',"Debit Card"),('F','Forex Card'),('P',"Prepaid Card"),('C',"Charge Card")], default='')


class UnlockCardForm(Form):
    username = StringField('Username:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    identity_no = StringField('Identity Number:', [validators.DataRequired(), validators.Length(min=9, max=9,
                                                                                                message='Identity number not valid. Please enter a valid ID')])
