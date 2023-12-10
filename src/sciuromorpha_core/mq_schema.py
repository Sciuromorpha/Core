from faststream.rabbit import RabbitExchange, RabbitQueue, ExchangeType

# For service status broadcast
service_status = RabbitExchange(
    "service-status", type=ExchangeType.TOPIC, durable=True, auto_delete=False
)

# For meta rpc
meta_rpc = RabbitExchange(
    "meta-rpc", type=ExchangeType.DIRECT, durable=True, auto_delete=False
)

meta_topic = RabbitExchange(
    "meta-topic", type=ExchangeType.TOPIC, durable=True, auto_delete=False
)

# For task rpc
task_rpc = RabbitExchange(
    "task-rpc", type=ExchangeType.DIRECT, durable=True, auto_delete=False
)

task_topic = RabbitExchange(
    "task-topic", type=ExchangeType.TOPIC, durable=True, auto_delete=False
)

# For secret rpc
secret_rpc = RabbitExchange(
    "secret-rpc", type=ExchangeType.DIRECT, durable=True, auto_delete=False
)
