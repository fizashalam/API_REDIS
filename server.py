from flask import Flask,request, jsonify
import os 
import redis
redis_host = os.environ.get('REDIS_HOST')
redis_port = int(os.environ.get('REDIS_PORT'))
app = Flask(__name__)
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

data = [
    {'ENO': '1', 'ENAME': 'Amal', 'DNO': '10', 'SALARY': '30000'},
    {'ENO': '2', 'ENAME': 'Shyamal', 'DNO': '30', 'SALARY': '50000'},
    {'ENO': '3', 'ENAME': 'Kamal', 'DNO': '40', 'SALARY': '10000'},
    {'ENO': '4', 'ENAME': 'Nirmal', 'DNO': '50', 'SALARY': '60000'},
    {'ENO': '5', 'ENAME': 'Bimal', 'DNO': '20', 'SALARY': '40000'},
    {'ENO': '6', 'ENAME': 'Parimal', 'DNO': '10', 'SALARY': '20000'}
]
departments = [
    {'DNO': '10', 'DNAME': 'Admin'},
    {'DNO': '20', 'DNAME': 'Accounts'},
    {'DNO': '30', 'DNAME': 'Sales'},
    {'DNO': '40', 'DNAME': 'Marketing'},
    {'DNO': '50', 'DNAME': 'Purchasing'},
]

# Store department data in Redis
for department in departments:
    dname = department['DNAME']
    r.hmset(dname,department)
    
for employee in data:
    eno = employee['ENO']
    r.hmset(eno,employee)


@app.route('/api', methods=['GET'])
def get_data():
    eno= request.args.get('ENO') 
    dname = request.args.get('DNAME')
    if not dname and not eno:
        return jsonify({'error': 'key not found'}), 400   
    if eno:
        employee_details = r.hgetall(eno)
        if not employee_details:
            return jsonify({'error': 'Employee not found'}), 404
        return jsonify(employee_details)
    if dname:
    
        
        print(dname)
        matching_employees = []

        department = r.hgetall(dname)
        print(department)
        print(r.keys('employee:*'))
        for employee_key in r.keys('employee:*'):
            employee_data = r.hgetall(employee_key)
            print(employee_data)
            if employee_data.get('DNO') == department.get('DNO'):
                
                matching_employees.append(employee_data)

        
        if not matching_employees:
            return jsonify({'error': f'No employees found for department "{dname}"'}), 404

    return jsonify(matching_employees)    
                
    


if __name__ == '__main__':
    app.run(debug=True)