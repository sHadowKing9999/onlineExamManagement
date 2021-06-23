import json
import uuid
import copy

def checkCredentials(APP_ROOT,form):
    email=form.get('email')
    password=form.get('password')
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        studentDetails = json.load(json_file)
    studentDetailsBackup = copy.deepcopy(studentDetails)
    try:
        for student in studentDetails:
            if student['email']==email and student["password"] == password:
                resp = {
                    "status":"ok",
                    "message":"Signin Success",
                    "user":{
                        "email":email,
                        "name": student["name"]
                    }
                }
            return resp
        else:
            resp = {
            "status":"not-ok",
            "message":"Invalid Credentials!"
            }
            return resp
    except Exception:
        with open(f"{APP_ROOT}/db/student1.json","w") as json_file:
            json_file.seek(0)
            json.dump(studentDetailsBackup,json_file,indent=2)
        resp = {
            "status":"not-ok",
            "message":"Student Signin Failed!"
        }
        return resp

def profile(APP_ROOT,tid):
    try:
        with open(f"{APP_ROOT}/db/student1.json","r") as json_file:
            students = json.load(json_file)
        for student in students:
            if student['email']==tid:
                return {
                'status':'ok',
                'name':student['name'],
                'email':tid,
                'academic-year':student['academic-year'],
                'sem':student['sem'],
                'roll':student['roll'],
                'fee':student['fee'],
                'reg':student['reg'],
                'message':'success'
            }
            else:
                return {
                'status':'not-ok',
                'message':f'Teacher with email {tid} not found in db'
            }
    except Exception:
        return {
            "status":"not-ok",
            "message":"Cannot fetch data from the database!"
        }
def result(APP_ROOT,id):
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        allStudent = json.load(json_file)
    for student in allStudent:
        if student["email"] == id:
            dept = student["dept"]
            sem = student["sem"]
            stdnt = student
            break
    with open(f"{APP_ROOT}/db/subjects.json", "r") as json_file:
        allSubject = json.load(json_file)
    subject = allSubject[dept][sem]
    stdnt["subject"] = subject
    subjectWiseMarks = {}
    n = len(subject)
    totalMarks = 0
    count=0
    for i in range(n):
        subjectWiseMarks[subject[i]] = stdnt["marks"][i]
        if stdnt['marks'][i]!=-1:
            count+=1
            totalMarks += stdnt["marks"][i]
        
    stdnt["subject-wise-marks"] = subjectWiseMarks
    stdnt["total-marks"] = totalMarks
    stdnt['count']=count
    total = 100*count
    stdnt["percentage"] = round(((totalMarks/total)*100), 2)
    return stdnt
def trxid(APP_ROOT,id):
    try:
        with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
            allStudent = json.load(json_file)
        for student in allStudent:
            if student["email"] == id:
                return {
                    'status':'ok',
                    'trx-id':student['transactionId'],
                    'dept':student['dept'],
                    'sem':student['sem'],
                    'roll':student['roll'],
                    'name':student['name'],
                    'reg':student['reg'],
                    'fee':student['fee'],
                    'academic-year':student['academic-year']
                }
        return {'status':'not-ok','message':f'cannot fetch transaction id of {id}'}
    except Exception:
        return {'status':'not-ok','message':'an unhandled exception has occured'}
def addtrxid(APP_ROOT,id,form):
    trx_id=form.get('trxid')
    try:
        with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
            student = json.load(json_file)
        sid=-1
        print(-1)
        for i in range(len(student)):
            if student[i]["email"] == id:
                sid=i
                break
        print(0)
        if sid==-1 or sid>len(student):
            return {'status':'not-ok','message':f'cannot fetch transaction id of {id}'}
        student[sid]['transactionId']=trx_id
        print(student[sid]['transactionId'])
        with open(f"{APP_ROOT}/db/student1.json",'w') as json_file:
            json_file.seek(0)
            json.dump(student,json_file,indent=2)
        print(1)
        return {
            'status':'ok',
            'trxid':trx_id,
            'name':student[sid]['name'],
            'academic-year':student[sid]['academic-year'],
            'fee':student[sid]['fee'],
            'dept':student[sid]['dept'],
            'roll':student[sid]['roll'],
            'reg':student[sid]['reg']
        }
    except Exception:
        return {'status':'not-ok','message':'an unhandled exception has occured'}
def getexam(APP_ROOT,id,form):
    datetime=form.get('date-time')
    hr=datetime.index('T')
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        allStudent = json.load(json_file)
    for student in allStudent:
        if student["email"] == id:
            dept = student["dept"]
            sem = student["sem"]
            break
    with open(f"{APP_ROOT}/db/routine.json", "r") as json_file:
        routine = json.load(json_file)
    sub=''
    for exam in routine:
        if sem==exam['sem'] and dept==exam['dept'] and datetime==exam['date-time']:
            sub=exam['subject']
    if sub=='':
        return {
            'status':'not-ok',
            'message':f'No exam scheduled for time {datetime[hr+1:]} (24h format) and date {datetime[:hr]} (YYYY-MM-DD) for {dept}/{sem}'
        }
    with open(f"{APP_ROOT}/db/links.json", "r") as json_file:
        links = json.load(json_file)
    url=''
    for link in links:
        if sem==link['sem'] and dept==link['dept'] and sub==link['subject']:
            url=link['url']
    if url=='':
        return {
            'status':'not-ok',
            'message':f'Exam is scheduled for {dept}/{sem} of {sub} but no exam link added yet'
        }
    else:
        return {
            'status':'ok',
            'url':url,
            'datetime':datetime,
            'sem':sem,
            'dept':dept,
            'subject':sub
    }