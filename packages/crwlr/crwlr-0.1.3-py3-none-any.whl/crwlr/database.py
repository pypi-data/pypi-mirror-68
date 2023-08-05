#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import time
from uuid import uuid4

from sqlalchemy import Column, Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import create_engine, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from crwlr.helper import name_from, get_fact_key
from crwlr.statics import WARN, CRIT, DB_INSERT_LANGUAGES, DB_INSERT_TAG_EXCAVATION, DB_INSERT_TAG_PHASE, \
    DB_INSERT_TAG_FACET, DB_DATE_ID_FMT, DATA_SOURCE_SCOPUS, INFO, DB_SELECT_DIM_AUTHOR, \
    DB_SELECT_DIM_MEDIUM, DB_SELECT_FACT_KEYS, DB_SELECT_FACT_TITLES, CONNECT_DATABASE, INITIALIZE_DATABASE, \
    INSERT_DIM_LANG, INSERT_DIM_DATE, INSERT_DIM_TAG, CREATE_INDEX, DATA_SOURCE_CROSSREF
from crwlr.types import Log

Base = declarative_base()


class DLang(Base):
    __tablename__ = 'dim_lang'
    lang = Column(String(512), unique=True, primary_key=True)
    mysql_engine = 'MyISAM'


class DDate(Base):
    __tablename__ = 'dim_date'
    date = Column(String(32), unique=True, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    mysql_engine = 'MyISAM'


class DMedium(Base):
    __tablename__ = 'dim_medium'
    id = Column(String(128), primary_key=True)
    name = Column(String(1024))
    type_short = Column(String(8))
    type_long = Column(String(256))
    mysql_engine = 'MyISAM'


class DAuthor(Base):
    __tablename__ = 'dim_author'
    id = Column(String(128), primary_key=True)
    given_name = Column(String(1024))
    surname = Column(String(1024))
    indexed_name = Column(String(1024))
    auid = Column(String(1024))
    afid = Column(String(1024))
    affiliation_name = Column(String(2048))
    city = Column(String(1024))
    country = Column(String(1024))
    mysql_engine = 'MyISAM'


class DReference(Base):
    __tablename__ = 'dim_reference'
    id = Column(String(128), primary_key=True)
    pub_id = Column(String(128))
    ref_id = Column(String(128))
    title = Column(String(2048))
    year = Column(Integer)
    authors = Column(String(4096))
    fulltext = Column(String(4096))
    mysql_engine = 'MyISAM'


class DTag(Base):
    __tablename__ = 'dim_tag'
    id = Column(String(128), primary_key=True)
    tag_excavation = Column(String(128))
    tag_phase = Column(String(128))
    tag_facet = Column(String(128))
    mysql_engine = 'MyISAM'


class FPublication(Base):
    __tablename__ = 'fact_publication'
    doi = Column(String(2048))
    title_primary = Column(String(4096))
    relevance = Column(Integer, default=-1)
    abstract = Column(Text)
    db = Column(String(512))
    url = Column(String(4096))
    lang_id = Column(String(128), primary_key=True)
    date_id = Column(String(128), primary_key=True)
    author_id = Column(String(128), primary_key=True)
    medium_id = Column(String(128), primary_key=True)
    reference_id = Column(String(128))
    tag_id = Column(String(128))
    mysql_engine = 'MyISAM'


class MalformedPublication(Base):
    __tablename__ = 'malformed_publication'
    timestamp = Column(BigInteger, primary_key=True, autoincrement=True)
    eid = Column(String(128), primary_key=True)
    doi = Column(String(128), primary_key=True)
    action = Column(String(128))
    source = Column(String(128))
    reason = Column(Text)
    severity = Column(Integer)
    mysql_engine = 'MyISAM'


def connect_database(conn):
    global engine, connection

    Log.debug(None, CONNECT_DATABASE, 'Database connection attempt')
    engine = create_engine(conn)
    connection = engine.connect()
    Log.debug(None, CONNECT_DATABASE, 'Connected to database')


def initialize_database():
    # start with a fresh and clean db
    Log.info(None, INITIALIZE_DATABASE, '020: drop all tables')
    Base.metadata.drop_all(engine)
    Log.info(None, INITIALIZE_DATABASE, '--- init db: START ---')
    Log.info(None, INITIALIZE_DATABASE, '030; create tables')
    Base.metadata.create_all(engine)
    Log.info(None, INITIALIZE_DATABASE, '040; insert master data')
    insert_dim_lang()
    insert_dim_date()
    insert_dim_tag()
    create_index()
    Log.info(None, INITIALIZE_DATABASE, '---- init db: END ----')


def insert_dim_lang():
    # we should only receive eng and ger
    # but we want to be on the safe side here
    bulk_load([DLang(lang=i) for i in DB_INSERT_LANGUAGES])
    Log.info(None, INSERT_DIM_LANG, '041; insert languages')


def insert_dim_date():
    # we look at the past 20 years (2000-2019)
    years = range(2000, 2020)
    months = range(1, 13)

    dates = []

    for m in months:
        for y in years:
            dates.append(DDate(date=DB_DATE_ID_FMT.format(m, y), year=y, month=m))
    bulk_load(dates)
    Log.info(None, INSERT_DIM_DATE, '042; insert dates')


def insert_dim_tag():
    l_dtag = []
    for fac in DB_INSERT_TAG_FACET:
        for ph in DB_INSERT_TAG_PHASE:
            for exc in DB_INSERT_TAG_EXCAVATION:
                id_ = str(uuid4())
                l_dtag.append(DTag(id=id_, tag_excavation=exc, tag_phase=ph, tag_facet=fac))

    bulk_load(l_dtag)
    Log.info(None, INSERT_DIM_TAG, '043; insert tags')


def bulk_load(l_dbobj: list):
    """Bulk load list of database objects in db

    Shall bulk insert a list of database objects to database.

    :param l_dbobj: a list ob database objects
    :return: None
    """
    session = Session(bind=engine)
    session.bulk_save_objects(l_dbobj)
    session.commit()


def create_index():
    i_title = Index("title_fulltext", FPublication.title_primary, mysql_prefix='FULLTEXT')
    i_abstract = Index("abstract_fulltext", FPublication.abstract, mysql_prefix='FULLTEXT')
    i_title.create(engine)
    i_abstract.create(engine)
    Log.info(None, CREATE_INDEX, '044: create index')


def _get_malformed(eid, doi, reason, action, source, severity):
    millis = round(time() * 1000)
    return MalformedPublication(timestamp=millis, eid=eid, doi=doi, reason=reason, action=action, source=source,
                                severity=severity)


def malf_scopus_crit(reason, action, eid='', doi=''):
    return get_malformed_crit(eid=eid, doi=doi, reason=reason, action=action, source=DATA_SOURCE_SCOPUS)


def malf_scopus_warn(reason, action, eid='', doi=''):
    return get_malformed_warn(eid=eid, doi=doi, reason=reason, action=action, source=DATA_SOURCE_SCOPUS)


def malf_crossref_crit(reason, action, eid='', doi=''):
    return get_malformed_crit(eid=eid, doi=doi, reason=reason, action=action, source=DATA_SOURCE_CROSSREF)


def malf_crossref_warn(reason, action, eid='', doi=''):
    return get_malformed_warn(eid=eid, doi=doi, reason=reason, action=action, source=DATA_SOURCE_CROSSREF)


def malf_crossref_info(reason, action, eid='', doi=''):
    return get_malformed_info(eid=eid, doi=doi, reason=reason, action=action, source=DATA_SOURCE_CROSSREF)


def get_malformed_crit(reason, action, source, eid='', doi=''):
    return _get_malformed(eid=eid, doi=doi, reason=reason, action=action, source=source, severity=CRIT)


def get_malformed_warn(reason, action, source, eid='', doi=''):
    return _get_malformed(eid=eid, doi=doi, reason=reason, action=action, source=source, severity=WARN)


def get_malformed_info(reason, action, source, eid='', doi=''):
    return _get_malformed(eid=eid, doi=doi, reason=reason, action=action, source=source, severity=INFO)


def all_authors():
    with engine.connect() as con:
        rs = con.execute(DB_SELECT_DIM_AUTHOR)
        return rs.fetchall()


def all_media():
    with engine.connect() as con:
        rs = con.execute(DB_SELECT_DIM_MEDIUM)
        return rs.fetchall()


def all_fact_keys():
    with engine.connect() as con:
        rs = con.execute(DB_SELECT_FACT_KEYS)
        return rs.fetchall()


def all_fact_titles():
    with engine.connect() as con:
        rs = con.execute(DB_SELECT_FACT_TITLES)
        return rs.fetchall()


class DedupSingleton:
    class Dedup:

        @staticmethod
        def fact_sets():
            rs = all_fact_keys()
            f_ = set()
            t_ = set()
            d_ = set()

            for key in rs:
                f_.add(key[0])
                t_.add(key[1])
                d_.add(key[2])

            return f_, t_, d_

        @staticmethod
        def author_dicts():
            names = dict()
            auids = dict()
            rs = all_authors()

            for a in rs:
                # a[0]... id
                # a[1]... auid
                # a[2]... given_name
                # a[3]... surname
                if a[2] is not None:
                    # There are cases where no given_name is available
                    name = name_from(a[2], a[3])
                else:
                    name = a[3]
                id_ = a[0]
                names[name] = id_
                auid = a[1]
                if auid is not None and auid is not '':
                    auids[auid] = id_

            return names, auids

        @staticmethod
        def media_dict():
            rs = all_media()
            media = dict()

            for m in rs:
                media[m[0]] = m[1]

            return media

        def __init__(self):
            self._names, self._auids = DedupSingleton.Dedup.author_dicts()
            self._media = DedupSingleton.Dedup.media_dict()
            self._facts, self._titles, self._doi = DedupSingleton.Dedup.fact_sets()

        def add_author(self, author: DAuthor):
            if author.given_name is not None:
                # There are cases where no given_name is available
                name = name_from(author.given_name, author.surname)
            else:
                name = author.surname
            id_ = author.id
            self._names[name] = id_
            auid = author.auid
            if auid is not None and auid is not '':
                self._auids[auid] = author.id

        def add_medium(self, med: DMedium):
            self._media[med.name] = med.id

        def add_fact(self, fact: FPublication):
            self._facts.add(get_fact_key(fact.lang_id, fact.date_id, fact.author_id, fact.medium_id))
            self._titles.add(fact.title_primary)

            if fact.doi is not '':
                self._doi.add(fact.doi)

        def name(self, name):
            # If name exists, return author_id, else False
            if name in self._names:
                return self._names[name]
            return False

        def names(self, given_name, surname):
            name = name_from(given_name, surname)
            return self.name(name)

        def auid(self, auid):
            # if auid exists, return author_id, else False
            if auid in self._auids:
                return self._auids[auid]
            return False

        def medium(self, medium_name):
            # if medium_name exists, return medium_id, else False
            if medium_name in self._media:
                return self._media[medium_name]

            return False

        def fact_keys(self, lang, date_id, author_id, medium_id):
            return self.fact_key(get_fact_key(lang, date_id, author_id, medium_id))

        def fact_key(self, key):
            return key in self._facts

        def title(self, title):
            return title in self._titles

        def doi(self, doi):
            # there are sources which do not provide a doi
            if doi is '':
                return False
            return doi in self._doi

    instance = None

    def __init__(self):
        if not DedupSingleton.instance:
            DedupSingleton.instance = DedupSingleton.Dedup()

    def __getattr__(self, name):
        return getattr(self.instance, name)
