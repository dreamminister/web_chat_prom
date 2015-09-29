from flask import session, redirect, url_for, render_template, request
from flask.ext.login import current_user
from . import main
from ..models import Room, Message
from .forms import AddRoomForm
from app import db
import string

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/rooms')
def rooms():
    rooms = []
    if current_user.is_authenticated():
        q_rooms = Room.query.all()

        if len(q_rooms) == 0:
            general_room = Room('Main', 'General room for all users.')
            db.session.add(general_room)
            db.session.commit()

        rooms.extend(Room.query.all())
    return render_template('rooms.html', rooms=rooms)

@main.route('/chat')
def chat():
    name = session.get('name', '')
    session['room'] = 'Main'

    if not name:
        name = current_user.username
        session['name'] = name

    if name == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room='Main')

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

    history = Message.query.filter_by(room=room).limit(20).all()

    return render_template('chat.html', name=name, room=room, history=history)

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


@main.route('/room/search', methods=['POST'])
def room_search():
    error = ''
    if not request.form.get('search_query'):
        error = "Please provide the search query."
    else:
        search_query = request.form.get('search_query')
        # First, let's strip our sq off punctuation signs and limit it to 10 words.
        valid_sq = " ".join([elem.strip(string.punctuation) for elem in search_query.split(' ')[:10]]).strip(' ')

        # Now search for our sq in books and authors (cause it may be either). Search with AND & OR conjunctions.
        room_search_and = Room.query.whoosh_search(valid_sq).all()
        room_search_or = Room.query.whoosh_search(valid_sq, or_=True).all()

        # Now combine the results of AND/OR searches.
        # Note: the order matters, results are ranked by relevance in Whoosh.
        rooms = []

        rooms.extend(room_search_and)
        for room in room_search_or:
            if room not in rooms:
                rooms.append(room)

        return render_template('room_search.html',
                               rooms=rooms, sq=search_query)
    return render_template('room_search.html', error=error)