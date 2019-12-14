from flask import Flask
from flask_mail import Mail, Message

app =Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'databaseproject159753@gmail.com'
app.config['MAIL_PASSWORD'] = 'dbmsproject'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

@app.route("/")
def index():
   msg = Message('Hello',sender = 'databaseproject159753@gmail.com',recipients = ['hkumarks14@gmail.com'])
   msg.body = messageBody    
   
   
   messageBody="""Your trip details
   
        Name:%s
        E-mail:%s
        Mobile Number:%s
        Departure:%s
        Destination:%s
        Date:%s
        Time:6:00AM
        Accomodation Nuumber:%s
        Service Type:%s
        Number of people:%s

    For further details a new mail will be sent shortly.

    Regards
    TravelWithUs
   """%()

   mail.send(msg)
   return "Sent"

if __name__ == '__main__':
   app.run(debug = True)