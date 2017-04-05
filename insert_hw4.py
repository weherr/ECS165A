import csv
import psycopg2
import string
import os


def main():

    # Try to connect
    GradesPath = "./Grades/"
    try:
        conn=psycopg2.connect("dbname='temoc536' user='temoc536' password=''")
    except:
        print "I am unable to connect to the database."
        print "Ending Program."
        return
        
    cur = conn.cursor()

    #Create relation Class
    #Class (CID, Term, subj, crse, sec, units)             key: cid
    try:
        cur.execute("CREATE TABLE Class(CID INTEGER, Term INTEGER, Subj VARCHAR(3), CRSE INTEGER, SEC INTEGER, Units VARCHAR(32), PRIMARY KEY(CID, TERM) );")
    except:
        print "Relation Class already exists."
    
    #Create relation Meeting
    #Meeting(cid, instructor, type, days, time, build, room)    key: cid
    try:
        cur.execute("CREATE TABLE Meeting(CID INTEGER, Term INTEGER, Instructor VARCHAR(256), Type VARCHAR(256), Days VARCHAR(8), TimeStart TIME DEFAULT NULL, TimeEnd TIME DEFAULT NULL, Build VARCHAR(256), Room INTEGER DEFAULT NULL);") #possible the key is not unique if same day also
    except:
        print "Relation Meeting already exists."
    
    #Create relation MeetingStudents
    #Note: UnitsTaken named different because not the same as Units
    #MeetingStudents(sid, cid, seat, unitsTaken)            key: cid, sid
    try:
        cur.execute("CREATE TABLE MeetingStudent(SID INTEGER , CID INTEGER, Term INTEGER, Seat INTEGER, UnitsTaken INTEGER DEFAULT NULL, Grade VARCHAR(8) DEFAULT NULL, GradeVal FLOAT  DEFAULT NULL);")
    except:
        print "Relation MeetingStudents already exists."
    
    #Create relation Students
    #student(sid, prefname, last, level, class, major, email)   key: sid
    try:
        cur.execute("CREATE TABLE Student(SID INTEGER PRIMARY KEY, Prefname VARCHAR(256), Last VARCHAR(256), Level VARCHAR(256), Class VARCHAR(256), OldMajor VARCHAR(256) DEFAULT NULL, Major VARCHAR(256), Email VARCHAR(256));")
    except:
        print "Relation Student already exists."


    conn.commit()
    print "All tables created."


    files = os.listdir(GradesPath)
    for file in files:
        NewFile = GradesPath + str(file)
        print NewFile
        with open(NewFile) as csvfile:
            reader = csv.reader(csvfile)
            totalLines = 0
            CID = False
            Students = False
            Instructor = False
            Seat = False
            
            PrevCid = "unsetCid"
            PrevTerm = "unsetTerm"
            PrevInstructor = "unsetInst"
            for row in reader:
                
                #Set bools for what type of data will be coming up
                #If empty space then a new type of data is next reset everything 
                if(len(row) == 1 and row[0] == ""):
                    CID = False
                    Students = False
                    Instructor = False
                    Seat = False
                    continue
                elif(row[0] == "SEAT"):
                    Students = True
                    continue
                elif(row[0] == "CID"):
                    CID = True
                    continue
                elif(row[0] == "INSTRUCTOR(S)"):
                    Instructor = True
                    continue
                    
                #Replace all ' with '' per sql syntax
                for i in range(len(row)):
                    row[i] = string.replace(row[i], "'", "''")

                # Fill class table
                if(CID):
                    # Check if student is in the database
                    query = 'Select CID, Term FROM Class WHERE CID = %s AND term = %s;' % (row[0], row[1])
                
                    cur.execute(query)
                    if(cur.fetchone() == None):
                        insert = " INSERT INTO Class VALUES (%s, %s, '%s', %s, %s, '%s');" % (row[0], row[1], row[2], row[3], row[4], row[5])
                        cur.execute(insert)
                        PrevCid = row[0]
                        PrevTerm = row[1]
                
                # Fill student and meeting student table
                elif(Students):
                    # Check if student is in the database
                    query = 'Select SID FROM Student WHERE SID = %s;' % (row[1])
                
                    cur.execute(query)
                    if(cur.fetchone() == None):
                        insert = " INSERT INTO Student(sid, prefname, last, level, class, major, email)  VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s');" % (row[1], row[3], row[2], row[4], row[6], row[7], row[10])
                        cur.execute(insert)
    
                    #Student already in DB , then update the OldMajor and major
                    else:
                        query = "SELECT major FROM student WHERE sid = %s;" % (row[1])
                        cur.execute(query)
                        OldMajor = cur.fetchone()
                        #print oldAndNewMajor[0]
                        
                        if(OldMajor[0] != row[7]):
                            update = " UPDATE student SET OldMajor = '%s', major = '%s' WHERE sid = %s;" % (OldMajor[0], row[7], row[1])
                            cur.execute(update)
                       
                    # Fill meeting student table
                    if(row[5] == ""):
                        unitsTaken = "DEFAULT"
                    else:
                        unitsTaken = row[5]
                        
                    #calculate grade value
                    isValidVal = True
                    GradeVal = 0.00
                    if(row[8]=="A+" or row[8]=="A"):
                        GradeVal = 4.00
                    elif(row[8]=="A-"):
                        GradeVal = 3.70
                    elif(row[8]=="B+"):
                        GradeVal = 3.30
                    elif(row[8]=="B"):
                        GradeVal = 3.00
                    elif(row[8]=="B-"):
                        GradeVal = 2.70
                    elif(row[8]=="C+"):
                        GradeVal = 2.30
                    elif(row[8]=="C"):
                        GradeVal = 2.00
                    elif(row[8]=="C-"):
                        GradeVal = 1.70
                    elif(row[8]=="D+"):
                        GradeVal = 1.30
                    elif(row[8]=="D"):
                        GradeVal = 1.00
                    elif(row[8]=="D-"):
                        GradeVal = 0.70
                    elif(row[8]=="F"):
                        GradeVal = 0.00    
                    else:
                        isValidVal = False
                        
                    insert = " INSERT INTO MeetingStudent VALUES (%s, %s, %s, %s, %s, '%s', %s);" % (row[1], PrevCid, PrevTerm, row[0], unitsTaken, row[8], GradeVal)
                    
                    if(isValidVal == False):
                        insert = " INSERT INTO MeetingStudent VALUES (%s, %s, %s, %s, %s, '%s');" % (row[1], PrevCid, PrevTerm, row[0], unitsTaken, row[8])
                    cur.execute(insert)
                
                # Fill meeting table       
                elif(Instructor):
                    if(row[0] != ""):
                        PrevInstructor = row[0]
                        
                        
                    if(row[5] == ""):
                        room = "DEFAULT"
                    else:
                        room = row[5]
                    
                    #if time is missing
                    if(row[3] == ""):
                        insert = " INSERT INTO meeting(cid, term, instructor, type, days, build, room) VALUES (%s, %s, '%s', '%s', '%s', '%s', %s);" % (PrevCid, PrevTerm, PrevInstructor, row[1], row[2], row[4], room)
                    else:
                        times = row[3].split(' - ')
                        insert = " INSERT INTO meeting VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s', %s);" % (PrevCid, PrevTerm, PrevInstructor, row[1], row[2], times[0], times[1], row[4], room)
                    
                    cur.execute(insert)
                    
                    
                
                



        csvfile.close()   




        # Make the changes to the database persistent
        conn.commit()

    #Close communication with the database
    cur.close()
    conn.close()


    print "Ending Program"

# Run main on opening
if __name__ == "__main__":
    main() 