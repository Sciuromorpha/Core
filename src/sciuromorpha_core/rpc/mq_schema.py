from faststream.rabbit import RabbitExchange, RabbitQueue, ExchangeType

# For meta rpc
meta_rpc = RabbitExchange("meta-rpc", type=ExchangeType.DIRECT)

meta_topic = RabbitExchange("meta-broadcast", type=ExchangeType.TOPIC)

# For secret rpc
secret_rpc_exchange = RabbitExchange("secret-rpc", type=ExchangeType.DIRECT)

# For storage rpc
storage_rpc_exchange = RabbitExchange("storage-rpc", type=ExchangeType.DIRECT)
