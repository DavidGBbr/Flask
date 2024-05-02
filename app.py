from flask import Flask, jsonify, abort, make_response
from evento import Evento
from evento_online import EventoOnline

ev_online = EventoOnline("Live de Python")
ev2_online = EventoOnline("Live de JavaScript")
ev = Evento("Aula de Python","Rio de Janeiro")
eventos = [ev_online, ev2_online, ev]

app = Flask(__name__)

@app.route('/')
def index():
  return '<h1>Hello, World!!!!</h1>'

@app.route('/api/eventos/')
def get_eventos():
  eventos_dict = []
  for ev in eventos:
    eventos_dict.append(ev.__dict__)
  return jsonify(eventos_dict)

@app.errorhandler(404)
def not_found(error):
  return (jsonify(erro=str(error)), 404)

@app.route('/api/eventos/<int:id>/')
def get_evento(id):
  for ev in eventos:
    if ev.id == id:
      return jsonify(ev.__dict__)
  
  abort(404,"Evento não encontrado")