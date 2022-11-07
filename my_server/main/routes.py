from flask import Blueprint, redirect, render_template, url_for, abort, flash, request, session
from my_server import db_handler as dbh

main = Blueprint('main',__name__, template_folder='templates')

# Main employee list
@main.route('/')
@main.route('/index')
def index():
    values = 'employed.name, employed.phone_nr, department.name'
    table = 'employed JOIN department ON employed.department = department.dept_id'
    employees = dbh.select_sql(values, table)
    if not employees:
        abort(500)
    return render_template('index.html', employees=employees)

# List employees
@main.route('/employees')
def list_empl():
    employees = dbh.select_sql('employed.name, department.name, id', 'employed JOIN department ON employed.department = department.dept_id')
    return render_template('list_empl.html', employees = employees)

@main.route('/employees', methods=['POST'])
def list_empl_post():
    session['update_empl'] = request.form['id']
    return url_for('main.update_empl')

# List departments
@main.route('/departments', methods=['GET'])
def list_dept():
    departments = dbh.select_sql('name, dept_id', 'department')
    return render_template('list_dept.html', departments = departments)

@main.route('/departments', methods=['POST'])
def list_dept_post():
    session['update_dept'] = request.form['id']
    return url_for('main.update_dept')

# Add employee
@main.route('/add-employee')
def add_empl():
    departments = dbh.select_sql('name, dept_id','department')
    employees = dbh.select_sql('name, id','employed')
    return render_template('add_empl.html', employees=employees, departments=departments)

@main.route('/add-employee', methods=['POST'])
def add_empl_post():
    manager = request.form['manager']
    if manager == 'None':
        manager = None
    data = (control_input(request.form['name']), control_input(request.form['phone_nr']), control_input(request.form['salary']), manager, request.form['department'])
    if dbh.command_sql('INSERT INTO employed (name, phone_nr, salary, manager, department) VALUES(?,?,?,?,?)', data):
        flash('A new employee has been added','success')
        return empl_list_redirect()
    abort(500)
    
# Add department
@main.route('/add-department')
def add_dept():
    return render_template('add_dept.html')

@main.route('/add-department', methods=['POST'])
def add_dept_post():
    data = (request.form['id'], control_input(request.form['name']))
    if dbh.command_sql('INSERT INTO department (dept_id, name) VALUES(?,?)', data):
        flash('A new department has been added','success')
        return dept_list_redirect()
    abort(500)

# Update employee
@main.route('/update-employee')
def update_empl():
    if 'update_empl' not in session:
        abort(401)
    empl_id = int(session['update_empl'])
    employees = dbh.select_sql('*','employed')
    exists = False
    for employee in employees:
        if empl_id == employee[0]:
            exists = True
            active_empl = employee
            employees.remove(active_empl)
    if not exists:
        flash('The employee does not exist','warning')
        return empl_list_redirect()
    employees = superiors(empl_id, employees)
    departments = dbh.select_sql('name, dept_id', 'department')
    return render_template('upd_empl.html', departments=departments, employees=employees, active_empl=active_empl)

@main.route('/update-employee', methods=['POST'])
def update_empl_post():
    if 'update_empl' not in session:
        abort(401)
    empl_id = session['update_empl']
    session.pop('update_empl', None)
    manager = request.form['manager']
    if manager == 'None':
        manager = None
    data = (control_input(request.form['name']), control_input(request.form['phone_nr']), control_input(request.form['salary']), manager, request.form['department'], empl_id)
    if not dbh.command_sql('UPDATE employed SET name=?, phone_nr=?, salary=?, manager=?, department=? WHERE id=?', data):
        abort(500)
    flash('The employee has been updated', 'success')
    return empl_list_redirect()

# Update department
@main.route('/update-department')
def update_dept():
    if 'update_dept' not in session:
        abort(401)
    department = dbh.select_with_data('SELECT * FROM department WHERE dept_id=?',(session['update_dept'],))[0]
    if not department:
        abort(500)
    return render_template('upd_dept.html', department=department)

@main.route('/update-department', methods=['POST'])
def update_dept_post():
    if 'update_dept' not in session:
        abort(401)
    dept_id = session['update_dept']
    data = (control_input(request.form['name']), dept_id)
    if dbh.command_sql('UPDATE department SET name = ? WHERE dept_id = ?', data):
        flash('The department has been updated','success')
        return dept_list_redirect()
    abort(500)

# Delete employee
@main.route('/delete-empl', methods=['DELETE'])
def delete_empl():  
    empl_id = int(request.form['id'])
    employees = dbh.select_sql('*','employed')
    if not employees:
        abort(500)
    for employee in employees:
        if empl_id == employee[0]:
            active_empl = employee
            if not upd_direct_sub(active_empl, employees):
                abort(500)
            if dbh.command_sql('DELETE FROM employed WHERE id=?',(empl_id,)):
                flash('The employee has been deleted','info')
                return 'DELETE action was successful'
            else:
                abort(500)
    flash('The employee does not exist','warning')
    return 'DELETE action was unsuccessful'

# Control value for any forbidden characters and remove them
def control_input(value):
    forbidden_chars = ['"', '(', ')', '/', '\\', '\'','-',' ', '{', '}', '[', ']', '=', '?', '.', ',', ';', ':', '_']
    for char in forbidden_chars:
        value = value.replace(char,'')
    return value

#Common redirects
def empl_list_redirect():
    return redirect(url_for('main.list_empl'))
def dept_list_redirect():
    return redirect(url_for('main.list_dept'))

# Recursive algorithm for removing any subordinates from a list of employees
# and returning only superiors or those with no manager at all
def superiors(empl_id, employees):
    for employee in employees:
        if empl_id == employee[4]:
            employees.remove(employee)
            superiors(employee[0], employees)
            superiors(empl_id, employees)
    return employees

# Update any direct subordinates to an employee that is being deleted
# so that their manager is the deleted employees manager instead of NULL 
def upd_direct_sub(active_empl, employees):
    for employee in employees:
        if employee[4] == active_empl[0]:
            if not dbh.command_sql('UPDATE employed SET manager=? WHERE id=?', (active_empl[4], employee[0])):
                return False
    return True