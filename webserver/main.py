from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('hello_world.html', name=username)


if __name__ == "__main__":
    app.run()
