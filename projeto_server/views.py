from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Server
from dao import ServerDao, UserDao
import time
from helpers import delete_file, recovery_image
from server_monitor import db, app


server_dao = ServerDao(db)
user_dao = UserDao(db)

@app.route('/')
def index():
    if 'active_login' not in session or session['active_login'] == None:
            return redirect(url_for('login'))
    list = server_dao.list()
    return render_template('list.html', titulo='Manage Registered Linux Servers', servers=list)

@app.route('/cpu_load', methods=['GET', 'POST'])
def cpu_load():
        
        loadavg = {} 
        f = open("/proc/loadavg") 
        con = f.read().split() 
        f.close() 
        a = loadavg['lavg_1']=con[0] 
        b = loadavg['lavg_5']=con[1] 
        c = loadavg['lavg_15']=con[2] 
        #d = loadavg['nr']=con[3] 
        #e = loadavg['last_pid']=con[4] 
        newArray = [a, b, c]
        cpl = newArray
        return render_template('output.html',cpl = cpl)
        

@app.route('/monitor/<int:id>')
def system_monitoring(id):
    if 'active_login' not in session or session['active_login'] == None:
            return redirect(url_for('login', next=url_for('monitor')))
    server = server_dao.search_by_id(id)
    name_image = recovery_image(id)
    return render_template('monitor.html', titulo='Monitoring Linux Server Status', server=server
                            , server_pic=name_image)
    
@app.route('/configure/<int:id>')
def system_configure(id):
    if 'active_login' not in session or session['active_login'] == None:
            return redirect(url_for('login', next=url_for('monitor')))
    server = server_dao.search_by_id(id)
    name_image = recovery_image(id)
    return render_template('manage.html', titulo='Configure Linux Server Services', server=server
                            , server_pic=name_image)
    
@app.route('/new')
def new():
    if 'active_login' not in session or session['active_login'] == None:
        return redirect(url_for('login', proxima=url_for('new')))
    return render_template('new.html', titulo='New Server')


@app.route('/create', methods=['POST',])
def create():
    name = request.form['name']
    ip_address = request.form['ip_address']
    category = request.form['category']
    server = Server(name, ip_address, category)
    server = server_dao.save(server)

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    file.save(f'{upload_path}/pic{server.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'active_login' not in session or session['active_login'] == None:
        return redirect(url_for('login', next=url_for('edit')))
    server = server_dao.search_by_id(id)
    
    name_image = recovery_image(id)
    if name_image == None:
        return render_template('edit.html', titulo='Edit Linux Server Information', server=server
                           , server_pic=name_image or 'default_picture.jpg')
    else:
        return render_template('edit.html', titulo='Edit Linux Server Information', server=server
                               , server_pic=name_image)


@app.route('/update', methods=['POST',])
def update():
    name = request.form['name']
    ip_address = request.form['ip_address']
    
    category = request.form['category']
    id = request.form['id']
    server = Server(name, ip_address, category, id)
    server_dao.save(server)

    server_picture = request.form['server_picture']

    if server_picture == 'None':
        return redirect(url_for('index'))
    else:
        file = request.files['file']
        upload_path = app.config['UPLOAD_PATH']
        timestemp = time.time()
        delete_file(server.id)
        file.save(f'{upload_path}/pic{server.id}-{timestemp}.jpg')
        return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    server_dao.delete(id)
    flash('All informations about server are removed')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/autenticate', methods=['POST', ])
def autenticate():
    user = user_dao.search_by_id(request.form['user'])
    if user:
        if user.password == request.form['password']:
            session['active_login'] = user.id
            flash(user.id + ' ' + user.name + ' successfully authenticated!')
            next_page = request.form['next']
            return redirect(next_page)
        else:
            flash('Unauthorized Access!!!')
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['active_login'] = None
    flash('No users logged in. Please Login to manage servers.')
    return redirect(url_for('login'))


@app.route('/uploads/<file_name>')
def image(file_name):
    return send_from_directory('uploads', file_name)