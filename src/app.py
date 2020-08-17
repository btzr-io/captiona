from flask import Flask, request, jsonify
from tasks import searchTextTracks

server = Flask(__name__)

@server.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@server.route('/')
def hello_world():
    return { "version": "0.0.1", "status": "ok" }

@server.route('/text_tracks/<string:claim_id>',  methods=['GET'])
def get_text_tracks(claim_id):
    language = request.args.get('lang')
    text_tracks = searchTextTracks(claim_id, None, language)
    return { "text_tracks": text_tracks }

# Run on localhost (development version)
if __name__ == "__main__":
    server.run(debug=True)
