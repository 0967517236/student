from bson import ObjectId
from flask import Flask, jsonify
from flask import request

from model import table_student
from validate.student_validate import StudentCreateSchema, StudentUpdateSchema

app = Flask(__name__)
PREFIX_API = "/api/v1{}"
port = 8000


@app.route(PREFIX_API.format('/students'), methods=['GET'])
def students():
    list_student = table_student.find()
    list_student = list(list_student)
    for student in list_student:
        student['_id'] = str(student['_id'])  # ép kiểu từ ObjectId sang String
    return jsonify(list_student)


@app.route(PREFIX_API.format('/students'), methods=['POST'])
def add_student():
    body = request.get_json()
    # check value
    try:
        student_schema = StudentCreateSchema()
        student_schema.load(body)
    except Exception as err:
        return jsonify({'code:': 1, 'message': list(err.args)[0]}), 400

    # save document student to table_student
    result_insert = table_student.insert_one(body)
    student_id = str(result_insert.inserted_id)

    # return data insert and id student in data
    body['_id'] = student_id
    return jsonify(body)


@app.route(PREFIX_API.format('/students/<student_id>'), methods=['PUT'])
def update_student(student_id):
    # get data student to body with content type application/json
    body = request.get_json()

    # validate student_id
    if not student_id:
        return jsonify({'code': 1, 'message': 'Param invalid'}), 400

    # validate data body
    student_schema = StudentUpdateSchema()
    try:
        student_schema.load(body)
    except Exception as err:
        return jsonify({"code": 1, "message": list(err.args)[0]}), 400

    # check exists student by id
    student = table_student.find_one(ObjectId(student_id), {'_id': 1})
    if student:
        # update data student from body
        result_update = table_student.update_one({'_id': ObjectId(student_id)}, {'$set': body})

        # mapping data update student old
        student.update(body)

        # convert ObjectId primary Mongodb to string uuid
        student['_id'] = str(student.get('_id', student_id))

        # return data student update
        return jsonify(student), 200
    # check student not found -> return err not found student
    return jsonify({'code': 1, 'message': 'Student not found!!!'}), 404


@app.route(PREFIX_API.format('/students/<student_id>'), methods=['DELETE'])
def remove_animal(student_id):
    list_student = table_student.find()
    list_student = list(list_student)
    if not student_id:
        return jsonify({"code": 1, "message": "Param invalid"}), 400
    student_del = table_student.find_one(ObjectId(student_id), {"_id": 1})
    for student in list_student:
        student['_id'] = str(student['_id'])
        if student['_id'] == student_id:
            del student_del['_id']
            return jsonify({'Mess: ': 'Delete successfully'})
        return jsonify({'Mess: ': 'Not Found'})
    return jsonify({"code": 1, "message": "student not found!"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
