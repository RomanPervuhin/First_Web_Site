from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

secret_password = 'M_y105000Fw_S_2413'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    intro = db.Column(db.String(512), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    authors_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/publications')
def publications():
    publications = Article.query.order_by(Article.date.desc()).all()
    return render_template('publications.html', publications=publications)


@app.route('/publications/<int:id>')
def publication(id):
    publication = Article.query.get(id)
    return render_template('publication.html', publication=publication)


@app.route('/publications/<int:id>/del', methods=['POST', 'GET'])
def publication_delete(id):
    if request.method == 'POST':
        password1 = request.form['password1']

        if password1 != secret_password:
            return render_template('password_error2.html')

        if password1 == secret_password:
            publication = Article.query.get_or_404(id)
            try:
                db.session.delete(publication)
                db.session.commit()
                return redirect('/publications')
            except:
                return 'An error occurred while deleting the publication!'

    return render_template('publication_del.html')


@app.route('/create new publication', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        authors_name = request.form['authors_name']
        intro = request.form['intro']
        text = request.form['text']
        password = request.form['password']

        article = Article(password=password, title=title, authors_name=authors_name, intro=intro, text=text)

        if password != secret_password:
            return render_template('password_error.html')

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/publications')
        except:
            return 'An error occurred while adding the publication!'

    else:
        return render_template('create.html')

    return render_template('create.html')


@app.route('/password_error')
def password_error():
    return render_template('password_error.html')


@app.route('/publications/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    publication = Article.query.get(id)
    if request.method == 'POST':
        publication.title = request.form['title']
        publication.authors_name = request.form['authors_name']
        publication.intro = request.form['intro']
        publication.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/publications')
        except:
            return 'An error occurred while editing the publication!'

    else:
        return render_template('publication_edit.html', publication=publication)

    return render_template('create.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run()
