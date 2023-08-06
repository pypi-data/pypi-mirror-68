"""Card items."""


class TeamsWebhookException(Exception):
    """custom exception for failed webhook call"""

    pass


KEY_TITLE = "title"
KEY_TEXT = "text"
KEY_SUMMARY = "summary"
KEY_SECTIONS = "sections"
KEY_FACTS = "facts"

__all__ = ["Card", "Section"]


class TeamData:
    """Base class for TeamData"""

    def __init__(self):
        self.data = {}

    def card_data(self):
        """Return a dict which can be sent to the Teams webhook."""
        new_data = {}
        for key, value in self.data.items():
            try:
                new_data[key] = value.card_data()
            except AttributeError:
                new_data[key] = value

        return new_data


class _CardArray:
    """A list which implements the card_data method."""

    def __init__(self):
        self._items = []

    def append(self, item):
        self._items.append(item)

    def card_data(self) -> list:
        itms = []
        for itm in self._items:
            try:
                itms.append(itm.card_data())
            except AttributeError:
                itms.append(itm)
        return itms


class _CardProperty:
    """Property descriptor for the card properties."""

    def __init__(self, name):
        self._name = name

    def __get__(self, obj, objtype):
        return obj.data.get(self._name, None)

    def __set__(self, obj, val):
        obj.data[self._name] = val


class Section(TeamData):
    """A card section"""

    title = _CardProperty(KEY_TITLE)
    text = _CardProperty(KEY_TEXT)

    def __init__(self, title=None):
        super().__init__()
        if title:
            self.title = title

    def add_fact(self, name, value):
        """Add a fact to this section."""
        try:
            facts = self.data[KEY_FACTS]
        except:
            facts = _CardArray()
            self.data[KEY_FACTS] = facts
        facts.append({"name": name, "value": value})


class Card(TeamData):
    """A Card."""

    title = _CardProperty(KEY_TITLE)
    text = _CardProperty(KEY_TEXT)
    summary = _CardProperty(KEY_SUMMARY)

    def __init__(self):
        super().__init__()
        self.data["@type"] = "MessageCard"
        self.data["@context"] = "https://schema.org/extensions"

    def card_data(self):
        if self.text is None and self.summary is None:
            raise TeamsWebhookException("You need to provide either text or a summary")
        return super().card_data()

    def add_section(self, section: Section):
        """Add a section to the card."""
        try:
            sections = self.data[KEY_SECTIONS]
        except KeyError:
            sections = _CardArray()
            self.data[KEY_SECTIONS] = sections
        sections.append(section)
