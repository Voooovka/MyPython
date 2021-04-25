from os import abort
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Djkjlz2003@localhost:3306/studentdb'

ma = Marshmallow(app)
db = SQLAlchemy(app)


class ConstractionProfessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avg_salary = db.Column(db.Integer)
    education = db.Column(db.String(30))
    type_of_work = db.Column(db.String(30))
    instruments = db.Column(db.String(30))

    def __init__(self, avg_salary, education, type_of_work, instruments):
        self.avg_salary = avg_salary
        self.education = education
        self.type_of_work = type_of_work
        self.instruments = instruments


class ConstractionProfessionsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'avg_salary', 'education', 'type_of_work', 'instruments')
    id = fields.Int()
    avg_salary = fields.Integer()
    education = fields.Str()
    type_of_work = fields.Str()
    instruments = fields.Str()


constraction_profession_scheme = ConstractionProfessionsSchema()
constraction_professions_scheme = ConstractionProfessionsSchema(many=True)


@app.route('/professions', methods=['GET'])
def get_all_professions():
    all_professions = ConstractionProfessions.query.all()
    result = constraction_professions_scheme.dump(all_professions)
    return jsonify(result)


@app.route('/professions/<id>', methods=['GET'])
def get_profession(id):
    profession = ConstractionProfessions.query.get(id)
    if not profession:
        return abort(404)
    return constraction_profession_scheme.jsonify(profession)


@app.route('/professions', methods=['POST'])
def add_profession():

    data = constraction_profession_scheme.load(request.json)
    profession = ConstractionProfessions(**data)
    db.session.add(profession)
    db.session.commit()
    return constraction_profession_scheme.jsonify(profession)


@app.route('/professions/<id>', methods=['PUT'])
def update_profession(id):
    profession = ConstractionProfessions.query.get(id)
    if not profession:
        abort(404)
    profession.avg_salary = request.json["avg_salary"]
    profession.education = request.json["education"]
    profession.type_of_work = request.json["type_of_work"]
    profession.instruments = request.json["instruments"]
    db.session.commit()

    return constraction_profession_scheme.jsonify(profession)


@app.route('/professions/<id>', methods=['DELETE'])
def delete_profession(id):
    profession = ConstractionProfessions.query.get(id)
    if not profession:
        abort(404)
    db.session.delete(profession)
    db.session.commit()

    return constraction_profession_scheme.jsonify(profession)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

