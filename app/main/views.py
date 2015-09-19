from flask import session, redirect, url_for, render_template
from flask.ext.login import current_user
from . import main
from ..models import Room
from .forms import AddRoomForm
from app import db

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/rooms')
def rooms():
    rooms = [Room('Main', 'General room for all users.')]
    if current_user.is_authenticated():
        rooms.extend(Room.query.all())
    return render_template('rooms.html', rooms=rooms)

@main.route('/chat')
def chat():
    name = session.get('name', '')
    session['room'] = 'main_room'

    if not name:
        name = current_user.username
        session['name'] = name

    if name == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room='main_room')

@main.route('/chat/<room>')
def custom_chat(room):
    name = session.get('name', '')
    if not name:
        name = current_user.username
        session['name'] = name

    room = room
    session['room'] = room
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)

@main.route('/chat/add', methods=['GET', 'POST'])
def add_room():
    error = ''
    if current_user.is_authenticated():
        form = AddRoomForm()
        if form.validate_on_submit():
            room = Room(name=form.name.data, description=form.description.data)
            db.session.add(room)
            db.session.commit()
            return redirect(url_for('main.rooms'))
        else:
            return render_template('add_room.html', form=form, error=error)
    else:
        return redirect(url_for('auth.login'))