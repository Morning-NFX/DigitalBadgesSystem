from http.client import ImproperConnectionState
from flask import *
from flask_session import Session
import database
import shutil
from os import path
import qrcode


# Initialise the application
app = Flask(__name__)
app.config['SECRET_KEY'] = """
                           hVmYq3t6w9z$C&F)J@NcRfUjWnZr4u7x!A%D*G-KaPdSgVkYp2s5v8y/B?E(H+MbQeThWmZq4t6w9z$C&F)J@N
                           cRfUjXn2r5u8x!A%D*G-KaPdSgVkYp3s6v9y$B?E(H+MbQeThWmZq4t7w!z%C*F)J@NcRfUjXn2r5u8x/A?9y
                           D(G+KaPdSgVkYp3s6v9y$B&E)H@McQeThWmZq4t7w!z%C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeShVmYp3s6v
                           """
app.config['SESSION_TYPE'] = 'filesystem'
if path.exists("./flask_session"):
    shutil.rmtree("./flask_session")
Session(app)


#########
# INDEX #
#########
@app.route('/')
def index():
    """
    Main entrance
    """
    return render_template('index.html',
                           session=session)


############
#  BADGES  #
############
@app.route('/badges', methods=['GET'])
def listAllBadges():
    # check login status
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))

    if (request.method == 'GET'):
        badges = database.getAllBadges()
        if badges == None or len(badges) == 0:
            badges = None
        return (render_template('badges/badgesList.html',
                                session=session,
                                badges=badges))


@app.route('/badges/create', methods=['GET', 'POST'])
def createBadge():
    # check login status
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))

    if (request.method == 'GET'):
        return (render_template('badges/create.html', session=session))
    if (request.method == 'POST'):
        badge = None
        badge = database.createBadge(request.form['title'], request.form['description'])
        if badge == None:
            return (render_template('badges/error.html', session=session,
                                    error="Unable to create badge. Please make sure this badge doesn't already exist and try again."))

        return (render_template('badges/createSuccess.html', session=session, badge=badge))


@app.route('/deletebadge', methods=['POST'])
def delete_badge():
    # check login status
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))

    if request.method == 'POST':
        badge_id = request.form['badgeId']
        badge_title = request.form['badgeTitle']

        database.delete_badge(badge_id)
        session['error'] = False
        flash(' '.join(["Successfully deleted badge -", badge_title]))
        return redirect(url_for('listAllBadges'))


###################
#  ASSIGN BADGES  #
###################
@app.route('/assign_badge/select_badge')
def assign_badge_badge():
    """
    Select raw badge type to be assigned
    """
    # check login status
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))

    badges = database.getAllBadges()
    if badges == None or len(badges) == 0:
        badges = None
    return (render_template('badges/assignBadge/badgeSelect.html',
                            session=session,
                            badges=badges))


@app.route('/assign_badge/<badge_id>')
def assign_badge_student(badge_id):
    """
    Select students the raw badge will assign to
    """
    # check login status
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))

    student_list = database.get_student_list()
    badge = database.get_badge_info(badge_id)[0]

    return render_template('badges/assignBadge/studentSelect.html',
                           badge=badge,
                           students=student_list,
                           session=session)

@app.route('/assign_badge/operation', methods=['POST'])
def assign_badge_operation():
    if request.method == 'POST':
        badge_id = request.form['badgeId']
        students = request.form['students'].replace("_", " ")
        description = request.form['description'].replace("_", " ")
        student_list = students.split("/")
        session['tmp'] = []
        for student in student_list:
            new_badge_id = database.award_badge(badge_id, database.get_student_id(student)[0].get('id'), session['user_id'], description)
            session['tmp'].append(new_badge_id)
        session['error'] = False
        flash('You have successfully awarded ' + str(len(student_list)) + ' badges!')
        return redirect(url_for('assign_badge_summary'))


@app.route('/assign_badge/summary')
def assign_badge_summary():
    badges = []
    badges_id = session['tmp']
    for content in badges_id:
        badge_id = content[0].get('id')
        badges.append(database.check_badge(badge_id))
    return render_template('badges/assignBadge/summary.html',
                           badges=badges,
                           session=session)


###########
#  STAFF  #
###########
@app.route('/staff/<staff_id>')
def staff_home(staff_id):
    # check login status
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))
    # user not staff
    if session['user_type'] != 'staff':
        session['error'] = True
        flash('Invalid operation')
        return redirect(url_for('index'))

    awarded_badges = database.getStaffAwardedBadges(session['user_id'])
    return render_template('staff/staff_home.html',
                           staff_info=database.staff_home_info(staff_id),
                           badges=awarded_badges,
                           session=session)


@app.route('/revokebadge', methods=['POST'])
# check login status
def revoke_badge():
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))
    if request.method == 'POST':
        badge_id = request.form['badgeId']
        database.revoke_badge(badge_id)
        return redirect(url_for('staff_home', staff_id=session['user_id']))
@app.route('/editbadge', methods=['POST'])
# check login status
def edit_badge():
    if 'user_name' not in session:
        session['error'] = True
        flash('Please login')
        return redirect(url_for('index'))
    if request.method == 'POST':
        badge_id = request.form['badgeId']
        new_description = request.form['description'].replace("_", " ")
        database.edit_badge(badge_id, new_description)
        return redirect(url_for('staff_home', staff_id=session['user_id']))


###################
#  LOGIN CONTROL  #
###################
@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    """
    Staff login page
    """
    # user already login as staff
    if 'user_name' in session and session['user_type'] == 'staff':
        session['error'] = True
        flash('You have already login')
        return redirect(url_for('staff_home', staff_id=session['user_id']))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        correctLogin = database.check_staff_login(username, password)
        # login fail
        if correctLogin is False:
            session['error'] = True
            flash('Incorrect login information')
            return redirect(url_for('staff_login'))
        # login successful
        session['user_name'] = username
        session['user_type'] = 'staff'
        staff_user = database.get_staff(username)
        session['user_id'] = staff_user["id"]

        session['error'] = False
        flash('Login successful as ' + username)

        return redirect(url_for('staff_home', staff_id=session['user_id']))

    elif request.method == 'GET':
        return render_template('staff/staff_login.html', hideStaffButton=True)


@app.route('/logout')
def logout():
    """
    Logs out of the current session
    """
    # user haven't login yet
    if 'user_name' not in session:
        session['error'] = True
        flash('You have not login yet')
        return redirect(url_for('index'))

    # logout successfully
    session['error'] = False
    flash('You have been logged out')
    session.pop('user_name')
    return redirect(url_for('index'))


@app.route('/badges/<id>')
def show_badge(id):
    single_badge_data = database.check_badge(id)

    if single_badge_data is not None:
        # generate qr if file doesn't exist
        if path.isfile("./static/images/qr/"+id) == False:
            qr = qrcode.QRCode(version="1", box_size=10, border=5)
            qr.add_data(request.base_url)
            img = qr.make_image(fill_color=(230, 70, 38), back_color="white")
            img.save("./static/images/qr/"+id+".png")
            return render_template('badges/singleAwarded.html', data=single_badge_data)
    else:
        session['error'] = True
        flash("Badge not found.")
        return redirect(url_for('index'))

@app.route('/student/portfolio/<id>')
def show_portfolio(id):
    badges = database.getBadgesForStudent(id)
    if badges is not None:
        return render_template('badges/portfolio.html', data=badges)
    else:
        session['error'] = True
        flash("Student portfolio not found.")
        return redirect(url_for('index'))
