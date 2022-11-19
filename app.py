import os, mimetypes
from flask import Flask, render_template

STATIC_FOLDER = os.path.dirname(__file__) + '/static/'

mimetypes.add_type('application/javascript', '.js')

app = Flask(
    import_name=__name__,
    template_folder=STATIC_FOLDER + 'html',
    static_folder=STATIC_FOLDER
)


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)