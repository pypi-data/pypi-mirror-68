import json
from abc import ABCMeta

from loguru import logger

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

from .ontology import (
    PERFORMATIVE,
    PERFORMATIVE_DEREGISTER_AGENT,
    PERFORMATIVE_DEREGISTER_SERVICE,
    PERFORMATIVE_REGISTER_SERVICE,
    NAME,
    TEAM,
)

LONG_RECEIVE_WAIT: int = 1000000


class AbstractAgent(object, metaclass=ABCMeta):
    def __init__(self, jid, team=0, service_jid="cservice@localhost"):
        self.services = list()
        self._name = jid
        self.team = team
        self.service_jid = service_jid
        self.alive = True

    def start(self, auto_register=True):
        future = Agent.start(self, auto_register=auto_register)
        if self.services:
            for service in self.services:
                logger.info("{} registering service {}".format(self.name, service))
                self.register_service(service)
        return future

    async def die(self):
        await self.deregister_agent()
        self.alive = False
        await self.stop()
        logger.info("Agent {} was stopped.".format(self.name))

    async def send(self, msg):
        if self.is_alive():
            await super().send(msg)

    def register_service(self, service_name):
        class RegisterBehaviour(OneShotBehaviour):
            async def run(self):
                msg = Message(to=self.agent.service_jid)
                msg.set_metadata(PERFORMATIVE, PERFORMATIVE_REGISTER_SERVICE)
                msg.body = json.dumps({NAME: service_name, TEAM: self.agent.team})
                await self.send(msg)

        self.add_behaviour(RegisterBehaviour())

    def deregister_service(self, service_name):
        class DeregisterBehaviour(OneShotBehaviour):
            async def run(self):
                msg = Message(to=self.agent.service_jid)
                msg.set_metadata(PERFORMATIVE, PERFORMATIVE_DEREGISTER_SERVICE)
                msg.body = json.dumps({NAME: service_name, TEAM: self.agent.team})
                await self.send(msg)

        self.add_behaviour(DeregisterBehaviour())

    async def deregister_agent(self):
        class DeregisterAgentBehaviour(OneShotBehaviour):
            async def run(self):
                msg = Message(to=self.agent.service_jid)
                msg.set_metadata(PERFORMATIVE, PERFORMATIVE_DEREGISTER_AGENT)
                await self.send(msg)
                logger.info("Agent {}  stopped sends message to deregister to service agent.".format(self.agent.name))

        behav = DeregisterAgentBehaviour()
        self.add_behaviour(behav)
        await behav.join(timeout=5)

    @property
    def name(self):
        return self._name
