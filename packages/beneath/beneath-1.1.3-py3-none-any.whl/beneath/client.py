from datetime import timedelta
from collections.abc import Mapping
import os
from typing import Awaitable, Callable, Iterable


from beneath import __version__
from beneath import config
from beneath.stream import Stream
from beneath.admin.models import Models
from beneath.admin.organizations import Organizations
from beneath.admin.projects import Projects
from beneath.admin.secrets import Secrets
from beneath.admin.services import Services
from beneath.admin.streams import Streams
from beneath.admin.users import Users
from beneath.connection import Connection, GraphQLError
from beneath.config import (
  DEFAULT_READ_ALL_MAX_BYTES,
  DEFAULT_READ_BATCH_SIZE,
  DEFAULT_SUBSCRIBE_CONCURRENT_CALLBACKS,
  DEFAULT_SUBSCRIBE_PREFETCHED_RECORDS,
)
from beneath.utils import StreamQualifier


class Client:
  """
  Client for interacting with Beneath.
  Data-plane features are implemented directly on Client, while control-plane features
  are isolated in the `admin` member.
  """

  def __init__(self, secret=None):
    """
    Args:
      secret (str): A beneath secret to use for authentication. If not set, reads secret from ~/.beneath.
    """
    self.connection = Connection(secret=self._get_secret(secret=secret))
    self.admin = AdminClient(connection=self.connection)

  @classmethod
  def _get_secret(cls, secret=None):
    if not secret:
      secret = os.getenv("BENEATH_SECRET", default=None)
    if not secret:
      secret = config.read_secret()
    if not isinstance(secret, str):
      raise TypeError("secret must be a string")
    return secret.strip()

  async def find_stream(self, path: str) -> Stream:
    qualifier = StreamQualifier.from_path(path)
    stream = Stream(client=self, qualifier=qualifier)
    # pylint: disable=protected-access
    await stream._ensure_loaded()
    return stream

  async def stage_stream(
    self,
    path: str,
    schema: str,
    retention: timedelta = None,
    create_primary_instance: bool = True,
  ) -> Stream:
    qualifier = StreamQualifier.from_path(path)
    data = await self.admin.streams.stage(
      organization_name=qualifier.organization,
      project_name=qualifier.project,
      stream_name=qualifier.stream,
      schema_kind="GraphQL",
      schema=schema,
      retention_seconds=retention.seconds if retention else None,
      create_primary_instance=create_primary_instance,
    )
    stream = Stream(client=self, qualifier=qualifier)
    # pylint: disable=protected-access
    await stream._ensure_loaded(prefetched=data)
    return stream

  # EASY HELPERS

  async def easy_read(
    self,
    stream_path: str,
    # pylint: disable=redefined-builtin
    filter: str = None,
    to_dataframe=True,
    batch_size=DEFAULT_READ_BATCH_SIZE,
    max_bytes=DEFAULT_READ_ALL_MAX_BYTES,
    warn_max=True,
  ) -> Iterable[Mapping]:
    stream = await self.find_stream(path=stream_path)
    cursor = await stream.query_index(filter=filter)
    res = await cursor.fetch_all(
      max_bytes=max_bytes,
      batch_size=batch_size,
      warn_max=warn_max,
      to_dataframe=to_dataframe,
    )
    return res

  async def easy_process_once(
    self,
    stream_path: str,
    callback: Callable[[Mapping], Awaitable[None]],
    # pylint: disable=redefined-builtin
    filter: str = None,
    max_prefetched_records=DEFAULT_SUBSCRIBE_PREFETCHED_RECORDS,
    max_concurrent_callbacks=DEFAULT_SUBSCRIBE_CONCURRENT_CALLBACKS,
  ):
    stream = await self.find_stream(path=stream_path)
    cursor = await stream.query_index(filter=filter)
    await cursor.subscribe_replay(
      callback=callback,
      max_prefetched_records=max_prefetched_records,
      max_concurrent_callbacks=max_concurrent_callbacks,
    )

  async def easy_process_forever(
    self,
    stream_path: str,
    callback: Callable[[Mapping], Awaitable[None]],
    max_prefetched_records=DEFAULT_SUBSCRIBE_PREFETCHED_RECORDS,
    max_concurrent_callbacks=DEFAULT_SUBSCRIBE_CONCURRENT_CALLBACKS,
  ):
    stream = await self.find_stream(path=stream_path)
    cursor = await stream.query_index()
    await cursor.subscribe_replay(
      callback=callback,
      max_prefetched_records=max_prefetched_records,
      max_concurrent_callbacks=max_concurrent_callbacks,
    )
    await cursor.subscribe_changes(
      callback=callback,
      max_prefetched_records=max_prefetched_records,
      max_concurrent_callbacks=max_concurrent_callbacks,
    )


class AdminClient:
  """
  AdminClient isolates control-plane features
  """

  def __init__(self, connection: Connection):
    self.connection = connection
    self.models = Models(self.connection)
    self.organizations = Organizations(self.connection)
    self.projects = Projects(self.connection)
    self.secrets = Secrets(self.connection)
    self.services = Services(self.connection)
    self.streams = Streams(self.connection)
    self.users = Users(self.connection)
