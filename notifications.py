import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
def send_email(subject, body, sender_email, sender_password, recipient_email):
    # Cria a mensagem
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Adiciona o corpo do email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conecta ao servidor SMTP do Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Usa TLS para segurança
        server.login(sender_email, sender_password)  # Faz login no servidor
        text = msg.as_string()  # Converte a mensagem para string
        server.sendmail(sender_email, recipient_email, text)  # Envia o email
        server.quit()  # Encerra a conexão
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

