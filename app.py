from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask import request

from flask import Flask, render_template
import enum
from flask_marshmallow import Marshmallow, Schema, fields, ValidationError



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ma = Marshmallow(app)

class ItemEnum(enum.Enum):
    book = "book"
    pen = 'pen'
    folder = "folder"
    bag = 'bag'
    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default="pending")
    items = db.Column(db.Enum(ItemEnum), nullable=False)
    
    def __init__(self,items):

        self.items = items
        
class TodoSchemas(ma.Schema):
    class Meta:
        fields = ('id', 'status', 'items',)

todo_schema = TodoSchemas()
todo_schemas = TodoSchemas(many=True)


@app.route('/post', methods = ['POST'])
def add_items():
    
    
    items = request.json['items']
    my_items = Todo(items)
    try:
        db.session.add(my_items)
        db.session.commit()
        return todo_schema.jsonify(my_items)
            
        
    except Exception:
        return "successfully added", 200





@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        items = request.form['items']
        new_task = Todo(items = items)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            
            return redirect('/'), 200
        except Exception:
            print("there was an issue adding ur items")
        
    else:
        tasks = Todo.query.order_by(Todo.id).all()
        return render_template('index.html', tasks=tasks), 200
    

