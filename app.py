from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_mao_amiga'  # necessária para sessão

# ======== DADOS ========= #
usuarios = {}  # {email: {"nome": "Maria", "senha": "1234"}}

instituicoes = [
    {"nome": "Lar Esperança", "estado": "SP", "municipio": "São Paulo"},
    {"nome": "Casa Solidária", "estado": "SP", "municipio": "Campinas"},
    {"nome": "Amigos do Bem", "estado": "SP", "municipio": "Hortolândia"},
    {"nome": "Sementes do Amor", "estado": "SP", "municipio": "Piracicaba"},
    {"nome": "Abrigo Vida Nova", "estado": "SP", "municipio": "Santos"},
    {"nome": "Amparo Infantil", "estado": "SP", "municipio": "São José dos Campos"},
    {"nome": "Mãos Unidas", "estado": "SP", "municipio": "Ribeirão Preto"},
    {"nome": "Solidariedade SP", "estado": "SP", "municipio": "Sorocaba"},
    {"nome": "Nova Esperança", "estado": "SP", "municipio": "Sumaré"},
    {"nome": "Caminho da Luz", "estado": "SP", "municipio": "Monte Mor"},
    {"nome": "Acolher", "estado": "MG", "municipio": "Belo Horizonte"},
    {"nome": "Sementes do Amor", "estado": "MG", "municipio": "Uberlândia"},
    {"nome": "Vida e Esperança", "estado": "MG", "municipio": "Contagem"},
    {"nome": "Amigos do Bem MG", "estado": "MG", "municipio": "Juiz de Fora"},
    {"nome": "Casa do Coração", "estado": "MG", "municipio": "Betim"},
    {"nome": "Lar da Alegria", "estado": "MG", "municipio": "Montes Claros"},
    {"nome": "Instituto Vida RJ", "estado": "RJ", "municipio": "Rio de Janeiro"},
    {"nome": "Casa Solidária RJ", "estado": "RJ", "municipio": "Niterói"},
    {"nome": "Amparo Carioca", "estado": "RJ", "municipio": "São Gonçalo"},
    {"nome": "Mãos Unidas RJ", "estado": "RJ", "municipio": "Duque de Caxias"},
]

doacoes = []

# ======== ROTAS ========= #
@app.route('/')
def index():
    usuario_logado = session.get('usuario')
    return render_template('index.html', usuario_logado=usuario_logado)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if email in usuarios:
            flash("Esse e-mail já foi cadastrado. Tente outro.", "erro")
            return redirect(url_for('cadastro'))

        usuarios[email] = {"nome": nome, "senha": senha}
        flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if email in usuarios and usuarios[email]["senha"] == senha:
            session['usuario'] = usuarios[email]["nome"]
            flash("Login realizado com sucesso!", "sucesso")
            return redirect(url_for('index'))
        else:
            flash("E-mail ou senha incorretos.", "erro")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da conta.", "info")
    return redirect(url_for('index'))

@app.route('/instituicao', methods=['GET'])
def instituicao():
    estado = request.args.get('estado')
    municipio = request.args.get('municipio')
    resultados = []
    if estado and municipio:
        resultados = [
            i for i in instituicoes
            if i['estado'] == estado and i['municipio'].lower() == municipio.lower()
        ]
    return render_template('instituicao.html', resultados=resultados)

@app.route('/doacao', methods=['GET', 'POST'])
def doacao():
    if request.method == 'POST':
        item = request.form.get('item')
        quantidade = request.form.get('quantidade')
        nome = request.form.get('nome_instituicao')
        data = datetime.now().strftime('%d/%m/%Y %H:%M')

        doacoes.append({
            "nome": nome,
            "item": item,
            "quantidade": quantidade,
            "data": data
        })

        return redirect(url_for('pontos', item=item, quantidade=quantidade))

    return render_template('doacao.html', instituicoes=instituicoes)

@app.route('/pontos')
def pontos():
    tipo = request.args.get('item', '')
    quantidade = request.args.get('quantidade', '')
    return render_template('pontos.html', tipo=tipo, quantidade=quantidade)

@app.route('/historico', methods=['GET'])
def historico():
    total_doacoes = len(doacoes)
    kg_alimentos = sum(int(d['quantidade']) for d in doacoes if d['item'].lower() == 'alimento')
    roupas_doadas = sum(int(d['quantidade']) for d in doacoes if d['item'].lower() == 'roupa')
    familias_atendidas = total_doacoes

    return render_template('historico.html',
                           doacoes=doacoes,
                           total_doacoes=total_doacoes,
                           kg_alimentos=kg_alimentos,
                           roupas_doadas=roupas_doadas,
                           familias_atendidas=familias_atendidas)

@app.route('/somos')
def somos():
    return render_template('somos.html')



if __name__ == '__main__':
    app.run(debug=True)
