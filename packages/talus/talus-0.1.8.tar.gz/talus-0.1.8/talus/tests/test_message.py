"""
Unit tests for message parsing
"""
import json

import pytest

from talus.message import (
    message_class,
    MessageValidationException,
)


@message_class(routing_key="example.m", queues=["example1.q", "example2.q"])
class OutboundMessage:
    s: str
    i: int
    f: float
    d: str = "default"


@message_class(routing_key="example.m")
class InboundMessage:
    s: str
    i: int
    f: float
    d: str = "default"


@pytest.fixture(params=["inbound", "outbound"])
def MessageClass(request):
    message_classes = {
        "inbound": InboundMessage,
        "outbound": OutboundMessage
    }
    return message_classes[request.param]


@pytest.fixture(params=['all', 'all_required', 'coerce_int', 'coerce_float', 'coerce_str'])
def valid_message_body(request) -> dict:
    message_bodies = {
        "all": {"s": "s", "i": 1, "f": 1.1, "d": "d"},
        "all_required": {"s": "s", "i": 1, "f": 1.1},
        "coerce_int": {"s": "s", "i": "1", "f": 1.1},
        "coerce_float": {"s": "s", "i": 1, "f": "1.1"},
        "coerce_str": {"s": 1, "i": 1, "f": 1.1},
    }
    return message_bodies[request.param]


def test_valid_message_from_bytes(valid_message_body, MessageClass):
    """
    Given: valid message body
    When: parsing the message
    Then: Get a a valid message instance
    """
    body = json.dumps(valid_message_body).encode('utf-8')
    message = MessageClass.from_bytes(body)
    assert message.s == str(valid_message_body['s'])
    assert message.i == int(valid_message_body['i'])
    assert message.f == float(valid_message_body['f'])
    assert message.d == str(valid_message_body.get('d', 'default'))
    assert message.routing_key() == "example.m"
    if isinstance(message, OutboundMessage):
        assert message.binding() == [
            {
                "routing_key": "example.m",
                "bound_queue": "example1.q"
            },
            {
                "routing_key": "example.m",
                "bound_queue": "example2.q"
            },
        ]


@pytest.fixture(params=["bytes", "string", "missing_required"])
def invalid_message_body(request) -> dict:
    message_bodies = {
        "bytes": b"bytes string",
        "string": "just a string",
        "missing_required": json.dumps({"i": "1", "f": 1.1}).encode('utf-8'),
    }
    return message_bodies[request.param]


def test_invalid_message_from_bytes(invalid_message_body, MessageClass):
    """
    Given: invalid message body
    When: body is parsed
    Then: MessageValidationException is raised
    """
    with pytest.raises(MessageValidationException):
        MessageClass.from_bytes(invalid_message_body)


def test_message_dict(MessageClass):
    """
    Given: valid dict message body
    When: message instance is created dict
    Then: message instance dict method returns the input dict
    """
    body = {"s": "s", "i": 1, "f": 1.1, "d": "d"}
    message = MessageClass.from_dict(body)
    assert message.dict() == body
