"""
Module encapsulating message structure to facilitate use with the Consumer and Producer wrappers
"""
from dataclasses import asdict
import json
from typing import Union, Iterable

import pydantic

__all__ = ["message_class", "MessageValidationException"]


class MessageValidationException(Exception):
    """
    Exception raised when a message cannot be parsed
    """


def message_class(routing_key: str, queues: Union[Iterable[str], None] = None, **kwargs):
    """
    Standard lib dataclasses.dataclass like decorator for creating message classes
    :param routing_key: Routing key of the message e.g. message.m
    :param queues: Iterable of queue names to bind the routing key to e.g. [message.q,message2.q]
    :param kwargs: keyword arguments passed through to the pydantic.dataclasses.dataclass function
    :return: A pydantic.dataclasses.dataclass for the Message with the following methods
        - routing_key() : returns the str routing key
        - binding(): returns a list of dicts specifying the routing key to queue binding
        - from_dict(body: dict): Convert a dict message body to Message instance
        - from_bytes(body: bytes): Convert a bytes message body to Message instance
        - dict(**kwargs): Convert a dict message body to Message instance
    """
    def to_dict(self, **kwargs):
        """
        convert dataclass instance to a dict
        :param kwargs: keyword arguments passed through to the dataclasses.asdict function
        :return: dict of the instance
        """
        return asdict(self, **kwargs)

    @classmethod
    def from_dict(cls, body: dict):
        """
        Convert a dict message body to Message instance
        :param body: The string body of the message to parse into a Message instance
        :return: instance of the message class
        :raises: MessageValidationException, TypeError
        """
        if not isinstance(body, dict):
            raise TypeError("Message must be a dict to validate schema")
        valid_args = {k: v for k, v in body.items() if k in cls.__dataclass_fields__.keys()}
        try:
            return cls(**valid_args)
        except (UnicodeDecodeError, TypeError, ValueError) as e:  # Catch parsing Failure
            raise MessageValidationException("Message schema validation failed") from e

    @classmethod
    def from_bytes(cls, body: bytes):
        """
        Convert a bytes message body to Message instance
        :param body: The string body of the message to parse into a Message instance
        :return: instance of the message class
        :raises: MessageValidationException
        """
        try:
            # convert to dict
            body = json.loads(body)
            # validate against schema definition
            message = cls.from_dict(body)
        except (UnicodeDecodeError, TypeError, ValueError) as e:  # Catch parsing Failure
            raise MessageValidationException("Message schema validation failed") from e
        return message

    if queues is None:
        queues = list()

    def decorator(cls):
        """
        Decorator implementation for the message class
        """

        @classmethod
        def routing_key_method(cls):
            return routing_key

        @classmethod
        def binding_method(cls):
            return [{'routing_key': cls.routing_key(), 'bound_queue': q} for q in queues]
        MessageClass = pydantic.dataclasses.dataclass(cls, **kwargs)
        MessageClass.routing_key = routing_key_method
        MessageClass.binding = binding_method
        MessageClass.dict = to_dict
        MessageClass.from_dict = from_dict
        MessageClass.from_bytes = from_bytes

        return MessageClass
    return decorator
