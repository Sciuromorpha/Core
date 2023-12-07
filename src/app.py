from .settings import Settings
from faststream import ContextRepo, FastStream, Context
from faststream.rabbit import RabbitBroker

broker = RabbitBroker()
app = FastStream(broker)


@app.on_startup
async def setup(context: ContextRepo, env: str = ".env"):
    settings = Settings(_env_file=env)
    context.set_global("settings", settings)
    await broker.connect(settings.rabbit)


@app.on_startup
async def connect_db(settings: Settings = Context()):
    pass
