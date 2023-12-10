from faststream.rabbit import RabbitExchange, RabbitQueue, ExchangeType

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

# For storage rpc
storage_rpc = RabbitExchange(
    "storage-rpc", type=ExchangeType.DIRECT, durable=True, auto_delete=False
)
