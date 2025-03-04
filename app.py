from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Contact
from forms import ContactForm
import cx_Oracle
import os

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = False

# Database Info
DB_CONNECT_STRING = os.environ.get('DB_CONNECT_STRING')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://{}:{}@{}'.format(DB_USER,DB_PASSWORD,DB_CONNECT_STRING)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('contacts'))


@app.route("/new_contact", methods=('GET', 'POST'))
def new_contact():
    '''
    Create new contact
    '''
    form = ContactForm()
    if form.validate_on_submit():
        my_contact = Contact()
        form.populate_obj(my_contact)
        db.session.add(my_contact)
        try:
            db.session.commit()
            # User info
            flash('Employee successfully added.', 'success')
            return redirect(url_for('contacts'))
        except Exception as error:
            print(error)
            db.session.rollback()
            flash('Error adding employee.', 'danger')

    return render_template('web/new_contact.html', form=form)


@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
def edit_contact(id):
    '''
    Edit contact

    :param id: Id from contact
    '''
    my_contact = Contact.query.filter_by(id=id).first()
    form = ContactForm(obj=my_contact)
    if form.validate_on_submit():
        try:
            # Update contact
            form.populate_obj(my_contact)
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('successfully updated.', 'success')
        except:
            db.session.rollback()
            flash('Error while updating.', 'danger')
    return render_template(
        'web/edit_contact.html',
        form=form)


@app.route("/contacts")
def contacts():
    '''
    Show alls contacts
    '''
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=contacts)


@app.route("/search")
def search():
    '''
    Search
    '''
    name_search = request.args.get('name')
    all_contacts = Contact.query.filter(
        Contact.name.contains(name_search)
        ).order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=all_contacts)


@app.route("/contacts/delete", methods=('POST',))
def contacts_delete():
    '''
    Delete contact
    '''
    try:
        mi_contacto = Contact.query.filter_by(id=request.form['id']).first()
        db.session.delete(mi_contacto)
        db.session.commit()
        flash('successfully deleted.', 'danger')
    except:
        db.session.rollback()
        flash('error deleting.', 'danger')

    return redirect(url_for('contacts'))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
