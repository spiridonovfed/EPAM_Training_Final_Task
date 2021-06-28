import os
from random import random

import requests
from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired, NumberRange

# ------------- SETTINGS ----------------- #
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")  # Change to your settings
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")  # Change to your settings
POSTGRES_DB_NAME = "flasksql"  # Change to your settings

ENTRIES_PER_PAGE = 300

# -------------- Flask App ------------------ #

app = Flask(__name__)
app.secret_key = "any-string-to-keep-in-secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB_NAME}"
Bootstrap(app)

# ----------------- Database setup and handling -------------------- #
db = SQLAlchemy(app)


# Creating Table
class Person(db.Model):
    """This is a class to represent a Person table in the database
    :class: 'SQLAlchemy.Model'

    :param id: id and primary key of any entry in the database
    :type id: int, optional
    :param gender: gender of a person in the database
    :type gender: str
    :param first_name: first name of a person in the database
    :type first_name : str
    :param cell: cell phone number of a person in the database
    :type cell: str
    :param email: email of a person in the database
    :type email: str
    :param location: location of a person in the database
    :type location: str
    :param pic_link: link to a picture file of a person in the database
    :type pic_link: str
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(6), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    cell = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    pic_link = db.Column(db.String(500), nullable=False)


# Creating a class to handle the database
class DatabaseHandler:
    """This is a class to wrap all working with database functionality.
    Can be used without instances."""

    @staticmethod
    def create_table():
        """Creates Person table in the database if there is none"""
        db.create_all()

    @staticmethod
    def rerecord_data(quantity):
        """Delete all the data in the Person table and inserts a new data.
        All the data is collected with help of randomuser.me API.
        Parameter 'quantity' determines the number of entries of a new data.

        :param quantity: a number of records needed in a new dataset in the database
        :type quantity: int
        """
        db.session.query(Person).delete()
        db.session.commit()

        url = "https://randomuser.me/api/"
        parameters = {
            "inc": "gender, name, cell, email, location, picture",
            "results": quantity,
        }

        response = requests.get(url, params=parameters)
        response.raise_for_status()
        data = response.json()["results"]

        input_for_db = []
        for person_data in data:
            gender = person_data["gender"]
            first_name = person_data["name"]["first"]
            last_name = person_data["name"]["last"]
            cell = person_data["cell"]
            email = person_data["email"]
            location = f"{person_data['location']['city']}, {person_data['location']['country']}"
            pic_link = person_data["picture"]["large"]

            person_object = Person(
                gender=gender,
                first_name=first_name,
                last_name=last_name,
                cell=cell,
                email=email,
                location=location,
                pic_link=pic_link,
            )
            input_for_db.append(person_object)

        db.session.bulk_save_objects(input_for_db)
        db.session.commit()

    @staticmethod
    def create_new_record(edit_form):
        """
        Creates new entry in the Person table of the database.

        :param edit_form: object of a 'EditForm' class, has a data passed in in it
        :type edit_form: class 'EditForm(FlaskForm)'
        """
        new_person = Person(
            gender=edit_form.gender.data,
            first_name=edit_form.first_name.data,
            last_name=edit_form.last_name.data,
            cell=edit_form.cell.data,
            email=edit_form.email.data,
            location=edit_form.location.data,
            pic_link=edit_form.pic_link.data,
        )

        db.session.add(new_person)
        db.session.commit()

    @staticmethod
    def all_records_query():
        """Returns SQLAlchemy.Session.Query object with all the data in a database ordered by it's id.

        :return: SQLAlchemy.Session.Query object with all the data in a database ordered by it's id
        :rtype: SQLAlchemy.Session.Query object
        """
        return db.session.query(Person).order_by(Person.id)

    @staticmethod
    def get_person_data(person_id):
        """Returns a person data with an id passed in.

        :param person_id: id of a person in the Person table in the database
        :type person_id: int
        :return: all the person data in the database
        :rtype: class 'Person(db.Model)'
        """
        person_data = Person.query.get(person_id)
        print(type(person_data))
        return person_data

    @staticmethod
    def update_personal_data(person_id, edit_form):
        """Updates a person data in the database.

        :param person_id: id of a person in the Person table in the database
        :type person_id: int
        :param edit_form: object of a 'EditForm' class, has a data passed in in it
        :type edit_form: class 'EditForm(FlaskForm)'
        """
        person_data = Person.query.get(person_id)
        person_data.first_name = edit_form.first_name.data
        person_data.last_name = edit_form.last_name.data
        person_data.gender = edit_form.gender.data
        person_data.cell = edit_form.cell.data
        person_data.email = edit_form.email.data
        person_data.location = edit_form.location.data
        person_data.pic_link = edit_form.pic_link.data
        db.session.commit()

    @staticmethod
    def delete_person(person_id):
        """Deletes a person data from the Person tables from the database.

        :param person_id: id of a person in the Person table in the database
        :type person_id: int
        """
        person_data_to_delete = Person.query.get(person_id)
        db.session.delete(person_data_to_delete)
        db.session.commit()

    @staticmethod
    def generate_random_person_id():
        """Generates a random id of one entry from all the entries existing in the database.

        :return: a random id number from existing entries in the database
        :rtype: int
        """
        query = db.session.query(Person)
        rowCount = int(query.count())
        randomRow = query.offset(int(rowCount * random())).first()
        random_id = randomRow.id
        return random_id


# --------------- Flask Forms ------------------ #
class QuantityForm(FlaskForm):
    """This is a class to generate a form to give user an option to specify
    a quantity of entries in the database required (it is set up to 1000 by default).
    Consists of one Decimal Field to input integer in range 1-5000 (the biggest possible randomuser.me API response)
    and a submit button.
    Validators to check if there any entry and if that's an integer in range 1-5000 are established.
    class: 'FlaskForm'
    """

    quantity = DecimalField(
        "",
        validators=[
            InputRequired(),
            NumberRange(
                min=1, max=5000, message="Only integers in range 1-5000 are allowed"
            ),
        ],
    )
    submit = SubmitField(label="Change Number")


class EditForm(FlaskForm):
    """This is a class to generate a form to provide options
    to create new entry to the dataset or edit an existing one.
    All the fields have 'InputRequired' validator and EmailField has also an Email validator.
    class: 'FlaskForm'
    """

    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    gender = StringField("Gender", validators=[InputRequired()])
    cell = StringField("Cell Number", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    location = StringField("Location", validators=[InputRequired()])
    pic_link = StringField("Link to a photo_file", validators=[InputRequired()])
    submit = SubmitField(label="Save Data")


# ----------------- Flask Routing and Rendering ----------------------- #


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/index/<int:page>", methods=["GET", "POST"])
def index(page=1):
    """Renders the index page of the app.

    :param page: a page number, defaults to 1
    :type page: int, optional
    """
    quantity_form = QuantityForm()
    if quantity_form.validate_on_submit():
        new_quantity = quantity_form.quantity.data
        DatabaseHandler.rerecord_data(new_quantity)
        return redirect(url_for("index"))

    db_query_object = DatabaseHandler.all_records_query()
    all_people_data = db_query_object.all()
    people_data_paginated = db_query_object.paginate(page, ENTRIES_PER_PAGE, True)

    return render_template(
        "index.html",
        quantity_form=quantity_form,
        people_data=people_data_paginated,
        current_quantity=len(all_people_data),
    )


@app.route("/new_entry", methods=["GET", "POST"])
def new_entry():
    """Renders the 'new_entry' page of an app, that provides means to users to create an entry manually."""
    new_data_form = EditForm()
    if new_data_form.validate_on_submit():
        DatabaseHandler.create_new_record(new_data_form)
        flash("New entry is successfully added")
        return redirect(url_for("index"))

    return render_template("new_entry.html", new_data_form=new_data_form)


@app.route("/<int:person_id>")
def personal_page(person_id):
    """Renders a personal page of any user with id passed in.

    :param person_id: an id of an existing entry in the database
    :type person_id: int
    """
    person_data = Person.query.get(person_id)

    return render_template("personal_page.html", person_data=person_data)


@app.route("/<int:person_id>/edit", methods=["GET", "POST"])
def edit_personal_page(person_id):
    """Renders a page with means to edit a person's data with id passed in.

    :param person_id: an id of an existing entry in the database
    :type person_id: int
    """
    person_data = DatabaseHandler.get_person_data(person_id)
    edit_form = EditForm(
        first_name=person_data.first_name,
        last_name=person_data.last_name,
        gender=person_data.gender,
        cell=person_data.cell,
        email=person_data.email,
        location=person_data.location,
        pic_link=person_data.pic_link,
    )

    if edit_form.validate_on_submit():
        DatabaseHandler.update_personal_data(person_id, edit_form)
        flash("Data is successfully updated")
        return redirect(url_for("index"))

    return render_template("new_entry.html", new_data_form=edit_form)


@app.route("/random")
def random_person_page():
    """Renders a personal page for a random person from the database."""
    return redirect(
        url_for("personal_page", person_id=DatabaseHandler.generate_random_person_id())
    )


@app.route("/delete/<int:person_id>")
def delete_person_data(person_id):
    """Deletes a person data with person id passed in. Redirects to the homepage then.

    :param person_id: an id of an existing entry in the database
    :type person_id: int
    """
    DatabaseHandler.delete_person(person_id)
    flash("Data entry is successfully deleted")

    return redirect(url_for("index"))


if __name__ == "__main__":
    DatabaseHandler.create_table()
    DatabaseHandler.rerecord_data(1000)
    app.run()
