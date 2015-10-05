from flask import session, redirect, url_for, render_template, request, jsonify, current_app
from flask.ext.login import current_user, login_required
from . import main
from ..models import Room, Message
from .forms import AddRoomForm
from app import db
import string
from flask.ext.cors import cross_origin
from functools import wraps

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/rooms')
@login_required
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
    if not current_user.is_authenticated():
        return redirect(url_for('.index'))
    name = session.get('name', '')
    session['room'] = 'Main'

    if not name:
        name = current_user.username
        session['name'] = name

    if name == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room='Main')


@main.route('/chat/add', methods=['GET', 'POST'])
@login_required
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
@login_required
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

@main.route('/_history_search')
@login_required
def history_search():
    query = request.args.get('query')
    if not query:
        return jsonify(error="Something went wrong...")

    valid_sq = " ".join([elem.strip(string.punctuation) for elem in query.split(' ')[:10]]).strip(' ')
    msg_search_and = Message.query.whoosh_search(valid_sq).all()
    msg_search_or = Message.query.whoosh_search(valid_sq, or_=True).all()

    messages = []

    messages.extend(msg_search_and)
    for msg in msg_search_or:
        if msg not in messages:
            messages.append(msg)

    data = []

    for msg in messages:
        data.append({"msg": msg.user + ": " + msg.text})

    if len(data) == 0:
        return jsonify(error="No results...")

    return jsonify(result=data[:20])

@main.route('/chat/<room>', methods=['GET', 'POST'])
@login_required
@cross_origin()
def custom_chat(room):
    if not current_user.is_authenticated():
        return redirect(url_for('.index'))
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

@main.before_request
def beforeRequest():
    requestUrl = request.url
    https = 'https' in requestUrl
    if https == False:
        secureUrl = requestUrl.replace('http://','https://')
        secureUrl = secureUrl.replace('ws://','wss://')
        return redirect(secureUrl)