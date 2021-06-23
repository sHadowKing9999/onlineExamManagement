from flask import (
    Flask,request, jsonify,render_template
)
import os
from db import adminManager, teacherManager, studentManager

app = Flask(__name__,static_url_path="")
app.secret_key='y63le54ck45tt76ye54cr64mc25ze54cs63la16qs63li36ks63li36kh27bt76y'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template("404.html")

#####  Admin Section #####
@app.route("/api/admin/signin",methods=["POST"])
def adminSignin():
    form = request.form
    resp = adminManager.checkAdminCredentials(APP_ROOT,form)
    return jsonify(resp)

@app.route("/api/admin/create/examschedule",methods=["POST"])
def examSchedule():
    form = request.form
    resp = adminManager.setExamSchedule(APP_ROOT,form)
    return jsonify(resp)

@app.route("/api/admin/viewresult",methods=["POST"])
def viewResult():
    form = request.form
    resp = adminManager.viewResult(APP_ROOT,form)
    return jsonify(resp)
@app.route("/api/admin/printresult/<id>")
def printResult(id):
    resp = adminManager.printResult(APP_ROOT,id)
    return jsonify(resp)

@app.route("/api/admin/addteacher",methods=["POST"])
def addTeacher():
    form = request.form
    resp = adminManager.addTeacher(APP_ROOT,form)
    return jsonify(resp)

@app.route("/api/admin/teacherallotement",methods=["POST"])
def teacherAllotement():
    form = request.form
    resp = adminManager.teacherAllotement(APP_ROOT,form)
    return jsonify(resp)

@app.route("/api/admin/addstudent",methods=["POST"])
def addStudent():
    form = request.form
    resp = adminManager.addStudent(APP_ROOT,form)
    return jsonify(resp)

@app.route("/api/admin/allowforexam/<id>",methods=["POST"])
def allowForExam(id):
    resp = adminManager.allowStudentForExam(APP_ROOT,id)
    print(resp)
    return jsonify(resp)
@app.route("/api/admin/checkfeestatus",methods = ["POST"])
def checkFeeStatus():
    form = request.form
    resp = adminManager.checkFeeStatus(APP_ROOT,form)
    return jsonify(resp)






#####  Teacher Section #####
@app.route("/api/teacher/signin",methods=["POST"])
def teacherSignin():
    form = request.form
    resp = teacherManager.checkCredential(APP_ROOT,form)
    return jsonify(resp)
@app.route("/api/teacher/getSubjects",methods=["POST"])
def getSubjects():
    id=request.args.get('id')
    resp=teacherManager.subjects(APP_ROOT,id)
    return jsonify(resp)
@app.route('/api/teacher/viewresult/<teacherID>',methods=["POST"])
def getResult(teacherID):
    form=request.form
    resp=teacherManager.showResult(APP_ROOT,form,teacherID)
    return jsonify(resp)
@app.route("/api/teacher/setquestion/<teacheremail>",methods=["POST"])
def setQuestion(tid):
    form = request.form
    resp = teacherManager.setQuestion(APP_ROOT,form,tid)
    return jsonify(resp)

@app.route("/api/teacher/addMarks",methods=["POST"])
def addMarks():
    form=request.form 
    resp=teacherManager.addMarks(APP_ROOT,form)
    return jsonify(resp)

@app.route("/api/teacher/addMarks/<studentid>/<dept>/<sem>/<subject>",methods=["POST"])
def addMarksArg(studentid,dept,sem,subject):
    form=request.form 
    resp=teacherManager.addMarksArg(APP_ROOT,form,studentid,dept,sem,subject)
    return jsonify(resp)

@app.route("/api/teacher/addLink",methods=["POST"])
def addlink():
    form=request.form 
    resp=teacherManager.addlink(APP_ROOT,form)
    return jsonify(resp)
@app.route("/api/teacher/linktobeadded/<dept>/<sem>/<subject>",methods=["POST"])
def linktobeadded(dept,sem,subject):
    form=request.form 
    #print(form)
    resp=teacherManager.linktobeadded(APP_ROOT,form,dept,sem,subject)
    
    return jsonify(resp)
@app.route("/api/teacher/profile/<tid>",methods=["POST"])
def teacherprofile(tid):
    resp=teacherManager.profile(APP_ROOT,tid)
    return jsonify(resp)
#####  Student Section #####

@app.route("/api/student/signin",methods=["POST"])
def studentSignin():
    form = request.form
    resp = studentManager.checkCredentials(APP_ROOT,form)
    return jsonify(resp)
@app.route('/api/student/profile/<id>',methods=['POST'])
def studentprofile(id):
    resp = studentManager.profile(APP_ROOT,id)
    return jsonify(resp)
@app.route('/api/student/viewresult/<id>',methods=['POST'])
def studentresult(id):
    resp = studentManager.result(APP_ROOT,id)
    return jsonify(resp)
@app.route('/api/student/gettrxid/<id>',methods=["POST"])
def gettrxid(id):
    resp = studentManager.trxid(APP_ROOT,id)
    return jsonify(resp)
@app.route('/api/student/addtrxid/<id>',methods=["POST"])
def addtrxid(id):
    form=request.form 
    resp=studentManager.addtrxid(APP_ROOT,id,form)
    return jsonify(resp)
@app.route('/api/student/getexam/<id>',methods=['POST'])
def getexam(id):
    form=request.form
    resp=studentManager.getexam(APP_ROOT,id,form)
    return jsonify(resp)
if __name__=="__main__":
    app.run(port=5002,debug=True,host='0.0.0.0')