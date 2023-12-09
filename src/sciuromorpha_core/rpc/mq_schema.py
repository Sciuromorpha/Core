from faststream.rabbit import RabbitExchange, RabbitQueue, ExchangeType

# For meta rpc
meta_rpc = RabbitExchange("meta-rpc", type=ExchangeType.DIRECT)

meta_topic = RabbitExchange("meta-broadcast", type=ExchangeType.TOPIC)

# For task rpc
task_rpc = RabbitExchange("task-rpc", type=ExchangeType.DIRECT)

task_topic = RabbitExchange("task-broadcast", type=ExchangeType.TOPIC)

# For secret rpc
secret_rpc = RabbitExchange("secret-rpc", type=ExchangeType.DIRECT)

# For storage rpc
storage_rpc = RabbitExchange("storage-rpc", type=ExchangeType.DIRECT)
