import pika
import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, rabbitmq_host, rabbitmq_queue, smtp_server, smtp_port, sender_email, sender_password):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_queue = rabbitmq_queue
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, body) -> bool:
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            try:
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                return True
            except Exception as e:
                print("Error:", str(e))
                return False
    
    def wait_for_rabbitmq(self):
        url = f"http://{self.rabbitmq_host}:{15672}/api/healthchecks/node"

        while True:
            try:
                response = requests.get(url)
                response.raise_for_status()
                if response.status_code == 200:
                    print("RabbitMQ is ready!")
                    break
            except requests.RequestException:
                print("RabbitMQ is not ready yet. Retrying in 5 second...")
                time.sleep(5)

    def handle_message(self, ch, method, properties, body):
        try:
            # Извлечение данных из сообщения
            # body содержит данные для отправки письма, например, recipient_email, subject, body
            recipient_email, subject, body = body.decode().split('|')

            # Отправка письма
            self.send_email(recipient_email, subject, body)

            print("Email successfully sent to", recipient_email)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error:", str(e))
            # Если возникла ошибка, отправляем сообщение об ошибке в другую очередь с установленным TTL
            ch.basic_publish(exchange='',
                             routing_key='error_queue',
                             body=body,
                             properties=pika.BasicProperties(
                                 expiration='3600'  # TTL в миллисекундах (в данном случае, 1 час)
                             ))
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        # Подключение к RabbitMQ и начало прослушивания очереди
        credentials = pika.PlainCredentials('user', 'password')
        parameters = pika.ConnectionParameters(host=self.rabbitmq_host, port=5672, virtual_host='/', credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=self.rabbitmq_queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.rabbitmq_queue, on_message_callback=self.handle_message)
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

# if __name__ == "__main__": 
#     # Параметры подключения к RabbitMQ
#     rabbitmq_queue = 'email_queue'

#     # Параметры подключения к SMTP серверу
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     sender_email = ''
#     sender_password = ''

#     # Создание экземпляра класса EmailSender
#     email_sender = EmailSender('rabbitmq', rabbitmq_queue, smtp_server, smtp_port, sender_email, sender_password)
#     # Начало прослушивания очереди и обработка сообщений
#     time.sleep(30)
#     #email_sender.wait_for_rabbitmq()
#     email_sender.start_consuming()