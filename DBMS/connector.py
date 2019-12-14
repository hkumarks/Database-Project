from flask import Flask, render_template, request,url_for,redirect,flash,session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
# from tables import Results
app = Flask(__name__)

mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'databaseproject159753@gmail.com'
app.config['MAIL_PASSWORD'] = 'dbmsproject'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'harsha240'
app.config['MYSQL_DB'] = 'project'
app.secret_key='travelwithus'

mysql = MySQL(app)

em=[]
harshatotal=9
@app.route("/mail")
def index():
   msg = Message('Welcome',sender = 'databaseproject159753@gmail.com',recipients = em)
   msg.body = """
   Dear Customer,
        The best way to form a strong bond with someone is to travel with them. We are enlighted to have you in our community.
        Looking forward to plan an amazing vacation for you.
        
    With Regards
    TravelWithUs"""
   mail.send(msg)
   em.clear()
   return redirect(url_for('signin'))

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        details = request.form
        name = details['name']
        email = details['email']
        password = details['password']
        phone = int(details['phone_number'])
        # depart=details['depart']
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO customer(name,email,password,phone,departure) VALUES (%s, %s,%s, %s,%s)", (name,email,password,phone,depart))
        # mysql.connection.commit()
        # cur.close()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer(name,email,password,phone) VALUES (%s,%s, %s,%s)", (name,email,password,phone))
        mysql.connection.commit()
        cur.close()
        em.append(email)
        # session['email']=email
        return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        details = request.form
        email = details['email']
        password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("select password from customer where email=%s",[str(email)])
        passw=cur.fetchall()
        cur.close()
        print(passw)
        if passw:
            if passw[0][0]==password:
                session['email']=email
                return redirect(url_for('home'))
            else:
                return redirect(url_for('wrong'))
        else:
            return redirect(url_for('invalid'))
    return render_template('signin.html')



@app.route('/admin-signin', methods=['GET', 'POST'])
def adminsignin():
    if request.method == "POST":
        details = request.form
        name = details['name']
        password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("select emp_password from employee where emp_name=%s",[str(name)])
        passw=cur.fetchall()
        cur.close()
        if passw:
            if passw[0][0]==password:
                return redirect(url_for('admin'))
            else:
                # flash('wrong password')
                return redirect(url_for('wrong'))       
                # return render_template('signin.html')
        else:
            return redirect(url_for('notadmin'))
    return render_template('admin-signin.html')

@app.route('/admin-signin/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin-signin/update',methods=['GET','POST'])
def adminupdate():
    cur=mysql.connection.cursor()
    cur.execute("select * from places")
    data=cur.fetchall()
    cur.close()
    # table=Results(data)
	# # table.border=True
    return render_template('adminupdate.html',places=data)   

@app.route('/admin-signin/adminview')
def adminview():
    cur = mysql.connection.cursor()
    cur.execute("select * from cust")
    c = cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select * from accomodation")
    acc=cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("select * from payment")
    pay = cur.fetchall()
    cur.close()
    return render_template ("adminview.html",cust=c,accomodation=acc,payment=pay)

@app.route('/admin-signin/update/edit',methods=['GET','POST'])
def updateprice():
    if request.method == "POST":
        details = request.form
        dep = details['depname']
        des = details['desname']
        price = details['price']
        print(dep)
        print(des)
        print(price)
        query = 'update places set {dep} = {price} where destination= "{des}"'.format(dep=dep, price=price, des=des)

        cur = mysql.connection.cursor()
        cur.execute(query)
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('adminupdate'))
    return render_template('edit.html')

@app.route('/#wrong')
def wrong():
    return render_template('wrong.html')

@app.route('/#not')    
def notadmin():
    return render_template('not-admin.html')

@app.route('/#invalid')
def invalid():
    return render_template('invalid.html')

@app.route('/home',methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        details=request.form
        depart=details['depart']
        dest=details['destination']
        cur=mysql.connection.cursor()
        email=session['email']
        
        cur=mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        # cur.execute(" update customer set destination =%s where email = %s",(dest,email))
        # mysql.connection.commit()
        # cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO trip(c_id,departure,destination) VALUES (%s,%s,%s)", (cid[0][0],depart,dest))
        mysql.connection.commit()
        cur.close()
        
        cur=mysql.connection.cursor()
        cur.execute("insert into prices(c_id) select c_id from customer where email=%s",[str(email)])
        mysql.connection.commit()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("select departure from trip where c_id=%s",[cid[0][0]])
        depart=cur.fetchall()
        cur.close()
        
        cur=mysql.connection.cursor()
        cur.execute("select * from places where destination=%s", [dest])
        travelprice = cur.fetchall()
        cur.close()

        diction={'bangalore':1,'mumbai':2,'delhi':3,'chennai':4}    
        
        cur=mysql.connection.cursor()
        cur.execute("update prices set travel_price=%s where c_id=%s",(travelprice[0][diction[depart[0][0]]],cid[0][0]))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for(dest))
    return render_template('first-page.html')   

@app.route('/home/profile',methods=['GET','POST'])
def profile():
    email=session['email']
    cur=mysql.connection.cursor()
    cur.execute("select name from customer where email=%s",[str(email)])
    name=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select phone from customer where email=%s",[str(email)])
    n=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select c_id from customer where email=%s",[str(email)])
    c=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select * from custprofile where Customer_ID=%s",[c[0][0]])
    data=cur.fetchall()
    cur.close()
    return render_template('profilepage.html',cid=str(c[0][0]),name=name[0][0],mail=email,num=str(n[0][0]),custprofile=data) 
       

@app.route('/calc')    
def logout():
    session.pop('email',None)
    return redirect(url_for('signup'))            

@app.route('/home/bali',methods=['GET', 'POST'])
def bali():
    if request.method == "POST":
        details = request.form
        ser_type = details['service type']
        start = details['startdate']
        end = details['enddate']
        num = details['numofppl']
        email=session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO accomodation(c_id,people_num,service_type,start_date,end_date) VALUES (%s,%s, %s,%s, %s)", (cid[0][0],num,ser_type,start,end))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('invoice'))
    return render_template('bali.html')

@app.route('/home/barcelona',methods=['GET', 'POST'])
def barcelona():
    if request.method == "POST":
        details = request.form
        ser_type = details['service type']
        start = details['startdate']
        end = details['enddate']
        num = details['numofppl']
        email=session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO accomodation(c_id,people_num,service_type,start_date,end_date) VALUES (%s,%s, %s,%s, %s)", (cid[0][0],num,ser_type,start,end))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('invoice'))
    return render_template('barcelona.html')

@app.route('/home/dubai',methods=['GET', 'POST'])
def dubai():
    if request.method == "POST":
        details = request.form
        ser_type = details['service type']
        start = details['startdate']
        end = details['enddate']
        num = details['numofppl']
        email=session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO accomodation(c_id,people_num,service_type,start_date,end_date) VALUES (%s,%s, %s,%s, %s)", (cid[0][0],num,ser_type,start,end))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('invoice'))
    return render_template('dubai.html')

@app.route('/home/miami',methods=['GET', 'POST'])
def miami():
    if request.method == "POST":
        details = request.form
        ser_type = details['service type']
        start = details['startdate']
        end = details['enddate']
        num = details['numofppl']
        email=session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO accomodation(c_id,people_num,service_type,start_date,end_date) VALUES (%s,%s, %s,%s, %s)", (cid[0][0],num,ser_type,start,end))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('invoice'))
    return render_template('miami.html')

@app.route('/home/san',methods=['GET', 'POST'])
def san_francisco():
    if request.method == "POST":
        details = request.form
        ser_type = details['service type']
        start = details['startdate']
        end = details['enddate']
        num = details['numofppl']
        email=session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO accomodation(c_id,people_num,service_type,start_date,end_date) VALUES (%s,%s, %s,%s, %s)", (cid[0][0],num,ser_type,start,end))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('invoice'))
    return render_template('san.html')

@app.route('/home/sydney',methods=['GET', 'POST'])
def sydney():
    if request.method == "POST":
        details = request.form
        ser_type = details['service type']
        start = details['startdate']
        end = details['enddate']
        num = details['numofppl']
        email=session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO accomodation(c_id,people_num,service_type,start_date,end_date) VALUES (%s,%s, %s,%s, %s)", (cid[0][0],num,ser_type,start,end))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('invoice'))
    return render_template('sydney.html')

@app.route('/home/invoice',methods=['GET','POST'])
def invoice():
    email=session['email']
    cur=mysql.connection.cursor()
    cur.execute("select name from customer where email=%s",[str(email)])
    name=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select c_id from customer where email=%s",[str(email)])
    cid=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select phone from customer where email=%s",[str(email)])
    mob=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select departure from trip where c_id=%s",[cid[0][0]])
    dept=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select destination from trip where c_id=%s",[cid[0][0]])
    dest=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select start_date from accomodation where c_id=%s",[cid[0][0]])
    date=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select acmdn_num from accomodation where c_id=%s",[cid[0][0]])
    acc=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select service_type from accomodation where c_id=%s",[cid[0][0]])
    ser=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select people_num from accomodation where c_id=%s",[cid[0][0]])
    ppl=cur.fetchall()
    cur.close()
    # em.append(email)
    # # messageBody="""Your trip details
   
    # #     Name:%s
    # #     E-mail:%s
    # #     Mobile Number:%s
    # #     Departure:%s
    # #     Destination:%s
    # #     Date:%s
    # #     Time:6:00AM
    # #     Accomodation Nuumber:%s
    # #     Service Type:%s
    # #     Number of people:%s

    # # For further details a new mail will be sent shortly.

    # # Regards
    # # TravelWithUs
    # # """%(name[0][0],email,mob[0][0],dept[0][0],dest[0][0],date[0][0],acc[0][0],ser[0][0],ppl[0][0])

    # msg = Message('Hello',sender = 'databaseproject159753@gmail.com',recipients = [em])
    # msg.body ="""Your trip details
   
    #     Name:%s
    #     E-mail:%s
    #     Mobile Number:%s
    #     Departure:%s
    #     Destination:%s
    #     Date:%s
    #     Time:6:00AM
    #     Accomodation Nuumber:%s
    #     Service Type:%s
    #     Number of people:%s

    # For further details a new mail will be sent shortly.

    # Regards
    # TravelWithUs
    # """%(name[0][0],email,mob[0][0],dept[0][0],dest[0][0],date[0][0],acc[0][0],ser[0][0],ppl[0][0])   
    # mail.send(msg)
    # em.clear()

    return render_template('invoice.html',n=str(name[0][0]),e=str(email),m=str(mob[0][0]),dep=str(dept[0][0]),des=str(dest[0][0]),date=str(date[0][0]),a=str(acc[0][0]),ser=str(ser[0][0]),num=str(ppl[0][0]))
    
@app.route('/home/invoice2',methods=['GET','POST'])
def invoice2():
    email=session['email']
    cur=mysql.connection.cursor()
    cur.execute("select name from customer where email=%s",[str(email)])
    name=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select c_id from customer where email=%s",[str(email)])
    cid=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select phone from customer where email=%s",[str(email)])
    mob=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select departure from trip where c_id=%s",[cid[0][0]])
    dept=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select destination from trip where c_id=%s",[cid[0][0]])
    dest=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select start_date from accomodation where c_id=%s",[cid[0][0]])
    date=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select acmdn_num from accomodation where c_id=%s",[cid[0][0]])
    acc=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select service_type from accomodation where c_id=%s",[cid[0][0]])
    ser=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select people_num from accomodation where c_id=%s",[cid[0][0]])
    ppl=cur.fetchall()
    cur.close()
    return render_template('invoice2.html',n=str(name[0][0]),e=str(email),m=str(mob[0][0]),dep=str(dept[0][0]),des=str(dest[0][0]),date=str(date[0][0]),a=str(acc[0][0]),ser=str(ser[0][0]),num=str(ppl[0][0]))
    
    

@app.route('/home/invoice/payment',methods=['GET','POST'])
def payment():
    email=session['email']
    cur=mysql.connection.cursor()
    cur.execute("select c_id from customer where email=%s",[str(email)])
    cid=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select people_num from accomodation where c_id=%s",[cid[0][0]])
    pplnum=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select datediff(end_date,start_date) from accomodation where c_id=%s",[cid[0][0]])
    numofday=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select destination from trip where c_id=%s",[cid[0][0]])
    dest=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select service_type from accomodation where c_id=%s",[cid[0][0]])
    sertype=cur.fetchall()
    cur.close()

    cur=mysql.connection.cursor()
    cur.execute("select * from hotel where service_type=%s",[sertype[0][0]])
    price=cur.fetchall()
    cur.close()


    dicti={'miami':1,'sydney':2,'san_francisco':3,'bali':4,'barcelona':5,'dubai':6}          

    cur=mysql.connection.cursor()
    cur.execute("update prices set acdmn_price=(%s * %s * %s) where c_id=%s",(price[0][dicti[dest[0][0]]],pplnum[0][0],numofday[0][0],cid[0][0]))
    mysql.connection.commit()
    cur.close()
    print("qqq")
    cur=mysql.connection.cursor()
    cur.execute("update prices set total_price=acdmn_price+travel_price where c_id=%s",[cid[0][0]])
    mysql.connection.commit()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select total_price from prices where c_id=%s",[cid[0][0]])
    total=cur.fetchall()
    cur.close()
    session['old']=total[0][0]
    if request.method=="POST":
        details=request.form
        c_type=details['c_type']
        c_num=details['cardnumber']
        c_stat=details['status']
        cur=mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO payment(c_id,payment_type,card_num,payment_status) VALUES (%s,%s,%s,%s)", (cid[0][0],c_type,c_num,c_stat))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('thankyou'))
    # cur=mysql.connection.cursor()
    # cur.execute("update")
    # mysql.connection.commit()
    # cur.close()    
    cur=mysql.connection.cursor()
    cur.execute("select travel_price from prices where c_id=%s",[cid[0][0]])
    tp=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select acdmn_price from prices where c_id=%s",[cid[0][0]])
    ap=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select total_price from prices where c_id=%s",[cid[0][0]])
    tot=cur.fetchall()
    cur.close()
    return render_template('payment.html',msg1 = str(tp[0][0]), msg2 = str(ap[0][0]), msg3=str(tot[0][0]) )  


@app.route('/home/invoice2/payment2',methods=['GET','POST'])
def payment2():
    email=session['email']
    cur=mysql.connection.cursor()
    cur.execute("select c_id from customer where email=%s",[str(email)])
    cid=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select people_num from accomodation where c_id=%s",[cid[0][0]])
    pplnum=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select datediff(end_date,start_date) from accomodation where c_id=%s",[cid[0][0]])
    numofday=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select destination from trip where c_id=%s",[cid[0][0]])
    dest=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select service_type from accomodation where c_id=%s",[cid[0][0]])
    sertype=cur.fetchall()
    cur.close()

    cur=mysql.connection.cursor()
    cur.execute("select * from hotel where service_type=%s",[sertype[0][0]])
    price=cur.fetchall()
    cur.close()


    dicti={'miami':1,'sydney':2,'san_francisco':3,'bali':4,'barcelona':5,'dubai':6}          


    cur=mysql.connection.cursor()
    cur.execute("update prices set acdmn_price=(%s * %s * %s) where c_id=%s",(price[0][dicti[dest[0][0]]],pplnum[0][0],numofday[0][0],cid[0][0]))
    mysql.connection.commit()
    cur.close()
    print("qqq")
    cur=mysql.connection.cursor()
    cur.execute("update prices set total_price=acdmn_price+travel_price where c_id=%s",[cid[0][0]])
    mysql.connection.commit()
    cur.close()
    if request.method=="POST":
        details=request.form
        c_type=details['c_type']
        c_num=details['cardnumber']
        c_stat=details['status']
        cur=mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customer WHERE email=%s",[str(email)])
        cid=cur.fetchall()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("update payment set payment_type=%s,card_num=%s,payment_status=%s where c_id=%s",(c_type,c_num,c_stat,cid[0][0]))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('thankyou'))
    # cur=mysql.connection.cursor()
    # cur.execute("update")
    # mysql.connection.commit()
    # cur.close()    
    cur=mysql.connection.cursor()
    cur.execute("select travel_price from prices where c_id=%s",[cid[0][0]])
    tp=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select acdmn_price from prices where c_id=%s",[cid[0][0]])
    ap=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select total_price from prices where c_id=%s",[cid[0][0]])
    tot=cur.fetchall()
    cur.close()
    msg3 = session['old']
    amount=int(tot[0][0])-int(msg3)
    return render_template('payment2.html',msg1 = str(tp[0][0]), msg2 = str(ap[0][0]), msg3=msg3,msg4=str(tot[0][0]),msg5=str(amount) ) 

@app.route('/home/payment/thankyou',methods=['GET','POST'])
def thankyou():
    email=session['email']
    return render_template('thanktomain.html')

@app.route('/home/profile/cancel',methods=['GET','POST'])
def cancel():
    email=session['email']
    cur=mysql.connection.cursor()
    cur.execute("select c_id from customer where email=%s",[str(email)])
    cid=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("delete from trip where c_id=%s",[cid[0][0]])
    mysql.connection.commit()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("delete from accomodation where c_id=%s",[cid[0][0]])
    mysql.connection.commit()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("delete from payment where c_id=%s",[cid[0][0]])
    mysql.connection.commit()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("delete from prices where c_id=%s",[cid[0][0]])
    mysql.connection.commit()
    cur.close()
    em.append(email)
    return redirect(url_for('indexcancel'))
    
@app.route('/home/profile/edit',methods=['GET','POST'])
def tripedit():
    email=session['email']
    cur=mysql.connection.cursor()
    cur.execute("select c_id from customer where email=%s",[str(email)])
    cid=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select departure from trip where c_id=%s",[cid[0][0]])
    dept=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select destination from trip where c_id=%s",[cid[0][0]])
    dest=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select start_date from accomodation where c_id=%s",[cid[0][0]])
    sdate=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select end_date from accomodation where c_id=%s",[cid[0][0]])
    edate=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select service_type from accomodation where c_id=%s",[cid[0][0]])
    ser=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select people_num from accomodation where c_id=%s",[cid[0][0]])
    ppl=cur.fetchall()
    cur.close()
    cur=mysql.connection.cursor()
    cur.execute("select total_price from prices where c_id =%s",[cid[0][0]])
    temp=cur.fetchall()
    session['old']=temp[0][0]
    cur.close()
    # print(dept)
    # print(dest)
    # print(sdate)
    # print(edate)
    # print(ser)
    # print(ppl)
    if request.method == "POST":
        details = request.form
        departure=details['depart']
        destination=details['dest']
        start = details['start']
        end = details['end']
        ser_type = details['ser']
        num = details['ppl']
        cur=mysql.connection.cursor()
        cur.execute("update trip set departure=%s,destination=%s where c_id=%s",(departure,destination,cid[0][0]))
        mysql.connection.commit()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("update accomodation set people_num=%s,service_type=%s,start_date=%s,end_date=%s where c_id=%s",(num,ser_type,start,end,cid[0][0]))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('invoice2'))
    return render_template('tripedit.html',dep=str(dept[0][0]),des=str(dest[0][0]),start=str(sdate[0][0]),end=str(edate[0][0]),ser=str(ser[0][0]),ppl=str(ppl[0][0]))

@app.route("/mail1")
def indexcancel():
   msg = Message('Cancelled',sender = 'databaseproject159753@gmail.com',recipients = em)
   msg.html = "<h3><i>Dear Customer,<br>&nbsp;&nbsp;&nbsp;Your trip has been cancelled.Sorry for the inconvenience caused if any. Payment will be refunded shortly to your account.<br>With Regards<br>TravelWithUs</i></h3>"
   mail.send(msg)
   em.clear()
   return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug = True)