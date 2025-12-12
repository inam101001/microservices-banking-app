import pika
import json
import logging
from typing import Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    def __init__(self, host='rabbitmq', port=5672, username='admin', password='changeme'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchange
            self.channel.exchange_declare(
                exchange='banking_events',
                exchange_type='topic',
                durable=True
            )
            logger.info("Connected to RabbitMQ successfully")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def publish_message(self, routing_key: str, message: Dict[Any, Any]):
        """Publish a message to RabbitMQ"""
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()
            
            # Add timestamp to message
            message['timestamp'] = datetime.utcnow().isoformat()
            
            self.channel.basic_publish(
                exchange='banking_events',
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            logger.info(f"Published message to {routing_key}: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    def close(self):
        """Close the connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")

class RabbitMQConsumer:
    def __init__(self, host='rabbitmq', port=5672, username='admin', password='changeme'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchange
            self.channel.exchange_declare(
                exchange='banking_events',
                exchange_type='topic',
                durable=True
            )
            logger.info("Connected to RabbitMQ successfully")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def setup_queue(self, queue_name: str, routing_key: str):
        """Setup a queue and bind it to the exchange"""
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()
            
            # Declare queue
            self.channel.queue_declare(queue=queue_name, durable=True)
            
            # Bind queue to exchange
            self.channel.queue_bind(
                exchange='banking_events',
                queue=queue_name,
                routing_key=routing_key
            )
            logger.info(f"Queue {queue_name} setup with routing key {routing_key}")
        except Exception as e:
            logger.error(f"Failed to setup queue: {e}")
            raise

    def start_consuming(self, queue_name: str, callback):
        """Start consuming messages from the queue"""
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()
            
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback
            )
            
            logger.info(f"Started consuming from queue: {queue_name}")
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Failed to start consuming: {e}")
            raise

    def stop_consuming(self):
        """Stop consuming messages"""
        if self.channel:
            self.channel.stop_consuming()

    def close(self):
        """Close the connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")
