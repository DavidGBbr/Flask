from flask import Flask, jsonify, abort, request, json
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

@app.route('/api/eventos/', methods=['POST'])
def create_evento():
  data = json.loads(request.data)
  nome = data.get('nome')
  local = data.get('local')

  if not nome:
    abort(400, "'nome' precisa ser informado! ")

  if local:
    evento = Evento(nome=nome, local=local)
  else:
    evento = EventoOnline(nome=nome)

  eventos.append(evento)
  return {
    "id": evento.id,
    "url": f"/api/eventos/{evento.id}"
  }

@app.errorhandler(400)
def bad_request(error):
  return (jsonify(erro=str(error)), 400)

@app.errorhandler(404)
def not_found(error):
  return (jsonify(erro=str(error)), 404)

def find_evento_or_404(id):
  for ev in eventos:
    if ev.id == id:
      return ev
  
  abort(404,"Evento não encontrado")

@app.route('/api/eventos/<int:id>/')
def get_evento(id):
  ev = find_evento_or_404(id)
  return jsonify(ev.__dict__)

@app.route('/api/eventos/<int:id>/', methods=['DELETE'])
def delete_evento(id):
  for ev in eventos:
    ev = find_evento_or_404(id)
    eventos.remove(ev)
    return jsonify(id=id)

@app.route('/api/eventos/<int:id>/', methods=['PUT'])
def edit_evento(id):
  data = request.get_json()
  nome = data.get('nome')
  local = data.get('local')

  if not nome:
    abort(400, "'nome' precisa ser informado! ")

  if not local:
    abort(400, "'local' precisa ser informado! ")

  ev = find_evento_or_404(id)
  ev.nome = nome
  ev.local = local

  return jsonify(ev.__dict__)

@app.route('/api/eventos/<int:id>/', methods=['PATCH'])
def edit_partial_evento(id):
  data = request.get_json()
  ev = find_evento_or_404(id)

  if "nome" in data.keys():
    nome = data.get('nome')
    if not nome:
      abort(400, "'nome' precisa ser informado! ")
    ev.nome = nome
  
  if "local" in data.keys():
    local = data.get('local')
    if not local:
      abort(400, "'local' precisa ser informado! ")
    ev.local = local

  return jsonify(ev.__dict__)