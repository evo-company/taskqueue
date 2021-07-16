from typing import List

from strictconf import Section, Compose, Key

from .logging import LoggingSection


class Main(LoggingSection, Section):
    kafka_hosts = Key('kafka-hosts', List[str])
    kafka_group = Key('kafka-group', str)


class Config(Compose):
    main = Main('main')
