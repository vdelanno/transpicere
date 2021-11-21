from flask import Flask
from graphql_server.flask import GraphQLView

from web.schema import get_schema

SCHEMA = get_schema()

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=SCHEMA,
    graphiql=True,
))

if __name__ == '__main__':
    app.run(debug=True)
