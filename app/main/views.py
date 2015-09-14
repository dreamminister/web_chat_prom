from flask import session, redirect, url_for, render_template, request
from flask.ext.login import current_user
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/rooms')
def rooms():
    rooms = ['main_room']
    if current_user.is_authenticated():
        rooms.append('new_room')
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