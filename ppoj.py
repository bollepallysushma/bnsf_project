from flask import Flask, render_template, render_template_string, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DataError, IntegrityError
import sqlite3
import json
from sqlalchemy import CHAR, text



app = Flask(__name__)
db = sqlite3.connect('/Users/sushmabollepally/Desktop/project/project.db')
cur = db.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/sushmabollepally/Desktop/project/project.db'
db = SQLAlchemy(app)


'''def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db = None
    try:
        db = sqlite3.connect('/Users/sushmabollepally/Desktop/project/project.db')
    except Error as e:
        print(e)

    return db

def create_project(db, contact):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """

   # sql =  ( Insert into contact ('id','name','phone','email') VALUES(contact.id,contact.name,contact.phone,contact.email)  ) # type: ignore
    
    cur = db.cursor()
    cur.execute( "Insert into contact ('id','name','phone','email') VALUES(contact.id,contact.name,contact.phone,contact.email)")
    db.commit()
    return cur.lastrowid'''

       

## create model for the app
class Contact(db.Model):
    # columns to be added in the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.CHAR(100), nullable=False)
    phone = db.Column(db.CHAR(20), nullable=False)
    email = db.Column(db.CHAR(120), nullable=False)
    def __repr__(self):
        return "<Contact {}: {}>".format(self.id,self.name )


'''
def main():
    database = '/Users/sushmabollepally/Desktop/project/project.db'

    

    # create a database connection
    db = create_connection(database)
    with db:
        # create a new project
        contact = ('abc', '0987654321', 'abc@gmail.com')
        #project_id = create_project(db, project)

        # tasks
        #task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        #task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
'''

#from flask_marshmallow import Marshmallow
'''from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        include_relationships = True
        load_instance = True'''


# create above mentioned columns with the Table
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload')
def contacts():
    return render_template("upload.html")

@app.route('/retrieve')
def retrive():
    return render_template("retrieve.html")

# @app.route('/retrieve?')
# def retrive_data():
#     return render_template("retrieve_data.html")

#### Get all contacts list ####
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    # db.session.execute()
    return jsonify([{'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email} for contact in contacts])

##### Add a contact in the table
@app.route('/contacts', methods=['POST'])

def add_contact():
    #data = json.load(open('address_book.json', encoding='utf-8'))
    # data = request.get_json()
    data = str(request.data)
    data= data.replace("\\r", "")
    data= data.replace("\\n", " ")
    data = data.replace("'", "")
    data= data.strip()
    data = data.split(" ")

    data= [i.split("=")[1] for i in data]

    print("data ******** : \n", data)
    contact = Contact(name=data[0], phone=data[1], email=data[2])
    
    db.session.add(contact)
    db.session.commit()

    #cur.execute("Insert into contact ('id' ,'name','phone' ,'email') VALUES(?,?,?,?)"),("contact.id","contact.name","contact.phone","contact.email")
    #db.commit()
    #cur = db.cursor()
    #db.session.execute  ( "Insert into contact ('id' ,'name','phone' ,'email') VALUES(?,?,?,?)"),("contact.id","contact.name","contact.phone","contact.email")
    #db.session.execute("SELECT * from contact")
    #db.session.commit()
    #db.session.close()
    
    return {'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email}
    #return db.lastrowid
    #db.session.commit()

    


'''
    import sys

    class recursionlimit:
        
        def __init__(self, limit):
            self.limit = limit

        def __enter__(self):
            self.old_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(self.limit)

        def __exit__(self, type, value, tb):
            sys.setrecursionlimit(self.old_limit)

        @staticmethod
        def generatecode():
            pass 
    
    with contact(1500):
        print(db.session.add(add_contact(1000, 0)))


    from sqlalchemy import exc
    try:
        with db.session.begin_nested():
            #db.session.add(add_contact())
            #db.session.flush()
            db.session.commit()
            

    except exc.IntegrityError:
        pass
        cursor = db.cursor()
        cursor.execute(''''''SELECT * from contact'''''')
        db.session.rollback()
        #db.session.commit()
       

    #db.session.commit()
   
    return {'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email}
    #return render_template("upload.html", contact=contact)'''
    
'''def read_address_book():
        with open('address_book.json') as f:
            address_book = json.load(f)
            return address_book

    def add_to_address_book(name, phone, email):
        address_book = read_address_book()
        new_contact = {"name": name, "phone": phone, "email": email}
        address_book.append(new_contact)
        with open('address_book.json', 'w') as f:
            json.dump(address_book, f)'''


###### Modify a Record in the Table
@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.get_json()
    contact = Contact.query.get_or_404(id)
    contact.name = data['name']
    contact.phone = data['phone']
    contact.email = data['email']
    db.session.commit()
    return {'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email}

###### Delete a record in the Table
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return {'message': 'Contact deleted'}

if __name__ == '__main__':
   app.run(debug=True)

#if __name__ == '__main__':
 #   main()
