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
    data_nascimento = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    cns = db.Column(db.String(20))
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

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

# Rota principal
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

# Novo agendamento
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

# Deletar agendamento
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()
    return redirect(url_for('index'))

# Cadastrar paciente
@app.route('/cadastrar/paciente', methods=['GET', 'POST'])
def cadastrar_paciente():
    if request.method == 'POST':
        novo_paciente = Paciente(
            nome=request.form['nome'],
            data_nascimento=request.form['data_nascimento'],
            cpf=request.form['cpf'],
            cns=request.form.get('cns'),
            endereco=request.form['endereco'],
            telefone=request.form['telefone']
        )
        db.session.add(novo_paciente)
        db.session.commit()
        return redirect(url_for('lista_pacientes'))
    
    return render_template('cadastro.html', tipo='paciente')

# Cadastrar veículo
@app.route('/cadastrar/veiculo', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        novo_veiculo = Veiculo(
            modelo=request.form['modelo'],
            placa=request.form['placa']
        )
        db.session.add(novo_veiculo)
        db.session.commit()
        return redirect(url_for('lista_veiculos'))
    
    return render_template('cadastro.html', tipo='veiculo')

# Excluir paciente
@app.route('/deletar/paciente/<int:id>', methods=['POST'])
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return redirect(url_for('lista_pacientes'))

# Excluir veículo
@app.route('/deletar/veiculo/<int:id>', methods=['POST'])
def deletar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('lista_veiculos'))

# Relatório
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

# Criação das tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
