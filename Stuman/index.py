from flask import render_template
from Stuman import app
from flask_admin import Admin

admin = Admin(app, name="BYT EDUCATION ADMINISTRATION", template_mode='bootstap4')


@app.route("/")
def home():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
