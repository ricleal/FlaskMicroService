r'''
Bare bones example of Flask
'''

from flask import Flask, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<body>
    <h1>Flask Test</h1>
    <p>This is generated by Flask</p>
    <p><a href="/link">Click here to go to the link page</a></p>
    <p><a href="/form_page">Click here to go to the form page</a></p>
</body>
</html>
'''


@app.route('/link')
def link():
    return '''<!DOCTYPE html>
<html>
<body>
    <h1>Flask Test: Link page</h1>
    <p>This is the link page generated by Flask</p>
    <a href="/">Go back to the index</a>
</body>
</html>
'''


@app.route('/form_page')
def form_page():
    return '''<!DOCTYPE html>
<html>
<body>
    <h1>Flask Test: Form page</h1>
    <form action="/form_submit" method="post">
        First name:<br>
        <input type="text" name="firstname"><br>
        Last name:<br>
        <input type="text" name="lastname"><br>
        <input type="submit" value="Submit"><br>
    </form>
    <a href="/">Go back to the index</a>
</body>
</html>
'''


@app.route('/form_submit', methods=['POST'])
def form_submit():
    contents_raw = request.form
    print(80*"-")
    print(contents_raw)
    contents_dic = request.form.to_dict()
    print(contents_dic)
    print(80*"-")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)