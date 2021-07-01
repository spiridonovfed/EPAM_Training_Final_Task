from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from persons_table import db
from persons_table.models import DatabaseHandler, Person
from persons_table.persons.forms import EditForm, QuantityForm

from ..config import ENTRIES_PER_PAGE

persons = Blueprint("persons", __name__)


@persons.route("/", methods=["GET", "POST"])
@persons.route("/index", methods=["GET", "POST"])
@persons.route("/index/<int:page>", methods=["GET", "POST"])
def index(page=1):
    """Renders the index page of the app.

    :param page: a page number, defaults to 1
    :type page: int, optional
    """
    quantity_form = QuantityForm()
    if quantity_form.validate_on_submit():
        new_quantity = quantity_form.quantity.data
        DatabaseHandler.rerecord_data(new_quantity)
        return redirect(url_for("persons.index"))

    db_query_object = DatabaseHandler.all_records_query()
    people_data_paginated = db_query_object.paginate(page, ENTRIES_PER_PAGE, True)

    return render_template(
        "index.html",
        quantity_form=quantity_form,
        people_data=people_data_paginated,
        current_quantity=DatabaseHandler.count_entries(),
    )


@persons.route("/new_person", methods=["GET", "POST"])
def new_entry():
    """Renders the 'new_entry' page of an app, that provides means to users to create an entry manually."""
    new_data_form = EditForm()
    if new_data_form.validate_on_submit():
        DatabaseHandler.create_new_record(new_data_form)
        flash("New entry is successfully added")
        return redirect(url_for("persons.index"))

    return render_template("new_entry.html", new_data_form=new_data_form)


@persons.route("/person/<int:person_id>")
def personal_page(person_id):
    """Renders a personal page of any user with id passed in.

    :param person_id: an id of an existing entry in the database
    :type person_id: int
    """
    person_data = Person.query.get(person_id)

    return render_template("personal_page.html", person_data=person_data)


@persons.route("/edit-person/<int:person_id>", methods=["GET", "POST"])
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
        return redirect(url_for("persons.index"))

    return render_template("new_entry.html", new_data_form=edit_form)


@persons.route("/random")
def random_person_page():
    """Renders a personal page for a random person from the database."""
    return redirect(
        url_for(
            "persons.personal_page",
            person_id=DatabaseHandler.generate_random_person_id(),
        )
    )


@persons.route("/delete-person/<int:person_id>")
def delete_person_data(person_id):
    """Deletes a person data with person id passed in. Redirects to the homepage then.

    :param person_id: an id of an existing entry in the database
    :type person_id: int
    """
    DatabaseHandler.delete_person(person_id)
    flash("Data entry is successfully deleted")

    return redirect(url_for("persons.index"))
