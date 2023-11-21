from flask import Flask ,render_template,request,redirect,flash

from flask_mail import Mail,Message
import os

import mysql.connector


con = mysql.connector.connect(host = "localhost", username ="root",password= "ayush22001",database = "webst")
cur = con.cursor()

my_web = Flask(__name__)
my_web.secret_key = "my secret key"

my_web.config['MAIL_SERVER']='smtp.gmail.com'
my_web.config['MAIL_PORT'] = 465
my_web.config['MAIL_USERNAME'] = 'ayushdhiman4645@gmail.com'
my_web.config['MAIL_PASSWORD'] = 'aedf ezos rata jtpd'
my_web.config['MAIL_USE_TLS'] = False
my_web.config['MAIL_USE_SSL'] = True
mail = Mail(my_web)




@my_web.route("/")
def home():
    return render_template('home.html')

# @my_web.route("/about")
# def about():
#     nam = "ayush"
#     return render_template("about.html",nam=nam)


@my_web.route("/a")
def about():
    return render_template("about.html")

@my_web.route("/c")
def contact():
    return render_template("contact.html")

@my_web.route("/s",methods = ["POST"])
def savedata(): 
    if request.method == "POST":
        # print("savedata")

        fname = request.form.get("name")
        em = request.form.get("email")
        msg = request.form.get("message")
        Imag = request.files.get("img")
        print(Imag, "xxxxxxxxxxxxxxxxxx")
        if Imag:
            Imag.save(os.path.join("static/images",Imag.filename))
            imx = os.path.join("static/images/",Imag.filename)



        cur.execute(f"insert into ws values('{fname}','{em}','{msg}','{imx}')")
        con.commit()

        msag  = Message("Message from Flash ",sender="ayushdhiman4645@gmail.com",recipients=["ayushdhiman4645@gmail.com"])
        msag.body = f"""User Info::
        Name = {fname}
        Email = {em}
        message = {msg}"""

        mail.send(msag)


        flash(" Data saved sucessfully!")




        return redirect("/d")
    
    
# //////how to delte///////



@my_web.route("/d")
def det():
    cur.execute("select * from ws;")
    data = cur.fetchall()
    # print(data)   
    return render_template("detail.html",alldata = data)



@my_web.route("/r/<x>",methods = ["POST"])
def remv(x):    
    cur.execute(f"delete from ws where Name ='{x}'")
    con.commit()
    return redirect("/d")



# ///////////////////how to update the data////////////

@my_web.route("/showupdate/<x>",methods=["POST"])
def updtedata(x):
     
     cur.execute(f"select * from ws where name='{x}'")
     record = cur.fetchone()
     print(record, "xxxxxxxxxxxxx")
     return render_template("updatedata.html",data = record)



@my_web.route("/update/<x>",methods=["POST"])
def updatenow(x):
     
    if request.method == "POST":
     fname = request.form.get("name")
     em  = request.form.get("email")
     msg = request.form.get("message")
     print(fname,em,msg)
     cur.execute(f'update ws  set name="{fname}",email="{em}",message="{msg}" where name = "{x}";')
     con.commit()


     redirect("/showupdate")

# /////////////////////////how to save image and show image in contact us page//////////////////////




@my_web.route("/xyz/<d>")
def xyz(d):
    return f"this is a car {d}"





    

my_web.run(debug=True)