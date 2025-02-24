from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class NatsDelayedConsumerConfig:
    subject: str
    stream: str
    durable_name: str


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig
    delayed_consumer: NatsDelayedConsumerConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        nats=NatsConfig(servers=env.list('NATS_SERVERS')),
        delayed_consumer=NatsDelayedConsumerConfig(
            subject=env('NATS_DELAYED_CONSUMER_SUBJECT'),
            stream=env('NATS_DELAYED_CONSUMER_STREAM'),
            durable_name=env('NATS_DELAYED_CONSUMER_DURABLE_NAME')
        )
    )
