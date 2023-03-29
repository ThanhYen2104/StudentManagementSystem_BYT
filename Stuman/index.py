from flask import render_template
from StudentManagementSystem_BYT.Stuman import app
from flask_admin import Admin

admin = Admin(app, name="BYT EDUCATION ADMINISTRATION", template_mode='bootstap4')


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
