from flask import (
    Flask, render_template, request, make_response,flash
)
from flask.wrappers import Response
import pdfkit
import os
from flask.helpers import url_for
import requests
from werkzeug.utils import redirect
from datetime import date,datetime
app = Flask(__name__, static_url_path="")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = "msayak1269"
main='http://127.0.0.1:5001'
api = "http://127.0.0.1:5002/api"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    if request.cookies.get("admin"):
        userEmail = request.cookies.get("admin")
        if userEmail == "admin@gcect.com":
            return redirect(url_for("adminHome"))
    elif request.cookies.get("teacher"):
        return redirect(url_for("teacherHome"))
    elif request.cookies.get('student'):
        return redirect(url_for("studentHome"))
    else:
        return render_template("home.html")



### ADMIN ###

@app.route("/admin/login")
def adminLogin():
    return render_template("login.html", user="Admin", url="admin")


@app.route("/admin/signin", methods=["POST"])
def adminSignin():
    form = request.form
    response = requests.post(f"{api}/admin/signin", data=form)
    resp = response.json()
    if resp["status"] == "ok":
        resp1 = make_response(redirect(url_for("adminHome")))
        resp1.set_cookie("admin", resp["user"]["email"], max_age=60*60*24*365*2)
        return resp1
    else:
        return redirect(url_for("adminLogin"))


@app.route("/admin/home")
def adminHome():
    return render_template("adminhome.html")


@app.route("/admin/result")
def adminResult():
    alldept = ["CSE", "IT", "CT"]
    totalSem = [1, 2, 3, 4, 5, 6, 7, 8]
    return render_template("adminResultForm.html", totalSem=totalSem, alldept=alldept)


@app.route("/admin/getresult", methods=["POST"])
def adminGetResult():
    form = request.form
    response = requests.post(f"{api}/admin/viewresult", data=form)
    resp = response.json()
    dept = resp["dept"]
    sem = resp["sem"]
    subjects = resp["subjects"]
    studentOfDeptSem = resp["student-of-dept-sem"]
    # return resp
    return render_template("adminGetResult.html",sem=sem,dept=dept,subjects=subjects,studentOfDeptSem = studentOfDeptSem)
@app.route("/admin/printresult/<id>")
def adminPrintResult(id):
    response = requests.get(f"{api}/admin/printresult/{id}")
    resp = response.json()
    rendered =  render_template("printResult.html",student = resp)
    pdf =pdfkit.from_string(rendered,False)
    pdfResponse = make_response(pdf)
    pdfResponse.headers['Content-Type'] = "result/pdf"
    pdfResponse.headers['Content-Disposition'] = 'inline;filename = result.pdf'
    return pdfResponse

@app.route("/admin/addstudentform")
def adminAddStudentForm():
    if request.cookies.get("admin"):
        return render_template("adminAddStudent.html")
    else:
        return redirect(url_for("home"))

@app.route("/admin/addstudentsubmit",methods=["POST"])
def adminAddStudentSubmit():
    if request.cookies.get("admin"):
        form = request.form
        response = requests.post(f"{api}/admin/addstudent", data=form)
        resp = response.json()
        if resp["status"]=="ok":
            flash(resp["message"])
            return redirect(url_for("adminHome"))
        else:
            return redirect(url_for("adminAddStudentForm"))
    else:
        return redirect(url_for("home"))

@app.route("/admin/addteacherform")
def adminAddTeacherForm():
    if request.cookies.get("admin"):
        return render_template("adminAddTeacher.html")
    else:
        return redirect(url_for("home"))

@app.route("/admin/addteachersubmit",methods=["POST"])
def adminAddTeacherSubmit():
    if request.cookies.get("admin"):
        form = request.form
        response = requests.post(f"{api}/admin/addteacher", data=form)
        resp = response.json()
        if resp["status"]=="ok":
            return redirect(url_for("adminHome"))
        else:
            return redirect(url_for("adminAddTeacherForm"))
    else:
        return redirect(url_for("home"))

@app.route("/admin/feeform")
def adminFeeCheckForm():
    if request.cookies.get("admin"):
        alldept = ["CSE", "IT", "CT"]
        totalSem = [1, 2, 3, 4, 5, 6, 7, 8]
        return render_template("adminFeeCheckForm.html", totalSem=totalSem, alldept=alldept) 
    else:
        return redirect(url_for("home"))

@app.route("/admin/feestatus",methods=["POST"])
def adminFeeCheckStatus():
    if request.cookies.get("admin"):
        form = request.form
        response = requests.post(f"{api}/admin/checkfeestatus", data=form)
        resp = response.json() 
        dept = resp["dept"]
        sem = resp["sem"]
        studentOfDeptSem = resp["student-of-dept"]
        return render_template("adminGetFeeStatus.html",dept = dept,sem=sem,studentOfDeptSem=studentOfDeptSem)
         

    else:
        return redirect(url_for("home"))

@app.route("/admin/allowforexam/<id>",methods=["GET","POST"])
def adminAllowForExam(id):
    if request.cookies.get("admin"):
        response = requests.post(f"{api}/admin/allowforexam/{id}")
        return redirect(url_for("adminFeeCheckForm"))
    else:
        return redirect(url_for("home"))  

@app.route("/admin/teacheralloteform")
def adminTeacherAlloteForm():
    if request.cookies.get("admin"):
        return render_template("adminTeacherAlloteForm.html")
    else:
        return redirect(url_for("home"))

@app.route("/admin/teacherallote",methods=["POST"])
def adminTeacherAllote():
    if request.cookies.get("admin"):
        form = request.form
        response = requests.post(f"{api}/admin/teacherallotement", data=form)
        resp = response.json() 
        if resp["status"]=="ok":
            return redirect(url_for("home"))
        else:
            return redirect(url_for("adminTeacherAlloteForm"))
        
    else:
        return redirect(url_for("home"))

@app.route("/admin/examscheduleform")
def adminExamScheduleForm():
    if request.cookies.get("admin"):
        return render_template("adminExamScheduleForm.html")
    else:
        return redirect(url_for("home"))

@app.route("/admin/examschedule",methods=["POST"])
def adminExamSchedule():
    if request.cookies.get("admin"):
        form = request.form
        response = requests.post(f"{api}/admin/create/examschedule", data=form)
        resp = response.json() 
        if resp["status"]=="ok":
            return redirect(url_for("home"))
        else:
            return redirect(url_for("adminExamScheduleForm"))        
    else:
        return redirect(url_for("home"))




@app.route("/admin/logout")
def adminLogout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('admin', expires=0)
    return resp



#### TEACHER ###
@app.route("/teacher/login")
def teacherLogin():
    return render_template("login.html", user="Teacher", url="teacher")


@app.route("/teacher/signin", methods=["POST"])
def teacherSignin():
    form = request.form
    response = requests.post(f"{api}/teacher/signin", data=form)
    resp = response.json()
    if resp["status"] == "ok":
        resp1 = make_response(redirect(url_for("teacherHome")))
        resp1.set_cookie("teacher", resp["user"]["email"], max_age=60*60*24*365*2)
        return resp1
    else:
        return redirect(url_for("teacherLogin"))

@app.route("/teacher/home")
def teacherHome():
    if request.cookies.get("teacher"):
        return render_template("teacherHome.html")
    else:
        return redirect(url_for("home"))


@app.route("/teacher/result")
def teacherResult():
    alldept = ["CSE", "IT", "CT"]
    totalSem = [1, 2, 3, 4, 5, 6, 7, 8]
    if request.cookies.get('teacher')!=None:
        subjects=requests.post(f'{api}/teacher/getSubjects',params={'id':request.cookies.get('teacher')}).json()
        if subjects.get('status')=='ok':
            return render_template("teacherResultForm.html", totalSem=totalSem, alldept=alldept,subjects=subjects['subjects'])
        else:
            return render_template("error.html",message=subjects['message'],errorAt='/teacher/result',returnto='/teacher/result')
    else:
        return redirect(url_for(teacherSignin))


@app.route("/teacher/getresult", methods=["POST"])
def teacherGetResult():
    form = request.form
    tid=request.cookies.get('teacher')
    if tid!=None:
        response = requests.post(f"{api}/teacher/viewresult/{tid}", data=form).json()
        if response['status']=='ok':
            dept = response["dept"]
            sem = response["sem"]
            subject = form.get('subject')
            studentOfDeptSem = response["student-of-dept-sem"]
            # return resp
            return render_template("teacherGetResult.html",sem=sem,dept=dept,subject=subject,studentOfDeptSem = studentOfDeptSem)
        else:
            return render_template("error.html",message=response['message'],errorAt='/teacher/result',returnto='teacher/result')
    else:
        return redirect(url_for(teacherSignin))

@app.route("/teacher/addmarksform")
def addMarksForm():
    alldept = ["CSE", "IT", "CT"]
    totalSem = [1, 2, 3, 4, 5, 6, 7, 8]
    if request.cookies.get('teacher')!=None:
        subjects=requests.post(f'{api}/teacher/getSubjects',params={'id':request.cookies.get('teacher')}).json()
        if subjects.get('status')=='ok':
            return render_template("teacherAddMarksForm.html",link='/teacher/addMarks' ,message="Add Marks", totalSem=totalSem, alldept=alldept,subjects=subjects['subjects'])
        else:
            return render_template("error.html",message=subjects['message'],errorAt='/teacher/addmarksform')
    else:
        return redirect(url_for(teacherSignin))

@app.route('/teacher/addMarks',methods=["POST"])
def addMarks():
    if request.cookies.get('teacher')!=None:
        form=request.form

        students=requests.post(f'{api}/teacher/addMarks',data=form).json()
        if students.get('status')=='ok':
            print(students)
            return render_template("teacherAddMarks.html", dept=students['dept'],sem=students['sem'],subject=students['subject'],studentOfDeptSem = students['student-of-dept-sem'])
        else:
            return render_template("error.html",message=students['message'],errorAt='/teacher/addMarks',returnto='/teacher/addmarksform')
    else:
        return redirect(url_for(teacherSignin))
@app.route('/teacher/addmarks/<studentid>/<dept>/<sem>/<subject>',methods=['POST'])
def addMarksArg(studentid,dept,sem,subject):
    form=request.form
    try:
        marks=int(form.get('marks'))
        if marks<0 or marks>100:
            return render_template("error.html",message='Marks cannot be less than 0 or greater than 100',errorAt='/teacher/addmarksform')
    except Exception:
        return render_template("error.html",message='Marks cannot be string',errorAt='/teacher/addmarksform')
    response=requests.post(f'{api}/teacher/addMarks/{studentid}/{dept}/{sem}/{subject}',data=form).json()
    if response['status']=='ok':
        form={'dept':dept,'sem':sem,'subject':subject}
        students=requests.post(f'{api}/teacher/addMarks',data=form).json()
        return render_template("teacherAddMarks.html", dept=students['dept'],sem=students['sem'],subject=students['subject'],studentOfDeptSem = students['student-of-dept-sem'])
    else:
        return render_template("error.html",message=response['message'],errorAt='/teacher/addMarks',returnto='/teacher/addMarks')

@app.route('/teacher/addlinkform')
def addlinkform():
    alldept = ["CSE", "IT", "CT"]
    totalSem = [1, 2, 3, 4, 5, 6, 7, 8]
    if request.cookies.get('teacher')!=None:
        subjects=requests.post(f'{api}/teacher/getSubjects',params={'id':request.cookies.get('teacher')}).json()
        if subjects.get('status')=='ok':
            return render_template("teacherAddMarksForm.html",link='/teacher/addLink' ,message="Add Link", totalSem=totalSem, alldept=alldept,subjects=subjects['subjects'])
        else:
            return render_template("error.html",message=subjects['message'],errorAt='/teacher/addmarksform',returnto='/teacher/addmarksform')
    else:
        return redirect(url_for(teacherSignin))
@app.route('/teacher/addLink',methods=['POST'])
def addlink():
    if request.cookies.get('teacher')!=None :
        form=request.form
        resp=requests.post(f'{api}/teacher/addLink',data=form).json()
        if resp.get('status')=='ok':
            link=resp.get('link')
            return render_template("teacherAddLinkForm.html",link=link, dept=resp['dept'],sem=resp['sem'],subject=resp['subject'])
        else:
            return render_template("error.html",message=resp['message'],errorAt='/teacher/addlinkform',returnto='/teacher/addlinkform')
    elif  request.args.get('id')!=None:
        form=request.form 
        link=form.get('link')
        dept=form.get('dept')
        sem=form.get('sem')
        subject=form.get('subject')
        return render_template("teacherAddLinkForm.html",link=link, dept=dept,sem=sem,subject=subject)
    else:
        return redirect(url_for(teacherSignin))
@app.route('/teacher/linktobeadded/<dept>/<sem>/<subject>',methods=['POST'])
def linktobeadded(dept,sem,subject):
    if request.cookies.get('teacher')!=None:
        form=request.form
        resp=requests.post(f'{api}/teacher/linktobeadded/{dept}/{sem}/{subject}',data=form).json()
        if resp.get('status')=='ok':
            link=resp.get('link')
            form={'dept':dept,'sem':sem,'subject':subject,'link':link}
            rsp=requests.post(f'{main}/teacher/addLink',data=form,params={'id':'secretide'})
            return rsp.content
        else:
            return render_template("error.html",message=resp['message'],errorAt=f'/teacher/linktobeadded/{dept}/{sem}/{subject}',returnto='/teacher/addlinkform')
    else:
        return redirect(url_for(teacherSignin))
@app.route('/teacher/profile')
def profile():
    if request.cookies.get("teacher"):
        id=request.cookies.get('teacher')
        response=requests.post(f'{api}/teacher/profile/{id}').json()
        if response['status'] =='ok':
            return render_template("teacherProfile.html",teacher=response['teacher'],len=len(response['teacher']['subject']),home='/teacher/home')
        else:
            return render_template("error.html",message=response['message'],errorAt='/teacher/profile',returnto='/teacher/home')
    else:
        return redirect(url_for("home"))
@app.route("/teacher/logout")
def teacherLogout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('teacher', expires=0)
    return resp
### STUDENT ####
@app.route("/student/login")
def studentLogin():
    return render_template("login.html", user="Student", url="student")
@app.route("/student/signin", methods=["POST"])
def studentSignin():
    form = request.form
    response = requests.post(f"{api}/student/signin", data=form)
    resp = response.json()
    if resp["status"] == "ok":
        resp1 = make_response(redirect(url_for("studentHome")))
        resp1.set_cookie("student", resp["user"]["email"], max_age=60*60*24*365*2)
        return resp1
    else:
        return redirect(url_for("stdudentLogin"))

@app.route("/student/home")
def studentHome():
    if request.cookies.get("student"):
        return render_template("studentHome.html")
    else:
        return redirect(url_for("home"))
@app.route('/student/profile')
def studentprofile():
    if request.cookies.get("student"):
        id=request.cookies.get('student')
        response=requests.post(f'{api}/student/profile/{id}').json()
        if response['status'] =='ok':
            return render_template("studentProfile.html",student=response,home='/student/home')
        else:
            return render_template("error.html",message=response['message'],errorAt='/student/profile',returnto='/student/home')
    else:
        return redirect(url_for("home"))
@app.route("/student/logout")
def studentLogout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('student', expires=0)
    return resp

@app.route("/student/result", methods=["GET","POST"])
def studentGetResult():
    tid=request.cookies.get('student')
    if tid!=None:
        response = requests.post(f"{api}/student/viewresult/{tid}").json()
        if 'percentage' in response:
            dept = response["dept"]
            sem = response["sem"]
            subject = response.get('subject')
            # return resp
            return render_template("studentResult.html",sem=sem,dept=dept,subjects=response['subject-wise-marks'],student=response)
        else:
            return render_template("error.html",message='cannot access result at the moment',errorAt='/student/result',returnto='student/home')
    else:
        return redirect(url_for(teacherSignin))

@app.route('/student/gettrxid',methods=['GET','POST'])
def gettrx():
    if request.cookies.get('student')!=None :
        id=request.cookies.get('student')
        resp=requests.post(f'{api}/student/gettrxid/{id}').json()
        if resp.get('status')=='ok':
            trxid=resp.get('trx-id')
            return render_template("studentgettrx.html",trxid=trxid, student=resp,len=len(trxid))
        else:
            return render_template("error.html",message=resp['message'],errorAt='/student/addtrxid',returnto='/student/home')
    elif  request.args.get('id')!=None:
        trxid=request.args.get('id')
        student=request.form 
        return render_template("studentgettrx.html",trxid=trxid, student=student,len=len(trxid))
    else:
        return redirect(url_for(studentSignin))
@app.route('/student/addtrxid',methods=["POST"])
def addtrxid():
    if request.cookies.get('student')!=None:
        id=request.cookies.get('student')
        form=request.form
        trxid=form.get('trxid')
        if len(trxid)<12:
            return render_template('error.html',message='The length of transaction id must be greater than equal to 12 ',errorAt='/student/addtrxid',returnto='/student/gettrxid')
        resp=requests.post(f'{api}/student/addtrxid/{id}',data=form).json()
        if resp.get('status')=='ok':
            trxid=resp.get('trxid')
            student=resp
            rsp=requests.post(f'{main}/student/gettrxid',data=student,params={'id':trxid})
            return rsp.content
        else:
            return render_template("error.html",message=resp['message'],errorAt='/student/addtrxid',returnto='/student/gettrxid')
    else:
        return redirect(url_for(studentSignin))
@app.route('/student/giveExam')
def giveExam():
    if request.cookies.get('student')!=None:
        id=request.cookies.get('student')
        resp=requests.post(f'{api}/student/gettrxid/{id}').json()
        if resp.get('status')=='ok':
            trxid=resp.get('trx-id')
            if len(trxid)<12:
                return render_template("error.html",message='Transaction Id not submitted',errorAt='/student/giveExam',returnto='/student/home')
            else:
                return render_template("studentexam.html")
        else:
            return render_template("error.html",message=resp['message'],errorAt='/student/gettrxid',returnto='/student/home')
    else:
        return redirect(url_for(studentSignin))
@app.route('/student/getexamlinks',methods=['POST'])
def giveexamlink():
    if request.cookies.get('student')!=None:
        id=request.cookies.get('student')
        form=request.form 
        resp=requests.post(f'{api}/student/getexam/{id}',data=form).json()
        if resp.get('status')=='ok':
            today = date.today()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            hr=current_time.index(':')
            min=current_time.rindex(':')
            current={
                'year':int(today.year),
                'month':int(today.month),
                'day':int(today.day),
                'hr':int(current_time[:hr]),
                'min':int(current_time[hr+1:min])
            }
            ind=resp['datetime'].index('T')
            date1=resp['datetime'][:ind]
            time=resp['datetime'][ind+1:]
            ld=date1.index('-')
            rd=date1.rindex('-')
            lt=time.index(':')
            scheduled={
                'year':int(date1[:ld]),
                'month':int(date1[ld+1:rd]),
                'day':int(date1[rd+1:]),
                'hr':int(time[:lt]),
                'min':int(int(time[lt+1:])-2)
            }
            return render_template("studentexamlink.html",current=current,scheduled=scheduled,url=resp['url'],dept=resp['dept'],sem=resp['sem'],subject=resp['subject'])
        else:
            return render_template("error.html",message=resp['message'],errorAt='/student/getexamlink',returnto='/student/giveExam')
    else:
        return redirect(url_for(studentSignin))
if __name__ == "__main__":
    app.run(port=5001, debug=True, host='0.0.0.0')
