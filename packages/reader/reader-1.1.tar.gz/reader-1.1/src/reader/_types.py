from dataclasses import dataclass
from datetime import datetime
from typing import Generic
from typing import Iterable
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar

from .types import _entry_argument
from .types import _feed_argument
from .types import _namedtuple_compat
from .types import Content
from .types import Enclosure
from .types import Entry
from .types import EntryInput
from .types import Feed
from .types import FeedInput


# Private API
# https://github.com/lemon24/reader/issues/111

# structure similar to
# https://github.com/lemon24/reader/issues/159#issuecomment-612512033


class FeedData(Feed):

    """Future-proofing alias."""

    def as_feed(self) -> Feed:
        """For testing."""
        return Feed(**self.__dict__)


_UpdatedType = TypeVar('_UpdatedType', datetime, Optional[datetime])


@dataclass(frozen=True)
class EntryData(Generic[_UpdatedType], _namedtuple_compat):

    """Like Entry, but .updated is less strict and .feed is missing.

    The natural thing to use would have been generics, but pleasing Python,
    mypy and Sphinx all at the same time is not possible at the moment,
    and the workarounds are just as bad or worse.

    We should be able to use generics once/if this is resolved:
    https://github.com/sphinx-doc/sphinx/issues/7450

    ...however, it may be better to just have entry be a separate
    plain dataclass -- help(Entry) works weird with concrete generics.

    We can't use subclass Entry because the attribute types become less specific.

    We can't use a subclass for the common attributes because it confuses
    Sphinx: https://github.com/sphinx-doc/sphinx/issues/741

    An implementation using generics is available here:
    https://github.com/lemon24/reader/blob/62eb72563b94d78d8860519424103e3c3c1c013d/src/reader/core/types.py#L78-L241

    """

    #: The feed URL.
    feed_url: str

    # WARNING: When changing attributes, keep Entry and EntryData in sync.

    id: str

    # Entries returned by the parser have .updated Optional[datetime];
    # entries sent to the storage always have .updatd set (not optional).
    updated: _UpdatedType

    title: Optional[str] = None
    link: Optional[str] = None
    author: Optional[str] = None
    published: Optional[datetime] = None
    summary: Optional[str] = None
    content: Sequence[Content] = ()
    enclosures: Sequence[Enclosure] = ()

    # TODO: are.read and .important used? maybe delete them if not
    read: bool = False
    important: bool = False

    def as_entry(self, **kwargs: object) -> Entry:
        """For testing."""
        attrs = dict(self.__dict__)
        attrs.pop('feed_url')
        attrs.update(kwargs)
        return Entry(**attrs)


class ParsedFeed(NamedTuple):

    feed: FeedData
    entries: Iterable[EntryData[Optional[datetime]]]
    http_etag: Optional[str] = None
    http_last_modified: Optional[str] = None


class FeedForUpdate(NamedTuple):

    """Update-relevant information about an exiting feed, from Storage."""

    url: str

    #: The date the feed was last updated, according to the feed.
    updated: Optional[datetime]

    http_etag: Optional[str]
    http_last_modified: Optional[str]

    #: Whether the next update should update *all* entries,
    #: regardless of their .updated.
    stale: bool

    #: The date the feed was last updated, according to reader; none if never.
    last_updated: Optional[datetime]


class EntryForUpdate(NamedTuple):

    """Update-relevant information about an existing entry, from Storage."""

    #: The date the entry was last updated, according to the entry.
    updated: datetime


class FeedUpdateIntent(NamedTuple):

    """Data to be passed to Storage when updating a feed."""

    url: str

    #: The time at the start of updating this feed.
    last_updated: datetime

    feed: Optional[FeedData] = None
    http_etag: Optional[str] = None
    http_last_modified: Optional[str] = None


class EntryUpdateIntent(NamedTuple):

    """Data to be passed to Storage when updating a feed."""

    #: The entry.
    entry: EntryData[datetime]

    #: The time at the start of updating this feed (start of update_feed
    #: in update_feed, the start of each feed update in update_feeds).
    last_updated: datetime

    #: The time at the start of updating this batch of feeds (start of
    #: update_feed in update_feed, start of update_feeds in update_feeds);
    #: None if the entry already exists.
    first_updated_epoch: Optional[datetime]

    #: The index of the entry in the feed (zero-based).
    feed_order: int

    @property
    def new(self) -> bool:
        """Whether the entry is new or not."""
        return self.first_updated_epoch is not None


# TODO: these should probably be in storage.py (along with some of the above)


_EFO = TypeVar('_EFO', bound='EntryFilterOptions')


class EntryFilterOptions(NamedTuple):

    """Options for filtering the results of the "get entry" storage methods."""

    feed_url: Optional[str] = None
    entry_id: Optional[str] = None
    read: Optional[bool] = None
    important: Optional[bool] = None
    has_enclosures: Optional[bool] = None

    @classmethod
    def from_args(
        cls: Type[_EFO],
        feed: Optional[FeedInput] = None,
        entry: Optional[EntryInput] = None,
        read: Optional[bool] = None,
        important: Optional[bool] = None,
        has_enclosures: Optional[bool] = None,
    ) -> _EFO:
        feed_url = _feed_argument(feed) if feed is not None else None

        # TODO: should we allow specifying both feed and entry?
        if entry is None:
            entry_id = None
        else:
            feed_url, entry_id = _entry_argument(entry)

        if read not in (None, False, True):
            raise ValueError("read should be one of (None, False, True)")
        if important not in (None, False, True):
            raise ValueError("important should be one of (None, False, True)")
        if has_enclosures not in (None, False, True):
            raise ValueError("has_enclosures should be one of (None, False, True)")

        return cls(feed_url, entry_id, read, important, has_enclosures)
