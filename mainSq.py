import sqlite3


# db = sqlite3.connect("books.db")
# cursor = db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")


#🟡ADD Data
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J.K.', '9.3')")
# db.commit()



#-----------------------------------------------------------------------#
#🟡 SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# initialize the app with the extension
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(30), nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()

#🟡Create A New Record
# with app.app_context():
#     book = Book(title="Spongebob", author='Lolo', rate=3)
#     db.session.add(book)
#     db.session.commit()

#🟡Read All Records
# with app.app_context():
#     result = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
# print(result)

#🟡Update A Particular Record By Query
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.title == 'Spongebob'))
#     book_to_update.title = 'Harry Potter'
#     db.session.commit()

#🟡Update A Record By PRIMARY KEY
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.id == 1)).scalar()
#     book_to_update.title = "Harry Potter"
#     db.session.commit()

#🟡DELETE
# with app.app_context():
#     book_to_delete = db.session.execute(db.select(Book).where(Book.id == 1)).scalar()
#     db.session.delete(book_to_delete)
#     db.session.commit()








