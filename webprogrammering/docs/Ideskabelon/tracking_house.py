from flask import Flask
from flask import request
from flask import g
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import send_file
import io
from flask import make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from random import randint


from tracking_datalayer import TrackingData

app = Flask(__name__)
app.secret_key = 'very secret string'

data = None

@app.teardown_appcontext
def close_connection(exception):
    data.close_connection()

"""
Denne funktion sørger for at pakke den template, der skal vises,
ind i nogle standard-ting, f.eks. loginstatus.

my_render bør kaldes i stedet for at kalde render_template direkte.
"""
def my_render(template, **kwargs):
    login_status = get_login_status()
    if login_status:
        return render_template(template, loggedin=login_status, user = session['currentuser'], **kwargs)
    else:
        return render_template(template, loggedin=login_status, user = '', **kwargs)

def get_login_status():
    return 'currentuser' in session

def get_user_id():
    if get_login_status():
        return session['currentuser']
    else:
        return -1

@app.route("/")
@app.route("/home")
def home():
    return my_render('home.html', vars = data.get_var_list(get_user_id()))

@app.route("/nyvar")
def nyvar():
    return my_render('nyvar.html')

@app.route("/visideer", methods=['GET'])
def vis():
    if False:
    #if 'currentuser' in session:
        if 'id' in request.args:
            ideer = data.get_idea_list(session['currentuser'], ideaid = request.args['id'])
        else:
            ideer = data.get_idea_list(session['currentuser'])

    else:
        ideer = [{'text': "noget tekst"},{'text': "noget mere tekst"}]
    return my_render("vis.html", ideas = ideer)

@app.route("/register")
def register():
    return my_render('register.html', success= True, complete = True)

@app.route("/login")
def login():
    return my_render('login.html', success = True)

@app.route("/logout")
def logout():
    session.pop('currentuser', None)
    return my_render('home.html')


@app.route("/about")
def about():
    return my_render('about.html', title='Om idéhuset')

@app.route("/contact")
def contact():
    return my_render('contact.html', title='Kontakt')

@app.route("/tilfoj_var", methods = ['POST'])
def tilfoj_var():
    name = request.form['name']
    type = request.form['type']

    data.add_new_var(get_user_id(), name, type)
    return redirect("/")

def login_success(user, pw):
    return data.login_success(user,pw)

def register_success(user, pw, email):
    return data.register_user(user, pw, email)

@app.route('/register_user', methods=['POST'])
def register_user():
    pw = request.form['password']
    user = request.form['username']
    email = request.form['email']

    if register_success(user, pw, email):
        #Create user object, store in session
        session['currentuser'] = data.get_user_id(user)
        return my_render('home.html')
    else:
        session.pop('currentuser', None)
        if len(pw) == 0 or len(user) == 0:
            return my_render('register.html', success = False, complete = False)
        else:
            return my_render('register.html', success = False, complete = True)


@app.route('/login_user', methods=['POST'])
def login_user():
    pw = request.form['password']
    user = request.form['username']

    if login_success(user, pw):
        #Create user object, store in session.
        session['currentuser'] = data.get_user_id(user)
        return my_render('home.html', vars = data.get_var_list(get_user_id()))
    else:
        session.pop('currentuser', None)
        return my_render('login.html', success = False)

@app.route('/fig/<figure_key>')
def fig(figure_key):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    axis.set_title(figure_key)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
    '''plt.title(figure_key)
    plt.plot([1,2,3,4], [1,3,2,4])
    img = io.BytesIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')'''


if __name__ == "__main__":
    with app.app_context():
        data = TrackingData()

    app.run(debug=True)
