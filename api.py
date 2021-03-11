from flask import Flask, request, jsonify, abort, make_response
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

#DATABASE SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audios.sqlite3'
db = SQLAlchemy(app)

#ENTRYING MODEL
class songs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_of_song = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, name_of_song, duration):
        self.name_of_song = name_of_song
        self.duration = duration

    def __repr__(self):
        return f"songs('{self.name_of_song}', '{self.uploaded_time}')"

    def to_dict(self):
        data = {
            'id': self.id,
            'name_of_song': self.name_of_song,
            'duration': self.duration,
            'uploaded_time': self.uploaded_time.isoformat() + 'Z'
        }
        return data

class podcasts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_podcast = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    host =  db.Column(db.String(100), nullable=False)
    participants =  db.Column(db.String(100), nullable=True)
    def __init__(self, name_of_podcast, duration, host, participants):
        self.name_of_podcast = name_of_podcast
        self.duration = duration
        self.host = host
        self.participants = participants
    def __repr__(self):
        return f"podcasts('{self.name_of_podcast}', '{self.uploaded_time}')"

    def to_dict(self):
        data = {
            'id': self.id,
            'name_of_podcast': self.name_of_podcast,
            'duration': self.duration,
            'uploaded_time': self.uploaded_time.isoformat() + 'Z',
            'host': self.host,
            'participants': self.participants
        }
        return data

class audiobooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_of_audiobook = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __init__(self, title_of_audiobook, author, narrator, duration):
        self.title_of_audiobook = title_of_audiobook
        self.author = author
        self.narrator = narrator
        self.duration = duration
    def __repr__(self):
        return f"audiobooks('{self.title_of_audiobook}', '{self.uploaded_time}')"
    
    def to_dict(self):
        data = {
            'id': self.id,
            'title_of_audiobook': self.title_of_audiobook,
            'author': self.author,
            'narrator': self.narrator,
            'duration': self.duration,
            'uploaded_time': self.uploaded_time.isoformat() + 'Z'
            
        }
        return data


#ENTRYING API ROUTES
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome!</h1>
<p>This is a web API that simulates the behavior of an audio file server</p>'''

@app.route('/api/v1/resources/<string:audio_type>', defaults={'audio_id': -1}, methods=['GET'])
@app.route('/api/v1/resources/<string:audio_type>/<int:audio_id>', methods=['GET'])
def api_get(audio_type, audio_id):
    if audio_type.lower() not in ["song", "podcast", "audiobook"]:
        abort(404)
    if audio_type == 'song':
        if audio_id != -1:
            song = songs.query.get_or_404(audio_id).to_dict()
            if len(song) == 0:
                abort(404)
            return jsonify(song)
        all_song = [item.to_dict() for item in songs.query.all()]
        return jsonify(all_song)

    elif(audio_type == 'podcast'):
        if audio_id != -1:
            podcast = podcasts.query.get_or_404(audio_id).to_dict()
            if len(podcast) == 0:
                abort(404)
            return jsonify(podcast)
        all_podcast = [item.to_dict() for item in podcasts.query.all()]
        return jsonify(all_podcast)

    else:
        if audio_id != -1:
            audiobook = audiobooks.query.get_or_404(audio_id).to_dict()
            if len(audiobook) == 0:
                abort(404)
            return jsonify(audiobook)
        all_audiobook = [item.to_dict() for item in audiobooks.query.all()]
        return jsonify(all_audiobook)


@app.route('/api/v1/resources/<string:audio_type>/<int:audio_id>', methods=['PUT'])
def api_udpate(audio_type, audio_id):
    if audio_type.lower() not in ["song", "podcast", "audiobook"]:
        abort(404)
    if not request.json:
        abort(400)

    if audio_type == "song":
        song = songs.query.get_or_404(audio_id)
        if request.json['duration'] < 0:
            abort(400)
        song.name_of_song = request.json['name_of_song']
        song.duration = request.json['duration']
        db.session.commit()
        return jsonify(song.to_dict())

    elif(audio_type == "podcast"):
        podcast = podcasts.query.get_or_404(audio_id)
        if request.json['duration'] < 0:
            abort(400)
        podcast.name_of_podcast = request.json['name_of_podcast']
        podcast.duration = request.json['duration']
        podcast.host = request.json['host']
        podcast.participants = request.json['participants']
        db.session.commit()
        return jsonify(podcast.to_dict())

    else:
        audiobook = audiobooks.query.get_or_404(audio_id)
        if request.json['duration'] < 0:
            abort(400)
        audiobook.title_of_audiobook = request.json['title_of_audiobook']
        audiobook.author = request.json['author']
        audiobook.narrator = request.json['narrator']
        audiobook.duration = request.json['duration']
        db.session.commit()
        return jsonify(audiobook.to_dict())

@app.route('/api/v1/resources/<string:audio_type>', methods=['POST'])
def api_create(audio_type):
    if audio_type.lower() not in ["song", "podcast", "audiobook"]:
        abort(404)
    if not request.json:
        abort(400)
    if audio_type == "song":
        if "name_of_song" not in request.json and "duration" not in request.json:
            abort(400)
        if request.json['duration'] < 0:
            abort(400)
        song = songs(
            request.json['name_of_song'],
            request.json['duration']
        )
        db.session.add(song)
        db.session.commit()       
        return jsonify(song.to_dict())
    elif (audio_type == "podcast"):
        if "name_of_podcast" not in request.json and "duration" not in request.json and "host" not in request.json:
            abort(400)
        podcast = podcasts(
            request.json['name_of_podcast'],
            request.json['duration'],
            request.json['host'],
            request.json['participants']
            #paticipants = [data['participant1'],data['participant2'],data['participant3']]
        )
        db.session.add(podcast)
        db.session.commit()       
        return jsonify(podcast.to_dict())

    else:
        if "title_of_audiobook" not in request.json and "author" not in request.json and "narrator" not in request.json and "duration" not in request.json:
            abort(400)
        audiobook = audiobooks(
            request.json['title_of_audiobook'],
            request.json['author'],
            request.json['narrator'],
            request.json['duration']
        )
        db.session.add(audiobook)
        db.session.commit()       
        return jsonify(audiobook.to_dict())

@app.route('/api/v1/resources/<string:audio_type>/<int:audio_id>', methods=['DELETE'])
def api_delete(audio_type, audio_id):
    if audio_type.lower() not in ["song", "podcast", "audiobook"]:
        abort(404)
    if audio_type == "song":
        song = songs.query.get_or_404(audio_id)
        db.session.delete(song)
        db.session.commit()
        return jsonify(song.to_dict())

    elif (audio_type == "podcast"):
        podcast = podcasts.query.get_or_404(audio_id)
        db.session.delete(podcast)
        db.session.commit()
        return jsonify(podcast.to_dict())
    
    else: 
        audiobook = audiobooks.query.get_or_404(audio_id)
        db.session.delete(audiobook)
        db.session.commit()
        return jsonify(audiobook.to_dict())

if __name__ == '__main__':
   db.create_all()
app.run(debug = True)