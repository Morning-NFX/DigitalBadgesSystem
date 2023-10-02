from configparser import ConfigParser
import psycopg2
import bcrypt
import string
import random


############
# DB Tools #
############
def database_connect():
    """
    Connect to the database
    """
    config_file = "config.ini"
    config_section = "DATABASE"
    # Read configuration file
    parser = ConfigParser()
    parser.read(config_file)
    parameters = {}
    if parser.has_section(config_section):
        params = parser.items(config_section)
        for item in params:
            parameters[item[0]] = item[1]
    else:
        raise Exception("Error while reading configuration file")
    # Connection to database
    conn = None
    try:
        conn = psycopg2.connect(**parameters)
    except (Exception, psycopg2.DatabaseError) as error:
        return None
    return conn


def dictfetchall(cursor, sqltext, params=None):
    """
    Returns query results as list of dictionaries.
    """
    result = []
    cursor.execute(sqltext, params)
    cols = [a[0] for a in cursor.description]
    returnres = cursor.fetchall()
    for row in returnres:
        result.append({a: b for a, b in zip(cols, row)})
    return result


def dictfetchone(cursor, sqltext, params=None):
    """
    Returns query results as list of dictionaries.
    """
    result = []
    cursor.execute(sqltext, params)
    cols = [a[0] for a in cursor.description]
    returnres = cursor.fetchone()
    result.append({a: b for a, b in zip(cols, returnres)})
    return result


##########
# Badges #
##########
# Get a list of badges in the system
def getAllBadges():
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    r = dictfetchall(cur, 'SELECT * FROM badgesystem.Badge')
    return r


# create a new badge in the system. Returns the new badge
def createBadge(title, description):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    res = dictfetchone(cur,
                       "INSERT INTO badgesystem.Badge(title, description) VALUES (%s, %s) RETURNING id, title, description",
                       [title, description])
    conn.commit()
    return res[0]


def delete_badge(badge_id):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
                  DELETE FROM badgesystem.badge WHERE id = %s;
                 """
        cur.execute(sql, (badge_id,))
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return None


def award_badge(badge_id, student_id, staff_id, description):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        res = dictfetchone(cur,
                           "INSERT INTO badgesystem.awardedbadge(id, badge_id, student_id, issued_by, issued_for) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                           [random_id_generator(), badge_id, student_id, staff_id, description])
        conn.commit()
        return res
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        return None


def revoke_badge(badge_id):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
              DELETE FROM badgesystem.awardedbadge WHERE id = %s;
             """
        cur.execute(sql, (badge_id,))
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return None


def edit_badge(badge_id, new_description):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
              UPDATE badgesystem.awardedbadge SET issued_for = %s WHERE id = %s;
             """
        cur.execute(sql, (new_description, badge_id))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        return None


###############
# Staff LOGIN #
###############
# returns true if correct login, false if otherwise
def check_staff_login(username, password):
    """
    Check that the users information exists in the database.
    """
    conn = database_connect()
    if conn is None:
        return False
    cur = conn.cursor()
    try:
        sql = """
        SELECT * 
            FROM badgesystem.staff
            WHERE username=%s LIMIT 1;
            """
        r = dictfetchone(cur, sql, [username])
        if r is None:
            return False
        hashed = r[0]["password"]
        cur.close()
        conn.close()
        if bcrypt.checkpw(password, hashed):
            return True
        return False
    except:
        return False


# get a staff member by username.
def get_staff(username):
    conn = database_connect()
    if conn is None:
        return False
    cur = conn.cursor()
    try:
        sql = """
        SELECT * 
          FROM badgesystem.staff
         WHERE username=%s LIMIT 1;
         """
        r = dictfetchone(cur, sql, [username])
        cur.close()
        conn.close()
        if r is None:
            return None
        return r[0]
    except:
        return None


def staff_home_info(staff_id):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
            SELECT s.name, COUNT(ab.id) AS awardeBadgeNumber
              FROM badgesystem.staff s LEFT JOIN badgesystem.awardedBadge ab ON (s.id = ab.issued_by)
          GROUP BY s.id, s.name
            HAVING s.id = %s;
                """
        r = dictfetchone(cur, sql, (staff_id,))
        cur.close()
        conn.close()
        if r is None:
            return None
        return r[0]
    except (Exception, psycopg2.DatabaseError) as error:
        return None


###############
# Portfolio SEARCH #
###############
# get the badges for a student given their id.
def getBadgesForStudent(id):
    """
    Check that the users information exists in the database.
    """
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
        SELECT badgesystem.awardedBadge.id, badge_id, student_id, issued_by, date_issued, issued_for, title, description, student.name, curricular, image_url FROM badgesystem.awardedBadge 
        INNER JOIN badgesystem.badge ON badgesystem.badge.id = badgesystem.awardedBadge.badge_id
        INNER JOIN badgesystem.student ON badgesystem.awardedBadge.student_id = badgesystem.student.id
        INNER JOIN badgesystem.staff ON badgesystem.awardedBadge.issued_by = badgesystem.staff.id
        WHERE badgesystem.awardedBadge.student_id=%s
        """

        r = dictfetchall(cur, sql, [id])
        cur.close()
        conn.close()
        if len(r) == 0:
            cur.close()
            conn.close()
            return None
        return r
    except:
        print("No student found")
    cur.close()
    conn.close()
    return None


###############
# single Badge SEARCH #
###############
def check_badge(id):
    """
    Check that the users information exists in the database.
    """
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
            SELECT badgesystem.awardedbadge.id, student.name, staff.name as staff_name, issued_for, title, date_issued, TO_CHAR(date_issued, 'DD Mon, yyyy') as date_issued_formatted, curricular
            FROM badgesystem.awardedbadge
              INNER JOIN badgesystem.student ON badgesystem.awardedBadge.student_id = badgesystem.student.id
              INNER JOIN badgesystem.staff ON badgesystem.awardedBadge.issued_by = badgesystem.staff.id
              INNER JOIN badgesystem.badge ON badgesystem.awardedBadge.badge_id = badgesystem.badge.id;
            """

        r = dictfetchall(cur, sql)

        for badge in r:
            if badge.get("id") == id:
                return badge
        cur.close()
        conn.close()
        return None
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return None


def get_badge_info(badge_id):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
                SELECT id, title 
                  FROM badgesystem.badge
                 WHERE id = %s;
                """

        r = dictfetchall(cur, sql, [badge_id])
        cur.close()
        conn.close()
        if r is None:
            return None
        return r
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return None


###############
# Staff Awarded Badges #
###############
# get the badges for a student given their id.
def getStaffAwardedBadges(staff_id):
    """
    Check that the users information exists in the database.
    """
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
        SELECT badgesystem.student.name as student_name, badgesystem.awardedBadge.date_issued as date_issued, badgesystem.awardedBadge.issued_for as issued_for, badgesystem.awardedBadge.id as id
        FROM badgesystem.awardedBadge 
        INNER JOIN badgesystem.student ON badgesystem.student.id=badgesystem.awardedBadge.student_id 
        WHERE badgesystem.awardedBadge.issued_by=%s
        ORDER BY date_issued DESC
        LIMIT 10;
        """

        r = dictfetchall(cur, sql, [staff_id])
        cur.close()
        conn.close()
        if len(r) == 0:
            cur.close()
            conn.close()
            return None
        return r
    except Exception as e:
        print(e)
        print("You have not awarded any Badges yet :(")
    cur.close()
    conn.close()
    return None


def get_student_list():
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
            SELECT * FROM badgesystem.student;
            """

        r = dictfetchall(cur, sql, )
        cur.close()
        conn.close()
        if r is None:
            return None
        return r
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return None


def get_student_id(student_name):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        sql = """
                SELECT id FROM badgesystem.student WHERE name=%s;
                """

        r = dictfetchall(cur, sql, [student_name])
        cur.close()
        conn.close()
        if r is None:
            return None
        return r
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
    return None


def random_id_generator():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(40))
