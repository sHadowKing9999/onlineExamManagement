import json
import uuid
import copy


def checkAdminCredentials(APP_ROOT, form):
    email = form.get("email")
    password = form.get("password")
    with open(f"{APP_ROOT}/db/admin.json", "r") as json_file:
        adminDetails = json.load(json_file)
    adminDetailsBackup = copy.deepcopy(adminDetails)
    try:
        if adminDetails["email"] == email and adminDetails["password"] == password:
            resp = {
                "status": "ok",
                "message": "Signin Success",
                "user": adminDetails
            }
            return resp

        else:
            resp = {
                "status": "not-ok",
                "message": "Invalid Credentials!"
            }
            return resp
    except Exception:
        with open(f"{APP_ROOT}/db/admin.json", "w") as json_file:
            json_file.seek(0)
            json.dump(adminDetailsBackup, json_file, indent=2)
        resp = {
            "status": "not-ok",
            "message": "Admin Signin Failed!"
        }
        return resp


def setExamSchedule(APP_ROOT, form):
    dept = form.get("dept")
    sem = form.get("sem")
    subject = form.get("subject")
    dateTime = form.get("datetime")
    with open(f"{APP_ROOT}/db/routine.json", "r") as json_file:
        routines = json.load(json_file)
    routineBackup = copy.deepcopy(routines)
    try:
        routineToBeAdded = {
            "id": str(uuid.uuid4()),
            "dept": dept,
            "sem": sem,
            "subject": subject,
            "date-time": dateTime,
        }
        routines.insert(0, routineToBeAdded)
        with open(f"{APP_ROOT}/db/routine.json", "w") as json_file:
            json_file.seek(0)
            json.dump(routines, json_file, indent=2)
        resp = {
            "status": "ok",
            "message": "exam schedule added successfully",
            "routine": routineToBeAdded
        }
        return resp

    except Exception:
        with open(f"{APP_ROOT}/db/routine.json", "w") as json_file:
            json_file.seek(0)
            json.dump(routineBackup, json_file, indent=2)
        resp = {
            "status": "not-ok",
            "message": "exam schedule creation failed"
        }
        return resp


def viewResult(APP_ROOT, form):
    dept = form.get("dept")
    sem = form.get("sem")
    with open(f"{APP_ROOT}/db/subjects.json", "r") as json_file:
        allSubject = json.load(json_file)
    subjects = allSubject[dept][sem]
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        allStudent = json.load(json_file)
    studentOfDeptSem = []
    try:
        for student in allStudent:
            if student["dept"] == dept and student["sem"] == sem:
                studentToBeAdded = {
                    "email": student["email"],
                    "id": student["id"],
                    "marks": student["marks"],
                    "name": student["name"],
                    "status": student["status"],
                    "dept": student["dept"],
                    "sem": student["sem"]
                }
                studentOfDeptSem.append(studentToBeAdded)
        resp = {
            "status": "ok",
            "dept": dept,
            "sem": sem,
            "subjects": subjects,
            "student-of-dept-sem": studentOfDeptSem,
            "message": "success"
        }
    except Exception:
        resp = {
            "status": "not-ok",
            "message": "exception"
        }
    return resp


def printResult(APP_ROOT, id):
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        allStudent = json.load(json_file)
    for student in allStudent:
        if student["id"] == id:
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
    for i in range(n):
        subjectWiseMarks[subject[i]] = stdnt["marks"][i]
        totalMarks += stdnt["marks"][i]
    stdnt["subject-wise-marks"] = subjectWiseMarks
    stdnt["total-marks"] = totalMarks
    total = 60
    stdnt["percentage"] = round(((totalMarks/total)*100), 2)
    if stdnt["percentage"] >= 50.0:
        stdnt["result-status"] = "P"
    else:
        stdnt["result-status"] = "F"
    return stdnt


def teacherAllotement(APP_ROOT, form):
    teacherEmail = form.get("email")
    dept = form.get("dept")
    sem = form.get("sem")
    subject = form.get("subject")
    with open(f"{APP_ROOT}/db/teachersallotement.json", "r") as json_file:
        teachersallotement = json.load(json_file)
    # return teacherAllotement
    teachersallotementBackup = copy.deepcopy(teacherAllotement)
    with open(f"{APP_ROOT}/db/subjects.json", "r") as json_file:
        allSubject = json.load(json_file)
    try:
        if subject in allSubject[dept][sem]:
            flag = 1
            for allotement in teachersallotement:
                if allotement["teacher-email"] != teacherEmail and allotement["dept"] == dept and allotement["sem"] == sem and allotement["subject"] == subject:
                    flag = 0
                    allotement["teacher-email"] = teacherEmail
                    break
            if flag:
                newAllotement = {
                    "id": str(uuid.uuid4()),
                    "teacher-email": teacherEmail,
                    "dept": dept,
                    "sem": sem,
                    "subject": [subject]
                }
                teachersallotement.append(newAllotement)
            with open(f"{APP_ROOT}/db/teachersallotement.json", "w") as json_file:
                json_file.seek(0)
                json.dump(teachersallotement, json_file, indent=2)
            resp = {
                "status": "ok",
                "messege": "added"
            }
        else:
            resp = {
                "status": "not-ok",
                "messege": "subject-error"
            }
    except Exception:
        with open(f"{APP_ROOT}/db/teachersallotement.json", "w") as json_file:
            json_file.seek(0)
            json.dump(teachersallotementBackup, json_file, indent=2)
        resp = {
            "status": "not-ok",
            "messege": "exception"
        }
    return resp


def addTeacher(APP_ROOT, form):
    name = form.get("name")
    email = form.get("email")
    dept = form.get("dept")
    subject = form.get("subject")
    dob = form.get("dob")
    try:
        with open(f"{APP_ROOT}/db/teacherdetails.json", "r") as json_file:
            teacherDetail = json.load(json_file)
        teacherDetailBackup = copy.deepcopy(teacherDetail)
        sublist=[]
        sublist.append(subject)
        if email in teacherDetail.keys():
            resp = {
                "status": "not-ok",
                "message": "teacher-already-present"
            }
        
        else:
            teacherDetail[email] = {
                "name": name,
                "dept": dept,
                "subject": sublist,
                "dob": dob,
                "password": "teachergcect"
            }
            with open(f"{APP_ROOT}/db/teacherdetails.json", "w") as json_file:
                json_file.seek(0)
                json.dump(teacherDetail, json_file, indent=2)
            resp = {
                "status": "ok",
                "message": "teacher-added"
            }
    except Exception:
        with open(f"{APP_ROOT}/db/teacherdetails.json", "w") as json_file:
            json_file.seek(0)
            json.dump(teacherDetailBackup, json_file, indent=2)
        resp = {
            "status": "not-ok",
            "messege": "exception"
        }
    return resp


def addStudent(APP_ROOT, form):
    name = form.get("name")
    email = form.get("email")
    academicYear = form.get("academicyear")
    dept = form.get("dept")
    sem = form.get("sem")
    roll = form.get("roll")
    reg = form.get("reg")
    fee = 0
    status = ""
    transactionId = 0
    with open(f"{APP_ROOT}/db/subjects.json", "r") as json_file:
        subjectDetail = json.load(json_file)
    subject = subjectDetail[dept][sem]
    marks = [-1 for i in range(len(subject))]
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        allStudent = json.load(json_file)
    allStudentBackup = copy.deepcopy(allStudent)
    newStudent = {
        "name": name,
        "id": str(uuid.uuid4()),
        "email": email,
        "academic-year": academicYear,
        "dept": dept,
        "sem": sem,
        "roll": roll,
        "reg": reg,
        "marks": marks,
        "status": status,
        "transactionId": transactionId,
        "fee": fee
    }
    with open(f"{APP_ROOT}/db/studentlogin.json", "r") as json_file:
        studentLoginDetail = json.load(json_file)
    studentLoginDetailBackup = copy.deepcopy(studentLoginDetail)
    studentLoginDetail[email] = "student@gcect"
    try:
        allStudent.append(newStudent)
        with open(f"{APP_ROOT}/db/student1.json", "w") as json_file:
            json_file.seek(0)
            json.dump(allStudent, json_file, indent=2)
        with open(f"{APP_ROOT}/db/studentlogin.json", "w") as json_file:
            json_file.seek(0)
            json.dump(studentLoginDetail, json_file, indent=2)
        resp = {
            "status": "ok",
            "message": "student-added"
        }
    except Exception:
        with open(f"{APP_ROOT}/db/student1.json", "w") as json_file:
            json_file.seek(0)
            json.dump(allStudentBackup, json_file, indent=2)
        with open(f"{APP_ROOT}/db/studentlogin.json", "w") as json_file:
            json_file.seek(0)
            json.dump(studentLoginDetailBackup, json_file, indent=2)
        resp = {
            "status": "not-ok",
            "message": "exception"
        }
    return resp


def allowStudentForExam(APP_ROOT, id):
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        allStudent = json.load(json_file)
    allStudentBackup = copy.deepcopy(allStudent)
    try:
        for student in allStudent:
            if student["id"] == id:
                student["fee"] = 1
                break
        resp = {
            "status": "ok",
            "messege": "success"
        }
    except Exception:
        with open(f"{APP_ROOT}/db/student1.json", "w") as json_file:
            json_file.seek(0)
            json.dump(allStudentBackup, json_file, indent=2)
        resp = {
            "status": "not-ok",
            "messege": "exception"
        }
    return resp


def checkFeeStatus(APP_ROOT, form):
    sem = form.get("sem")
    dept = form.get("dept")
    with open(f"{APP_ROOT}/db/student1.json", "r") as json_file:
        allStudent = json.load(json_file)
    studentOfDeptSem = []
    try:
        for student in allStudent:
            if student["dept"] == dept and student["sem"] == sem:
                studentOfDeptSem.append(student)
        resp = {
            "status": "ok",
            "message": "success",
            "student-of-dept": studentOfDeptSem,
            "sem": sem,
            "dept": dept
        }
    except Exception:
        resp = {
            "status": "not-ok",
            "message": "exception"
        }
    return resp
