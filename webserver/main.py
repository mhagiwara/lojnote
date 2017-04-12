from ldp.depparser import parse as ldp_parse

from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('hello_world.html', name=username)


@app.route('/parse/<sentence>')
def parse(sentence):
    """Show a parse tree for the given sentence using LDP."""
    parse_str = str(list(ldp_parse(sentence)))
    return render_template('parse.html', sentence=sentence, parse_str=parse_str)


@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run()
