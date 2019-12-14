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
   msg = Message('Hello',sender = 'databaseproject159753@gmail.com',recipients = ['manoj.islore@gmail.com'])
   msg.body = "The best way to form a strong bond with someone is to travel with them. We are enlighted to have you in our community. Looking forward to plan an amazing vacation for you."
   mail.send(msg)
   return "Sent"

if __name__ == '__main__':
   app.run(debug = True)