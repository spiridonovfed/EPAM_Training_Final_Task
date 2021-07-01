from random import random

import requests

from persons_table import db


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


# --------- Creating a class to handle the database ---------------- #


def get_API_response(quantity):
    """Collects data from API Randomuser.me.

    :param quantity: requested number of entries in data to collect
    :type quantity: int

    :return: collected data
    :rtype: dict
    """

    url = "https://randomuser.me/api/"
    parameters = {
        "inc": "gender, name, cell, email, location, picture",
        "results": quantity,
    }
    response = requests.get(url, params=parameters)
    return response.json()


def serialize_API_data(API_data):
    """Converts collected data from API to a list of Person objects.

    :param API_data: collected data from API
    :type API_data: dict

    :return: list of Person objects
    :rtype: list[Person(db.Model), ...]
    """

    input_for_db = []

    for person_data in API_data:
        person_object = Person(
            gender=person_data["gender"],
            first_name=person_data["name"]["first"],
            last_name=person_data["name"]["last"],
            cell=person_data["cell"],
            email=person_data["email"],
            location=f"{person_data['location']['city']}, {person_data['location']['country']}",
            pic_link=person_data["picture"]["large"],
        )
        input_for_db.append(person_object)

    return input_for_db


def bulk_insert_into_db(input_for_db):
    """Conducts bulk insert into the database

    :param input_for_db: list of Person objects
    :type input_for_db:list[Person(db.Model), ...]
    """
    db.session.bulk_save_objects(input_for_db)
    db.session.commit()


class DatabaseHandler:
    """This is a class to wrap all working with database functionality.
    Can be used without instances."""

    @staticmethod
    def create_table():
        """Creates Person table in the database if there is none"""
        db.create_all()

    @staticmethod
    def rerecord_data(quantity_requested):
        """Delete all the data in the Person table and inserts a new data.
        All the data is collected with help of randomuser.me API.
        Parameter 'quantity' determines the number of entries of a new data.

        :param quantity_requested: a number of records needed in a new dataset in the database
        :type quantity_requested: int
        """

        current_quantity = db.session.query(Person).count()
        if quantity_requested < current_quantity:
            entry_start_delete_from = (
                db.session.query(Person)
                .order_by(Person.id)
                .offset(quantity_requested)
                .first()
            )
            db.session.query(Person).filter(
                Person.id >= entry_start_delete_from.id
            ).delete()
            db.session.commit()
        elif quantity_requested > current_quantity:
            API_data_to_insert = get_API_response(
                quantity_requested - current_quantity
            )["results"]
            input_for_db = serialize_API_data(API_data_to_insert)
            bulk_insert_into_db(input_for_db)

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
    def count_entries():
        """Counts a number of entries in the Person table of database

        :return: a number of entries in the Person table of database
        :rtype: int
        """
        return db.session.query(Person).count()

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
