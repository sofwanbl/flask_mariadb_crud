from flask import render_template, request, url_for, redirect
from flaskext.mysql import MySQL
from app import app
from app.frm_entry import EntryForm

# Connecting database
app.config["MYSQL_DATABASE_HOST"]="localhost"
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]="opansan63"
app.config["MYSQL_DATABASE_DB"]="test"
app.config["MYSQL_PORT"]="3306"

# Preparing variable on mysqlnya
mysqlnya=MySQL(app)
mysqlnya.init_app(app)

@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/frm_entry", methods=["GET","POST"])
def frm_entry():
    resultnya=0
    rem=""
    xvalue_1=0
    xvalue_2=0
    xoperator=""    
    
    formnya=EntryForm()
    
    # Save inputted data to variables
    if request.method=="POST":
        details=request.form
        xvalue_1=details["value_1"]
        xvalue_2=details["value_2"]
        xoperator=details["operatornya"]
    
    # Processing result
    if xoperator=="+":
       resultnya=int(xvalue_1)+int(xvalue_2)
    elif xoperator=="-":
       resultnya=int(xvalue_1)-int(xvalue_2)
    elif xoperator=="/":
       resultnya=int(xvalue_1)/int(xvalue_2)
    elif xoperator=="*":
       resultnya=int(xvalue_1)*int(xvalue_2)    
   
    # Processing remarks, Even, Odd or Zero
    if resultnya==0:
        rem="Zero"
    elif resultnya % 2 ==0:    
        rem="Even"
    elif resultnya % 2==1:
         rem="Odd"    
    else:
        rem=""

    # Save data        
    cur=mysqlnya.connect().cursor()
    cur.execute("insert into penjumlahan (value_1,value_2,operator,result, remark) values (%s,%s,%s,%s,%s)",((xvalue_1,xvalue_2,xoperator,resultnya,rem)))
    cur.connection.commit()
    cur.close()
    
    return render_template("frm_entry.html", title="Nilai", formnya=formnya, xresultnya=resultnya, remnya=rem)

@app.route("/display_data")    
def display_data():
    formnya=EntryForm()     
       
    cur=mysqlnya.connect().cursor()
    cur.execute("select * from penjumlahan")
    hasilnya=cur.fetchall()    
    return render_template("tampil_data.html", title="Tampil Data",hasilnya=hasilnya,no=1)

@app.route("/frm_edit_data/<id>",methods=["GET","POST"])
def frm_edit_data(id):
    cur=mysqlnya.connect().cursor()
    form=EntryForm()
    cur.execute("select * from penjumlahan where id='"+id+"'")
    hasilnya=cur.fetchall()    
    for rows in hasilnya:
        xvalue_1=rows[1]
        xvalue_2=rows[2]
        xoperator=rows[3]
        xresult=rows[4]
        xremark=rows[5]    
        
    if request.method=="POST":       
       
       details=request.form
       xvalue_1=details["value_1"]
       xvalue_2=details["value_2"]
       xoperator=details["operatornya"]
       
       # Memproses hasil    
       if xoperator=="+":
          xresult=float(xvalue_1)+float(xvalue_2)
       elif xoperator=="-":
          xresult=float(xvalue_1)-float(xvalue_2)
       elif xoperator=="/":
          xresult=float(xvalue_1)/float(xvalue_2)
       elif xoperator=="*":
           xresult=float(xvalue_1)*float(xvalue_2)
       else:
           xresult=0
        
       # Menentukan Ganjil atau Genap
       if xresult % 2 ==0:
          xremark="Even"
       elif xresult % 2==1:
          xremark="Odd"
       else:
          xremark="Zero"   
       
       cur=mysqlnya.connect().cursor()
       #cur.execute("update penjumlahan set value_1='"+xnilai_1+"'"+
       #            ",value_2='"+xnilai_2+"'"+",operator='"+xoperator+"'"+
       #            ",result='"+hasil+"'"+",remark='"+xremark+"'"+"where id='"+id+"'")
       
       cur.execute ("update penjumlahan set value_1=%s,value_2=%s,operator=%s,result=%s,remark=%s where id= %s",
                    ((xvalue_1,xvalue_2,xoperator,xresult,xremark,id)))
       cur.connection.commit()
       cur.close()
    else:   
       form.value_1.data=xvalue_1    
       form.value_2.data=xvalue_2
       form.operatornya.data=xoperator          
    
    return render_template("frm_edit.html", title="Edit Data",znilai_1=xvalue_1,form=form,
                           ketnya=xremark,hasilnya=xresult)    

@app.route("/delete_data/<id>", methods=["GET","POST"])
def delete_data(id):
    cur=mysqlnya.connect().cursor()
    cur.execute("delete from penjumlahan where id='"+id+"'")
    cur.connection.commit()
    cur.close()    
    return redirect(url_for("display_data"))