from flask import Flask, jsonify
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