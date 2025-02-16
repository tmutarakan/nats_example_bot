from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        nats=NatsConfig(servers=env.list('NATS_SERVERS'))
    )
