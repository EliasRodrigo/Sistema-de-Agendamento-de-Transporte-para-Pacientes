from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agendamentos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos do banco de dados
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(20), nullable=False)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    destino = db.Column(db.String(200), nullable=False)

    paciente = db.relationship('Paciente', backref=db.backref('agendamentos', lazy=True))
    veiculo = db.relationship('Veiculo', backref=db.backref('agendamentos', lazy=True))

# Rota principal para exibir os agendamentos
@app.route('/')
def index():
    agendamentos = Agendamento.query.all()
    return render_template('index.html', agendamentos=agendamentos)

# Rota para listar pacientes
@app.route('/pacientes')
def lista_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

# Rota para listar veículos
@app.route('/veiculos')
def lista_veiculos():
    veiculos = Veiculo.query.all()
    return render_template('veiculos.html', veiculos=veiculos)

# Rota para adicionar um novo agendamento
@app.route('/novo', methods=['GET', 'POST'])
def novo_agendamento():
    pacientes = Paciente.query.all()
    veiculos = Veiculo.query.all()
    
    if request.method == 'POST':
        novo_agendamento = Agendamento(
            data=request.form['data'],
            hora=request.form['hora'],
            paciente_id=request.form['paciente_id'],
            veiculo_id=request.form['veiculo_id'],
            destino=request.form['destino']
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('form.html', pacientes=pacientes, veiculos=veiculos)

# Rota para excluir um agendamento
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()
    return redirect(url_for('index'))

# Rota para cadastrar pacientes
@app.route('/cadastrar/paciente', methods=['GET', 'POST'])
def cadastrar_paciente():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_paciente = Paciente(nome=nome)
        db.session.add(novo_paciente)
        db.session.commit()
        return redirect(url_for('lista_pacientes'))
    
    return render_template('cadastro.html', tipo='paciente')

# Rota para cadastrar veículos
@app.route('/cadastrar/veiculo', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        modelo = request.form['modelo']
        placa = request.form['placa']
        novo_veiculo = Veiculo(modelo=modelo, placa=placa)
        db.session.add(novo_veiculo)
        db.session.commit()
        return redirect(url_for('lista_veiculos'))
    
    return render_template('cadastro.html', tipo='veiculo')

# Rota para excluir um paciente
@app.route('/deletar/paciente/<int:id>', methods=['POST'])
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return redirect(url_for('lista_pacientes'))

# Rota para excluir um veículo
@app.route('/deletar/veiculo/<int:id>', methods=['POST'])
def deletar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('lista_veiculos'))

@app.route('/relatorio')
def relatorio():
    total_agendamentos = Agendamento.query.count()
    total_pacientes = Paciente.query.count()
    total_veiculos = Veiculo.query.count()

    agendamentos = Agendamento.query.all()

    return render_template('relatorio.html', 
        total_agendamentos=total_agendamentos, 
        total_pacientes=total_pacientes, 
        total_veiculos=total_veiculos, 
        agendamentos=agendamentos
    )


# Criar tabelas no banco de dados (execute uma vez)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
