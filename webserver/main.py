# from ldp.depparser import parse as ldp_parse

import models.db as db
from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


@app.route("/")
def hello():

    session = db.DBSession()
    result = session.execute('SELECT * FROM users;')
    return str(list(result))

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('hello_world.html', name=username)


# @app.route('/parse/<sentence>')
# def parse(sentence):
#     """Show a parse tree for the given sentence using LDP."""
#     tokens = next(ldp_parse(sentence))
#     nodes = []
#     edges = []
#     for i, token in enumerate(tokens):
#         nodes.append({
#           'data': {'id': 'n%d' % (i + 1), 'title': token.form},
#           'position': {'x': i * 100, 'y': 0}
#         })
#
#         edge = {'data': {'id': str(i),
#                          'source': 'n%d' % (i + 1),
#                          'target': 'n%d' % (token.head),
#                          'direction': 1}}
#         inversed = token.head < i + 1
#         if inversed:
#             edge['style'] = {'control-point-distances': '50 50'}
#         edges.append(edge)
#
#     return render_template('parse.html',
#                            sentence=sentence,
#                            nodes=nodes,
#                            edges=edges)


@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
