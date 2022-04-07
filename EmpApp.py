from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *
from datetime import datetime

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('AboutUs.html', about=about)


@app.route("/getemp", methods=['GET','POST'])
def GetEmp():
    return render_template('GetEmp.html', GetEmp=GetEmp)
        
@app.route("/fetchdata", methods=['GET','POST'])
def fetchdata();
if request.method == 'POST':
try:
    emp_id = request.form['emp_id']
    cursor = db_conn.cursor()
    
    fetch_emp_sql = "SELECT * employee WHERE emp_id = %s"
    cursor.execute(fetch_emp_sql,(emp_id))
    emp= cursor.fetchall()
    
    (id,fname,lname,priSkill,location,job,salary,email,phone_no,reg_datetime,benefit =emp[0])
    image_url = show_image(custombucket)
    
    att_emp_sql = "SELECT attendance.date, attendance.time, 
attendance.att_values FROM attendance INNER JOIN employee ON
attendance.emp_id = employee.emp_id WHERE employee.emp_id = %s"
    mycursor = db_conn.cursor()
    mycursor.execute(att_emp_sql, (emp_id))
    att_result= mycursor.fetchall()
    
    return render_template('GetEmpOutput.html')',
id=id,fname=fname,lname=lname,priSkill=priSkill,location=location,job=job,salary=salary,email=email,phone_no=phone_no,reg_datetime=reg_datetime,benefit=benefit,
image_url=image_url,att_result=att_result)
   except Exception as e:
   return render_template('IdNotFound.html')
   else:
        return render_template('AddEmp.html', fetchdata=fetchdata)
        
@app.route('/delete-emp', methods=['GET','POST'])
def DeleteEmp():
emp_id= request.form['emp_id']

mycursor = db_conn.cursor()
del_att_sql = "DELETE FROM attendance WHERE emp_id = %s"
mycursor.execute(del_att_sql, (emp_id))
db_conn.commit()

s3_client = boto3.client('s3')
emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
try:
    s3_client.delete-object(Bucket=custombucket, key = emp_image_file_name_in_s3)
    return render_template("SuccessDelete.html")
  except Exception as e:
    return render_template('UnsuccessDelete.html')
    
@app.route('/attendance-emp', methods=['GET', [POST]])
def AttendanceEmp():
  if request.method == 'POST':
  
  #datetime object containing current date and time
  now = datetime.now()
  dt_string = now.strftime("%d%m%Y%H%M%S")
  d_string = now.strftime("%d%m%Y")
  t_string = now.strftime("%H:%M:%S")
  
  attendance_id = request.form['attendance_id'] + dt_string
  date = request.form['date'] + d_string
  time = request.form['time'] + d_string
  attendance = request.form.getlist('attendance')
  emp_id = request.form['emp_id']
  
  #cursor = db_conn.cursor(db_conn.cursor.DictCursor)
  
  attence = ','.join(attendance)
  att_values = (attendance)
  
  try:
      
      insert_att_sql = 'INSERT INTO attendance VALUES (%S,%S,%S,%S,%S)'
      cursor = db_conn.cursor()
      
      cursor.execute(insert_att_sql,
      (attendance_id,date,time,att_values,emp_id))
                                 db_conn.commit()
                                 
                     return render_template('SuccessTakeAttendance.html', Id = attendance_id)
                     
                     except Exception as e:
                     return str(e)
                     
                     finally:
                     cursor.close()
                     
@app.route("/addemp", methods=['GET','POST'])
def AddEmp():
    if request.method == 'POST':

    #datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    reg = now.strftime("%d%m%Y %H:%M:%S") 

    emp_id = request.form['emp_id'] + dt_string
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    job = request.form['job']
    salary = request.form['salary']
    email = request.form['email']
    phone_no = request.form['phone_no']
    reg_datetime = request.form['reg_datetime']
    emp_image_file = request.files['emp_image_file']
    
    emp_image_file = request.files['emp_image_file']
    
    insert_sql = "INSERT INTO employee VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor = db_conn..cursor()
    
    if emp_image_file.filename == "":
       return "Please select a file"
       
    try:
    
        cursor.execute(inset_sql, (emp_id, first_name, last_name, pri_skill, location,job,salary,email,phone_no,reg_datetime,benefit))
        db_conn.commit()
        
        emp_name = "" + first_name + " " + last_name
        #Upload image file in s3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        
        s3 = boto3.resource('s3')
        
        try:
            print("Data inserted in MySQL RDS... uploading image to s3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])
            
            if s3_location is None:
               s3_location = ''
            else
               s3_location = '-' + s3_location
               
            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
            s3_location,
            custombucket,
            emp_image_file_name_in_s3)
            
            except Exception as e:
            return str(e)
            
            finally:
                cursor.close()
                
            print("all modification done...")
            return render_template('AddEmpOutput.html', name=emp_name, id=emp_id)
            
               else:
                   return render_template('GetEmp.html', AddEmp=AddEmp)
@app.route("/editemp", methods=['GET','POST'])
def EditEmp():
    if request.method == 'POST':
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_id = request.form['emp_id']
    emp_image_file = request.files['emp_image_file']
    job = request.form['job']
    salary = request.form['salary']
    email = request.form['email']
    phone_no = request.form['phone_no']
   
   update_sql = "UPDATE employee SET first_name = %s, last_name = %s,
   pri_skill = %s, location = %s,job = %s,salary = %s,email = %s,phone_no=%s
   WHERE emp_id = %s"
          cursor = db_conn.cursor()

          changefield = (first_name, last_name, pri_skill, location, job, salary, email, phone_no, emp_id)

    try:
        cursor.execute(update_sql, (changefield))
        db_conn.commit()
        emp_name = "" + first_name + "" + last_name

        #if user upload new image
        if emp_image_file_name == "";
             print("select nothing")

        else:
            #delete previous version of image in s3 then upload the new one (avoid of mutiple version store in s3)
             s3_client = boto3.client('s3')
             emp_image_file_name_in_s3 = "emp_id" + str(emp_id) + "_image_file"
             s3_client.delete_object(Bucket=custombucket, Key = emp_image_file_name_in_s3)

            #Upload image file in s3 #
            s3 = boto3.resource('s3')

            try:
               print("Data inserted in MySQL RDS... uploading image to s3...")
               s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
               bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
               s3_location = (bucket_location['LocationConstraint'])

               if s3_location is None:
                  s3_location = ''
               else:
                  s3_location = '' + s3_location
                      
                  object_url = 
"https://s3{0}.amazonaws.com/{1}{2}".format(s3_location, custombucket, emp_image_file_name_in_s3)
                   except Exception as e:
                   return str(e)
                   
               finally:
                   cursor.close()
                   
               print("all modification done...")
               return render_template('SuccessUpdate.html', name=emp_name,id=emp_id)
               
               else:
                   return render_template('GetEmp.html', AddEmp=AddEmp)
                   
@app.route("/editbenefit-emp", methods=['GET','POST'])
def EditBenefitEmp():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        benefit = request.form['benefit']
        
        update_sql = "UPDATE employee SET benefit= %s WHERE emp_id = %s"
        cursor = db_conn.cursor()
        
        changefield = (benefit,emp_id)
        
        try:
           cursor.execute(update_sql, (changefield))
           db_conn.commit()
           
        finally:
             cursor.close()
             
        print("all modification done...")
        return render_template('SuccessEditBenefit.html')
     else:
        return render_template('GetEmp.html', AddEmp=AddEmp)
        
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=80, debug=True)
        
                  
                                                
  
