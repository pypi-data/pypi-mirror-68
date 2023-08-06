"""Testing cards."""

import logging

import pytest

from mspyteams.card import Card, Section, _CardArray, TeamsWebhookException

_LOGGER = logging.getLogger(__name__)


def test_basic_card(card):
    """Test a basic card on its output."""
    _title = "a title"
    _text = "this is text"
    _summary = "this is a summary"
    expected = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "title": _title,
        "summary": _summary,
        "text": _text,
    }
    card.title = _title
    card.text = _text
    card.summary = _summary

    data = card.card_data()

    assert data == expected


def test_card_fail(card):
    card.title = "A title"
    with pytest.raises(TeamsWebhookException):
        card.card_data()


def test_add_section(card):
    _card_title = "Card title"
    _title = "a title"
    _text = "text"
    expected = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "title": _card_title,
        "text": _text,
        "sections": [{"title": _title}],
    }
    card.title = _card_title
    card.text = _text
    section = Section()
    section.title = _title

    card.add_section(section)

    data = card.card_data()

    assert data == expected


def test_section():
    _fact = ("fact1", 1)
    _title = "a title"

    expected = {"title": _title, "facts": [{"name": _fact[0], "value": _fact[1]}]}

    section = Section()
    section.title = _title
    section.add_fact(*_fact)

    data = section.card_data()
    assert data == expected


@pytest.mark.parametrize(
    "itms,expected",
    [
        ((1, 2, 3), [1, 2, 3]),
        (
            (Section(title="title1"), Section(title="title2")),
            [{"title": "title1"}, {"title": "title2"}],
        ),
        ((Section(title="title1"), "item"), [{"title": "title1"}, "item"]),
    ],
)
def test_card_array(itms, expected):
    card_array = _CardArray()
    for itm in itms:
        card_array.append(itm)

    result = card_array.card_data()

    assert result == expected
