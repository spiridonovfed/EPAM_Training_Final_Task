from persons_table import create_app
from persons_table.models import DatabaseHandler

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        DatabaseHandler.create_table()
        DatabaseHandler.rerecord_data(1000)
    app.run()
