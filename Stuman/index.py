from flask import render_template
from Stuman import app


@app.route("/")
def home():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
