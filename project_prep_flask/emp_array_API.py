from flask import Flask, render_template, jsonify, request

app=Flask(__name__)

#to give our API a little bit of data to work with, we will define an array of employee objects with an ID and name.
employees = [ { 'id': 1, 'name': 'Ashley' }, { 'id': 2, 'name': 'Kate' }, { 'id': 3, 'name': 'Joe' }]


@app.route('/employees',methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employees',methods=['POST'])
def create_employee():
    global nextemployeeID
    employee=json.loads(request.data)
    if not employee_is_valid(employee):
        return jsonify({'error ' : 'Invalis employee properties'}),400
    employee['id']=nextemployeeID
    nextemployeeID+=1
    employees.append(employee)
    return '',201,{'location': f'/employees/{employee["id"]}'}


@app.route('/employees/<int:id>',methods=['PUT'])
def update_employee(id:int):
    employee=get_employees(id)
    if employee is none:
        return jsonify({'error':'Invalid employee id'}),400
    employee.update(update_employee)
    return jsonify(employee)


@app.route('/employees/<int:id>',methods=['DELETE'])
def delete_employee(id:int ):
    global emp
    emp=get_employees(id:int)
    if employee is none:
        return jsonify({'error':'Invalid employee id'}),400
    employees = [e for e in employees if e['id'] != id]
    return jsonify(employee),200    


if __name__=='__main__':
    app.run(port=5000)