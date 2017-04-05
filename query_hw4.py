import csv
import psycopg2
import string
import os

def ThreeA():
    query = "SELECT DISTINCT Term FROM Class;"
    cur.execute(query)
    AllTerms = cur.fetchall()

    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0
    eight =0
    nine = 0
    ten = 0
    eleven = 0
    twelve =0
    thirteen = 0
    fourteen = 0
    fithteen = 0
    sixteen =0
    seventeen = 0
    eighteen = 0
    ninteen = 0
    twenety = 0

    for term in AllTerms:
        count  = 0
        for unit in range(1, 21):
            count  = 0
            #print 'UNITS', unit
            # Find total num of students for that term
            query = 'SELECT DISTINCT sid FROM Meetingstudent where term = %s;' % (term[0])
            cur.execute(query)
            totalStudents = cur.fetchall()
            query =     'SELECT count(*)                            \
                        FROM (  SELECT sid, SUM(unitsTaken), term   \
                                FROM meetingstudent                 \
                                GROUP BY sid, term) AS Foo          \
                        WHERE sum = %s AND term = %s;'  % (unit, term[0])
            cur.execute(query)
            TotalForUnit = cur.fetchone()
            print TotalForUnit[0]
#            if(count = 1):
#                one = one + 1
#            if(count = 2):
#                two = two + 1

#            if(count = 3):
#                three= three + 1
#            if(count = 4 ):
#                four = four + 1
#            if(count = 5):
#                five = five + 1
#            if(count = ^)
#        count = count + 1
            

def ThreeB():
    query = "SELECT DISTINCT Term FROM Class;"
    cur.execute(query)
    AllTerms = cur.fetchall()

    for term in AllTerms:
        print
        print 'TERM', term[0]
        for unit in range(1, 21):
            #print 'UNITS', unit
            # Find total num of students for that term
            query = 'SELECT DISTINCT sid FROM Meetingstudent where term = %s;' % (term[0])
            cur.execute(query)
            totalStudents = cur.fetchall()
            #print len(totalStudents)
            query = 'SELECT avg(gradeval)   \
                    FROM meetingstudent \
                    WHERE sid IN (      \
                            SELECT sid      \
                            FROM        \
                               (SELECT sid, SUM(unitsTaken), term         \
                               FROM meetingstudent                         \
                               GROUP BY sid, term) AS Foo                   \
                            WHERE sum = %s AND term = %s)               \
                        AND                                                \
                            Term = %s;' % (unit, term[0], term[0])
                    
            cur.execute(query)
            avgGpa = cur.fetchone()
            print avgGpa[0]

def ThreeC():
    query ="SELECT * \
    FROM    (SELECT max(Avg) AS avg \
            FROM    (SELECT avg(gradeval), instructor   \
                    FROM (  (SELECT cid, term, gradeval \
                            FROM meetingstudent \
                            WHERE gradeval IS NOT NULL) AS OneQuery \
                            NATURAL JOIN meeting) \
                    GROUP BY instructor) As TwoQuery) AS Max    \
                NATURAL JOIN    \
                (SELECT avg(gradeval), instructor   \
                FROM (  (SELECT cid, term, gradeval \
                        FROM meetingstudent     \
                        WHERE gradeval IS NOT NULL) AS OneQuery     \
                        NATURAL JOIN meeting) \
                GROUP BY instructor) AS AvgWInst;"
    cur.execute(query)
    print "Easiest Instructors"
    print "-------------------"
    easiest = cur.fetchall()
    for instr in easiest:
        print instr
        
    query ="SELECT * \
    FROM    (SELECT min(Avg) AS avg \
            FROM    (SELECT avg(gradeval), instructor   \
                    FROM (  (SELECT cid, term, gradeval \
                            FROM meetingstudent \
                            WHERE gradeval IS NOT NULL) AS OneQuery \
                            NATURAL JOIN meeting) \
                    GROUP BY instructor) As TwoQuery) AS Max    \
                NATURAL JOIN    \
                (SELECT avg(gradeval), instructor   \
                FROM (  (SELECT cid, term, gradeval \
                        FROM meetingstudent     \
                        WHERE gradeval IS NOT NULL) AS OneQuery     \
                        NATURAL JOIN meeting) \
                GROUP BY instructor) AS AvgWInst;"
    cur.execute(query)
    print
    print "Hardest Instructors"
    print "-------------------"
    easiest = cur.fetchall()
    for instr in easiest:
        print instr


def ThreeD():
    query = "SELECT DISTINCT crse   \
            FROM class  \
            WHERE crse >= 100 AND crse <= 199"
    cur.execute(query)
    lvl100s = cur.fetchall()
    
    for course in lvl100s:
        query = "SELECT * \
                FROM    (SELECT max(Avg) AS avg \
                        FROM    (SELECT avg(gradeval), instructor \
                                FROM (  (SELECT cid, term, gradeval, subj, crse\
                                        FROM meetingstudent NATURAL JOIN class\
                                        WHERE   gradeval IS NOT NULL\
                                        AND subj = 'ABC'\
                                        AND crse = %s) AS OneQuery \
                                        NATURAL JOIN meeting) \
                                GROUP BY instructor) As TwoQuery) AS Max\
                            NATURAL JOIN\
                            (SELECT avg(gradeval), instructor \
                            FROM (  (SELECT cid, term, gradeval, subj, crse\
                                    FROM meetingstudent NATURAL JOIN class\
                                    WHERE   gradeval IS NOT NULL\
                                    AND subj = 'ABC'\
                                    AND crse = %s) AS OneQuery \
                                    NATURAL JOIN meeting) \
                            GROUP BY instructor) AS AvgWInst;" % (course[0], course[0])
        cur.execute(query)
        maxProf = cur.fetchall()
        print "Easiest Prof(s) for course: ", course[0]
        print "-------------------------------"
        for prof in maxProf:
            print prof
            print
##########
    
    for course in lvl100s:
        query = "SELECT * \
                FROM    (SELECT min(Avg) AS avg \
                        FROM    (SELECT avg(gradeval), instructor \
                                FROM (  (SELECT cid, term, gradeval, subj, crse\
                                        FROM meetingstudent NATURAL JOIN class\
                                        WHERE   gradeval IS NOT NULL\
                                        AND subj = 'ABC'\
                                        AND crse = %s) AS OneQuery \
                                        NATURAL JOIN meeting) \
                                GROUP BY instructor) As TwoQuery) AS Max\
                            NATURAL JOIN\
                            (SELECT avg(gradeval), instructor \
                            FROM (  (SELECT cid, term, gradeval, subj, crse\
                                    FROM meetingstudent NATURAL JOIN class\
                                    WHERE   gradeval IS NOT NULL\
                                    AND subj = 'ABC'\
                                    AND crse = %s) AS OneQuery \
                                    NATURAL JOIN meeting) \
                            GROUP BY instructor) AS AvgWInst;" % (course[0], course[0])
        cur.execute(query)
        maxProf = cur.fetchall()
        print "Hardest Prof(s) for course: ", course[0]
        print "-------------------------------"
        for prof in maxProf:
            print prof
            print
    
    
def ThreeE():
    query = "SELECT c2.term AS term, conf.m1_subj, conf.m1_crse, c2.subj AS m2_subj, c2.crse AS m2_crse  \
            FROM (  \
                  SELECT m1.cid AS m1_cid, m1.term, c.subj AS m1_subj, c.crse AS m1_crse, m1.timestart AS m1_start, m1.timeend AS m1_end, m2.timestart AS m2_start, m2.timeend AS m2_end, m2.cid AS m2_cid, m2.term AS m2_term  \
                  FROM meeting AS m1, meeting AS m2, class AS c \
                  WHERE (CAST(m1.term AS TEXT) LIKE '%10'   \
                         AND c.cid = m1.cid AND c.term = m1.term    \
                         AND m1.term = m2.term  \
                         AND m1.cid <> m2.cid   \
                         AND m1.build = m2.build    \
                         AND m1.room = m2.room  \
                         AND (m1.timestart >= m2.timestart AND m1.timestart < m2.timeend OR \
                             m1.timeend > m2.timestart AND m1.timeend <= m2.timeend)    \
                        )    \
                ) AS conf   \
                ,class AS c2    \
                WHERE c2.cid = conf.m2_cid AND c2.term = conf.m2_term;"
    cur.execute(query)
    print
    print "Conflicting Courses"
    print "-------------------"
    conf = cur.fetchall()
    for c in conf:
        print c
    
def ThreeF():
    query = "SELECT * \
            FROM    (SELECT max(avg) AS avg \
                    FROM(                    \
                        SELECT major, avg(gradeval) \
                        FROM ((meetingstudent NATURAL JOIN class) NATURAL JOIN student) \
                        WHERE subj = 'ABC'  \
                        GROUP BY major  \
                        ORDER BY major  \
                        ) AS avgs) AS Max   \
                    NATURAL JOIN    \
                    (SELECT major, avg(gradeval)    \
                    FROM ((meetingstudent NATURAL JOIN class) NATURAL JOIN student) \
                    WHERE subj = 'ABC'  \
                    GROUP BY major  \
                    ORDER BY major) AS AvgWMajor;"
    cur.execute(query)
    print "Best Perfoming Major(s)"
    print "------------------------"
    best = cur.fetchall()
    for major in best:
        print major
        
        
    query = "SELECT * \
            FROM    (SELECT min(avg) AS avg \
                    FROM(                    \
                        SELECT major, avg(gradeval) \
                        FROM ((meetingstudent NATURAL JOIN class) NATURAL JOIN student) \
                        WHERE subj = 'ABC'  \
                        GROUP BY major  \
                        ORDER BY major  \
                        ) AS avgs) AS Max   \
                    NATURAL JOIN    \
                    (SELECT major, avg(gradeval)    \
                    FROM ((meetingstudent NATURAL JOIN class) NATURAL JOIN student) \
                    WHERE subj = 'ABC'  \
                    GROUP BY major  \
                    ORDER BY major) AS AvgWMajor;"
    cur.execute(query)
    print
    print "Worst Perfoming Major(s)"
    print "------------------------"
    worst = cur.fetchall()
    for major in worst:
        print major

def ThreeG():
    query = "SELECT count(*)\
            FROM student;"
    cur.execute(query)
    numStud = cur.fetchone()
    
    query = "SELECT count(*) \
            FROM student    \
            WHERE   major LIKE 'ABC%'   \
                    AND OldMajor IS NOT NULL    \
                    AND OldMajor NOT LIKE 'ABC%';"
    cur.execute(query)
    numTransfer = cur.fetchone()
    print "total stud ", numStud[0]
    print "total transfer ", numTransfer[0]
    print "percentage: ", float(numTransfer[0]) / numStud[0]
    
    
    query = "SELECT OldMajor, count(OldMajor) AS cnt  \
            FROM student    \
            WHERE   major LIKE 'ABC%'   \
                    AND OldMajor IS NOT NULL    \
                    AND OldMajor NOT LIKE 'ABC%'    \
            GROUP BY OldMajor   \
            ORDER BY cnt DESC;"
    cur.execute(query)
    majors = cur.fetchall()
    print "Top 5 majors"
    print "-------------"
    for i in range(0,5):
        print majors[i][0], majors[i][1]
            
def main():

    # Try to connect
    global conn
    global cur
    try:
        conn = psycopg2.connect("dbname='postgres' user='weherr' password=''")
    except:
        print "I am unable to connect to the database."
        print "Ending Program."
        return
        
    cur = conn.cursor()
    
    ThreeA()
    #ThreeB()
    #ThreeC()
    #ThreeD()
    #ThreeE()
    #ThreeF()
    #ThreeG()
    
    #Close communication with the database
    cur.close()
    conn.close()


    print "Ending Program"







# Run main on opening
if __name__ == "__main__":
    main() 
