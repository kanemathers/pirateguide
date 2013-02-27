import re
import json

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy.types import TypeDecorator

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base      = declarative_base()

class BaseMixins(object):

    @classmethod
    def all(cls):
        return DBSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()

    def save(self, flush=False):
        DBSession.add(self)

        if flush:
            DBSession.flush()

    def delete(self):
        DBSession.delete(self)

class JSONEncodedDict(TypeDecorator):

    impl = Unicode

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)

        return value

class Movies(Base, BaseMixins):

    __tablename__ = 'movies'

    id         = Column(Integer, primary_key=True)
    tmdb_id    = Column(Integer, unique=True, index=True)
    path       = Column(Text)
    tmdb_cache = Column(JSONEncodedDict, default=None)

    def __init__(self, tmdb_id, path):
        self.tmdb_id = tmdb_id
        self.path    = path

    def __json__(self, request):
        return {
            'id':      self.id,
            'tmdb_id': self.tmdb_id,
            'path':    self.path,
            'info':    self.tmdb_cache,
        }

    @classmethod
    def by_path(cls, path):
        return DBSession.query(cls).filter(cls.path == path).first()

    @staticmethod
    def clean_filename(filename, blacklist=None):
        if not blacklist:
            blacklist = []

        filename = re.sub(r"[^a-z0-9'$&]", ' ', filename.lower())
        rip      = filename.rfind('rip')

        if rip != -1:
            filename = filename[:rip].strip()
            end      = re.search(r'[\W]', filename[::-1])

            if end:
                filename = filename[:-end.start()].strip()

        filename = filename.split()

        for i, word in enumerate(filename[:]):
            if word in blacklist:
                filename = filename[:i]

                break

        # blacklist might wipe out all the words
        if not filename:
            return None

        if len(filename) > 1 and re.search(r'(19\d\d|20\d\d)', filename[-1]):
            filename.pop()

        return ' '.join(filename)
