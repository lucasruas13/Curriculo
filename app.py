from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from config import email, senha

app = Flask(__name__)
app.secret_key = "lrcode"

# Configurando serviço de envio de e-mail
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": email,
    "MAIL_PASSWORD": senha
}

app.config.update(mail_settings)
mail = Mail(app)

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

# Páginas do site
@app.route('/')
def index():
    return render_template('index.html')

# Configurando mensagem de envio de e-mail
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )

        msg = Message(
            subject = f"{formContato.nome} te enviou uma mensagem no Portfólio",
            sender = app.config.get("MAIL_USERNAME"),
            recipients = ["lucas_ruas@hotmail.com", app.config.get("MAIL_USERNAME")],
            body = f"""

            {formContato.nome} te enviou um e-mail pelo endereço {formContato.email}, com o seguinte conteúdo:

            {formContato.mensagem}

            """
        )
        mail.send(msg)
        flash("Mensagem enviada com sucesso!")
    return redirect('/')


# Colocando o site no ar
if __name__ == '__main__':
    app.run(debug=True)
