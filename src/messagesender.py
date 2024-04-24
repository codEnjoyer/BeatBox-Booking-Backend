import pika

class MessageSender:
    def __init__(self, rabbitmq_host, rabbitmq_queue):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_queue = rabbitmq_queue

    def send_message(self, recipient_email, subject, body):
        # Соединение с RabbitMQ и отправка сообщения в очередь
        credentials = pika.PlainCredentials('user', 'password')
        parameters = pika.ConnectionParameters(host=self.rabbitmq_host, port=5672, virtual_host='/', credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        
        channel = connection.channel()
        channel.queue_declare(queue=self.rabbitmq_queue, durable=True)
        message = f"{recipient_email}|{subject}|{body}"
        channel.basic_publish(exchange='', routing_key=self.rabbitmq_queue, body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2  # делаем сообщение постоянным (переживающим перезапуск брокера)
                              ))
        print("Message sent to RabbitMQ queue:", message)
        connection.close()

# if __name__ == "__main__": 
#     # Параметры подключения к RabbitMQ
#     rabbitmq_host = 'host.docker.internal'
#     rabbitmq_queue = 'email_queue'

#     message_sender = MessageSender(rabbitmq_host, rabbitmq_queue)

#     # Параметры подключения к SMTP серверу
#     smtp_server = 'smtp.example.com'
#     smtp_port = 587
#     sender_to = ''
#     sender_password = ''

#     # Пример отправки сообщения в нужном формате в очередь
#     message_sender.send_message(sender_to, "Тема письма", "Текст письма")
