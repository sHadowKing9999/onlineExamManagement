import json
import uuid
import copy


def checkCredential(APP_ROOT, form):
    email = form.get("email")
    password = form.get("password")
    with open(f"{APP_ROOT}/db/teacherdetails.json", "r") as json_file:
        teacherDetails = json.load(json_file)
    teacherDetailsBackup = copy.deepcopy(teacherDetails)
    try:
        if email in teacherDetails.keys() and teacherDetails[email]["password"] == password:
            resp = {
                "status":"ok",
                "message":"Signin Success",
                "user":{
                    "email":email,
                    "name":teacherDetails[email]["name"]
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
        with open(f"{APP_ROOT}/db/teacherdetails.json","w") as json_file:
            json_file.seek(0)
            json.dump(teacherDetailsBackup,json_file,indent=2)
        resp = {
            "status":"not-ok",
            "message":"Teacher Signin Failed!"
        }
        return resp
def subjects(APP_ROOT,id):
    with open(f"{APP_ROOT}/db/teacherdetails.json", "r") as json_file:
        teacherDetails = json.load(json_file)
    if id in teacherDetails:
        return {
            'status':'ok',
            'subjects':teacherDetails[id].get('subject')
        }
    else:
        return {
            'status':'not ok',
            'message':'You do not have authorization to view result of any subject '
        }
def showResult(APP_ROOT,form,tid):
    sub=form.get("subject")
    dept=form.get("dept")
    sem=form.get("sem")


    with open(f"{APP_ROOT}/db/teacherdetails.json","r") as json_file:
        teacher = json.load(json_file)
        teacherBackup=copy.deepcopy(teacher)
    try:
            with open(f"{APP_ROOT}/db/student1.json","r") as json_file:
                allStudent= json.load(json_file)
            with open(f"{APP_ROOT}/db/subjects.json","r") as json_file:
                allSubject = json.load(json_file)
            subjects = allSubject[dept][sem]
            sid=-1
            for index in range(len(subjects)):
                if subjects[index]==sub:
                    sid=index
                    break
            if sid==-1:
                return {
                    'status':'not-ok',
                    'message':f'This subject is not present in  semester {sem} for {dept} department'
                }
            studentOfDeptSem=[]
            for student in allStudent:
                if student["dept"]==dept and student["sem"]==sem:
                    studentToBeAdded = {
                        "email":student["email"],
                        "id":student["id"],
                        "marks":student["marks"][sid],
                        "name":student["name"],
                        "status":student["status"],
                        "roll":student['roll']
                    }
                    studentOfDeptSem.append(studentToBeAdded)
            sorted_student=sorted(studentOfDeptSem,key=lambda x:x['roll'])
            return {
                "status":"ok",
                "dept":dept,
                "sem":sem,
                "subjects":subjects,
                "student-of-dept-sem":sorted_student,
                "message":"success"
            }
    except Exception:
        with open(f"{APP_ROOT}/db/admin.json","w") as json_file:
            json_file.seek(0)
            json.dump(teacherBackup,json_file,indent=2)
        resp = {
            "status":"not-ok",
            "message":"Cannot fetch data from the database!"
        }
        return resp
def addMarks(APP_ROOT,form):
    sub=form.get("subject")
    dept=form.get("dept")
    sem=form.get("sem")


    with open(f"{APP_ROOT}/db/teacherdetails.json","r") as json_file:
        teacher = json.load(json_file)
        teacherBackup=copy.deepcopy(teacher)
    try:
            with open(f"{APP_ROOT}/db/student1.json","r") as json_file:
                allStudent= json.load(json_file)
            with open(f"{APP_ROOT}/db/subjects.json","r") as json_file:
                allSubject = json.load(json_file)
            subjects = allSubject[dept][sem]
            sid=-1
            for index in range(len(subjects)):
                if subjects[index]==sub:
                    sid=index
                    break
            if sid==-1:
                return {
                    'status':'not-ok',
                    'message':f'This subject is not present in  semester {sem} for {dept} department'
                }
            studentOfDeptSem=[]
            for student in allStudent:
                if student["dept"]==dept and student["sem"]==sem:
                    studentToBeAdded = {
                        "id":student["id"],
                        "marks":student["marks"][sid],
                        "name":student["name"],
                        "roll":student['roll']
                    }
                    studentOfDeptSem.append(studentToBeAdded)
            sorted_student=sorted(studentOfDeptSem,key=lambda x:x['roll'])
            return {
                "status":"ok",
                "dept":dept,
                "sem":sem,
                "subject":sub,
                "student-of-dept-sem":sorted_student,
                "message":"success"
            }
    except Exception:
        with open(f"{APP_ROOT}/db/admin.json","w") as json_file:
            json_file.seek(0)
            json.dump(teacherBackup,json_file,indent=2)
        resp = {
            "status":"not-ok",
            "message":"Cannot fetch data from the database!"
        }
def addMarksArg(APP_ROOT,form,id,dept,sem,sub):
    with open(f"{APP_ROOT}/db/student1.json","r") as json_file:
        allStudent= json.load(json_file)
    with open(f"{APP_ROOT}/db/subjects.json","r") as json_file:
        allSubject = json.load(json_file)
    with open(f"{APP_ROOT}/db/teacherdetails.json","r") as json_file:
        teacher = json.load(json_file)
    marks=form.get('marks')



    try:
        subjects = allSubject[dept][sem]
        sid=-1
        for index in range(len(subjects)):
            if subjects[index]==sub:
                sid=index
                break
        if sid==-1:
            return {
                'status':'not-ok',
                'message':f'this subject is not present in {sem} semester for {dept} department. You cannot add marks'
            }
        studid=-1
        for index in range(len(allStudent)):
            if allStudent[index]['id']==id:
                studid=index
                break
        allStudent[index]['marks'][sid]=int(marks)
        print(allStudent[index]['marks'][sid])
        with open(f"{APP_ROOT}/db/student1.json","w") as json_file:
            json_file.seek(0)
            json.dump(allStudent,json_file,indent=2)
        return {
            'status':'ok',
            'message':'Updated successfully'
        }
    except Exception:
        resp = {
           "status":"not-ok",
            "message":"Cannot update marks to the database! Check the student id provided or server error!"
        }
        return resp

def addlink(APP_ROOT,form):
    
    try:
        #print(0)
        sub=form.get("subject")
        dept=form.get("dept")
        sem=form.get("sem")
        #print('1')
        with open(f"{APP_ROOT}/db/subjects.json","r") as json_file:
            allSubject = json.load(json_file)
        subjects = allSubject[dept][sem]
        sid=-1
        for index in range(len(subjects)):
            if subjects[index]==sub:
                sid=index
                break
        if sid==-1:
            return {
                'status':'not-ok',
                'message':f'This subject is not present in  semester {sem} for {dept} department'
            }
        #print('2')
        with open(f"{APP_ROOT}/db/routine.json","r") as json_file:
                routines= json.load(json_file)
        rid=-1
        #print(routines)
        for index in range(len(routines)):
            if routines[index]['subject']==sub and routines[index]['dept']==dept and routines[index]['sem']==sem :
                rid=index
                break
        if rid==-1:
            return {
                'status':'not-ok',
                'message':f'The exam for this subject is not yet scheduled for semester {sem} of {dept} department'
            }
        with open(f"{APP_ROOT}/db/links.json",'r') as file:
            file_data = json.load(file)
        print(file_data)
        for i in range(len(file_data)):
            if file_data[i]['dept']==dept and file_data[i]['sem']==sem and file_data[i]['subject']==sub:
                if file_data[i].get('url')!=None:
                    #print('3')
                    return {
                        "status":"ok",
                        "dept":dept,
                        "sem":sem,
                        "subject":sub,
                        'link':file_data[i]['url']
                    }
        return {
            "status":"ok",
            "dept":dept,
            "sem":sem,
            "subject":sub,
            "link":''
        }
    except Exception:
        resp = {
            "status":"not-ok",
            "message":"Cannot fetch data from the database!"
        }
        return resp
def linktobeadded(APP_ROOT,form,dept,sem,subject):
    try:
        link=form.get('link')
        with open(f"{APP_ROOT}/db/links.json",'r') as json_file:
            file_data = json.load(json_file)
        #print(file_data)
        linkId=-1
        for i in range(len(file_data)):
            if file_data[i]['dept']==dept and file_data[i]['sem']==sem and file_data[i]['subject']==subject:
                file_data[i]['url']=link
                linkId=i
                break
        #print(linkId)
        if linkId==-1:
            newdata={
                'id':str(uuid.uuid4()),
                'subject':subject,
                'dept':dept,
                'url':link,
                'sem':sem
            }
            if(len(file_data)==0):
                file_data=[]
            print(5)
            file_data.append(newdata)
            print(file_data)
            with open(f"{APP_ROOT}/db/links.json",'w') as json_file:
                json_file.seek(0)
                json.dump(file_data, json_file, indent = 2)
            print(3)
            return {
                "status":"ok",
                "dept":dept,
                "sem":sem,
                "subject":subject,
                "message":"success",
                'link':newdata['url']
            }
        else:
            with open(f"{APP_ROOT}/db/links.json",'w') as json_file:
                    json_file.seek(0)
                    json.dump(file_data,json_file,indent=2)
            return {
            "status":"ok",
            "dept":dept,
            "sem":sem,
            "subject":subject,
            "message":"success",
            'link':file_data[i]['url']
                }
        #print(4)
    except Exception:
        resp = {
            "status":"not-ok",
            "message":"Cannot fetch data from the database!"
        }
        return resp
def profile(APP_ROOT,tid):
    try:
        with open(f"{APP_ROOT}/db/teacherdetails.json","r") as json_file:
            teacher = json.load(json_file)
        if tid in teacher:
            return {
                'status':'ok',
                'teacher':teacher[tid],
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
