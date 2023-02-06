from flask import Flask,request,jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('disneycharacters', user='isaac', password='iamstan', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Characters(BaseModel):
  name = CharField()
  fullName = CharField()
  active = BooleanField()
  currentVoice = CharField()
  originalDesigner = CharField()

db.connect()
db.drop_tables([Characters])
db.create_tables([Characters])

Characters(name = "Mickey Mouse", fullName = 'Michel Mouse', active = True, currentVoice = 'Bret Iwan', originalDesigner = 'Walt Disney').save()
Characters(name = "Goofy", fullName = 'Goofy Goof', active = True, currentVoice = 'Bill Farmer', originalDesigner = 'Art Babbitt').save()
Characters(name = "Donald Duck", fullName = 'Donald Fauntleroy Duck', active = True, currentVoice = 'Tony Anselmo', originalDesigner = 'Art Babbitt').save()
Characters(name = "Minnie Mouse", fullName = 'Minerva Mouse', active = True, currentVoice = 'Kaitlyn Robrock', originalDesigner = 'Ub Iwerks').save()
Characters(name = "Daisy Duck", fullName = 'Daisy Duck', active = True, currentVoice = 'N/A', originalDesigner = 'Paul Rudish').save()
Characters(name = "Pluto", fullName = 'Pluto the Pup', active = True, currentVoice = 'Bill Farmer', originalDesigner = 'Walt Disney').save()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome To The Disney Character Api!!! To begin, use route "/api".'

@app.route('/api/', methods=['GET', 'POST'])
@app.route('/api/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Characters.get(Characters.id == id)))
    else:
        char_list = []
        for char in Characters.select():
            char_list.append(model_to_dict(char))
        return jsonify(char_list)

  if request.method =='PUT':
    body = request.get_json()
    Characters.update(body).where(Characters.id == id).execute()
    return f"Disney Dude {str(id)} updated."

  if request.method == 'POST':
    new_character = dict_to_model(Characters, request.get_json())
    new_character.save()
    return jsonify(model_to_dict(new_character))

  if request.method == 'DELETE':
    Characters.delete().where(Characters.id == id).execute()
    return f"Disney Dude {str(id)} deleted."

app.run(port=3030, debug=True)