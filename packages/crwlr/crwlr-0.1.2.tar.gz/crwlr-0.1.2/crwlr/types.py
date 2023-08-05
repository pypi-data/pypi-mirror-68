#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
from collections import namedtuple
from configparser import ConfigParser
from datetime import datetime

from crwlr.errors import ConfigAttributeMissingError, ConfigSectionMissingError
from crwlr.helper import check_re_match
from crwlr.statics import CONFIG_SECTION_DB, CONFIG_ATTR_DB_USERNAME, CONFIG_ATTR_DB_PASSWORD, CONFIG_ATTR_DB_HOST, \
    CONFIG_ATTR_DB_PORT, CONFIG_ATTR_DB_DBNAME, DEFAULT_DB_PORT, DEFAULT_DB_HOST, DEFAULT_DB_DBNAME, \
    DEFAULT_DB_USERNAME, CONFIG_ATTR_CONN_STR, DB_CONNECTION_STRING_FMT, CONF_ERR, \
    CONF_ERR_DB_PW_NOT_FOUND_FMT, CONF_ERR_API_SECT_NOT_FOUND, CONFIG_ATTR_CR_ADMIN_MAIL, CONFIG_SECTION_API, \
    CONF_ERR_CR_NO_ADMIN_MAIL, CROSSREF_USERAGENT_FMT, CR_KEY_MAILTO, CR_KEY_AGENT, CONF_ERR_DB_SECT_NOT_FOUND, \
    LOG_DB_CONNECTION_FROM_CONF_FMT, STAR, CONFIG_CRWLR, LOG_DB_CONNECTION_STRING_FMT, CROSSREF_DICTKEY_AUTHOR, \
    CROSSREF_DICTKEY_FIRST, CROSSREF_DICTKEY_SEQUENCE, CROSSREF_DICTKEY_GIVEN, CROSSREF_DICTKEY_FAMILY, \
    CROSSREF_DICTKEY_MEDIUMNAME, CROSSREF_BOOK_REGEX, CROSSREF_PROCEEDING_REGEX, CROSSREF_JOURNAL_REGEX, \
    CROSSREF_DICTKEY_TYPE, DB_DATE_ID_FMT, CROSSREF_DICTKEY_CREATED, CROSSREF_DICTKEY_DATEPARTS, CROSSREF_DATE_FMT, \
    DASH, CROSSREF_DICTKEY_LANG, CROSSREF_LANGUAGE_MAPPINGS, CROSSREF_DICTKEY_REFS, CROSSREF_DICTKEY_URL, \
    CROSSREF_DICTKEY_TITLE, CROSSREF_DICTKEY_SOURCEDB, CONFIG_ATTR_SPRINGERNAT_API_KEY, CONF_ERROR_ATTR_MISSING_FMT, \
    CROSSREF_DEFAULT_LANGUAGE


class PublicationRetrieval:
    def __init__(self, doi, abstract):
        self.doi = doi
        self.abstract = abstract


class CrossRefRetrieval:

    @staticmethod
    def from_publication(pub: PublicationRetrieval, crossref_d):
        return CrossRefRetrieval(pub.doi, pub.abstract, crossref_d)

    def __init__(self, doi, abstract, crossref_d):
        self.doi = doi
        self._abstract = abstract
        self.crossref_d = crossref_d

    @property
    def first_author(self):
        list_authors = self.crossref_d[CROSSREF_DICTKEY_AUTHOR]
        for author_dict in list_authors:
            if author_dict[CROSSREF_DICTKEY_SEQUENCE] == CROSSREF_DICTKEY_FIRST:
                given_name = author_dict[CROSSREF_DICTKEY_GIVEN]
                surname = author_dict[CROSSREF_DICTKEY_FAMILY]
                return given_name, surname

        return False, False

    @property
    def medium_title(self):
        # Crossref splits media titles based on length
        med_title = ''.join(self.crossref_d[CROSSREF_DICTKEY_MEDIUMNAME])
        if med_title == '' or med_title is None:
            return False
        return med_title

    @property
    def medium_type(self):
        type_ = self.crossref_d[CROSSREF_DICTKEY_TYPE].lower()
        MediumType = namedtuple('MediumType', 'short_type long_type')

        types = {CROSSREF_JOURNAL_REGEX: MediumType('j', 'journal'),
                 CROSSREF_PROCEEDING_REGEX: MediumType('p', 'conference proceeding'),
                 CROSSREF_BOOK_REGEX: MediumType('b', 'book')
                 }

        for t in types.keys():
            if check_re_match(t, type_):
                type_short = types[t].short_type
                type_long = types[t].long_type
                return type_short, type_long

        return False, False

    @property
    def date_id(self):
        date_str = DASH.join(str(e) for e in self.crossref_d[CROSSREF_DICTKEY_CREATED][CROSSREF_DICTKEY_DATEPARTS][0])
        try:
            date_ = datetime.strptime(date_str, CROSSREF_DATE_FMT).date()
            date_id = DB_DATE_ID_FMT.format(date_.month, date_.year)
        except ValueError as e:
            return False

        if isinstance(date_id, str):
            return date_id

        return False

    @property
    def lang_id(self):
        # there are publications without language attribute => default: english
        if CROSSREF_DICTKEY_LANG not in self.crossref_d:
            return CROSSREF_LANGUAGE_MAPPINGS[CROSSREF_DEFAULT_LANGUAGE]

        lang_id = self.crossref_d[CROSSREF_DICTKEY_LANG]
        if lang_id is None or lang_id not in CROSSREF_LANGUAGE_MAPPINGS:
            return False

        return CROSSREF_LANGUAGE_MAPPINGS[lang_id]

    @property
    def references(self):
        if CROSSREF_DICTKEY_REFS not in self.crossref_d:
            return False

        return self.crossref_d[CROSSREF_DICTKEY_REFS]

    @property
    def url(self):
        return self.crossref_d[CROSSREF_DICTKEY_URL] if CROSSREF_DICTKEY_URL in self.crossref_d else ''

    @property
    def abstract(self):
        if isinstance(self._abstract, str) and self._abstract is not '':
            return self._abstract.lower()

        return False

    @property
    def primary_title(self):
        if CROSSREF_DICTKEY_TITLE in self.crossref_d:
            primary_title = ''.join(self.crossref_d[CROSSREF_DICTKEY_TITLE])
            if primary_title is not '':
                # title is available
                return primary_title.lower()

        return False

    @property
    def db(self):
        if CROSSREF_DICTKEY_SOURCEDB in self.crossref_d:
            name_of_database = self.crossref_d[CROSSREF_DICTKEY_SOURCEDB]
            return name_of_database.lower()
        return False


class CrwlrConfig:

    def __init__(self, path):
        self.config = ConfigParser()
        self.config.read(path)

    def cr_export(self, admin_mail=None):
        mail_adr = self.cr_admin_mail
        if admin_mail is not None:
            mail_adr = admin_mail
        # Export environment variables for CrossRef Client API
        os.environ[CR_KEY_AGENT] = str(CROSSREF_USERAGENT_FMT.format(mail_adr))
        os.environ[CR_KEY_MAILTO] = str(mail_adr)
        Log.debug(None, CONFIG_CRWLR, 'Export environment variables:')
        Log.debug(None, CONFIG_CRWLR, os.environ.get(CR_KEY_AGENT))
        Log.debug(None, CONFIG_CRWLR, os.environ.get(CR_KEY_MAILTO))

    @property
    def cr_admin_mail(self):
        if CONFIG_SECTION_API in self.config:
            if CONFIG_ATTR_CR_ADMIN_MAIL in self.config[CONFIG_SECTION_API]:
                return self.config.get(CONFIG_SECTION_API, CONFIG_ATTR_CR_ADMIN_MAIL)
            else:
                msg = CONF_ERROR_ATTR_MISSING_FMT.format(CONF_ERR_CR_NO_ADMIN_MAIL)
                raise ConfigAttributeMissingError(CONF_ERR.format(msg))
        raise ConfigSectionMissingError(CONF_ERR.format(CONF_ERR_API_SECT_NOT_FOUND))

    @property
    def api_key(self):
        if CONFIG_SECTION_API in self.config:
            if CONFIG_ATTR_SPRINGERNAT_API_KEY in self.config[CONFIG_SECTION_API]:
                return self.config.get(CONFIG_SECTION_API, CONFIG_ATTR_SPRINGERNAT_API_KEY)
            else:
                msg = CONF_ERROR_ATTR_MISSING_FMT.format(CONFIG_ATTR_SPRINGERNAT_API_KEY)
                raise ConfigAttributeMissingError(CONF_ERR.format(msg))
        raise ConfigSectionMissingError(CONF_ERR.format(CONF_ERR_API_SECT_NOT_FOUND))

    @property
    def db_password(self):
        if CONFIG_ATTR_DB_PASSWORD in self.config[CONFIG_SECTION_DB]:
            return self.config.get(CONFIG_SECTION_DB, CONFIG_ATTR_DB_PASSWORD)
        else:
            err_msg = CONF_ERR_DB_PW_NOT_FOUND_FMT.format(CONFIG_ATTR_DB_PASSWORD)
            raise ConfigAttributeMissingError(CONF_ERR.format(err_msg))

    @property
    def db_username(self):
        return self.config.get(CONFIG_SECTION_DB, CONFIG_ATTR_DB_USERNAME, fallback=DEFAULT_DB_USERNAME)

    @property
    def db_host(self):
        return self.config.get(CONFIG_SECTION_DB, CONFIG_ATTR_DB_HOST, fallback=DEFAULT_DB_HOST)

    @property
    def db_name(self):
        return self.config.get(CONFIG_SECTION_DB, CONFIG_ATTR_DB_DBNAME, fallback=DEFAULT_DB_DBNAME)

    @property
    def db_port(self):
        return self.config.get(CONFIG_SECTION_DB, CONFIG_ATTR_DB_PORT, fallback=DEFAULT_DB_PORT)

    @property
    def connection_string(self):
        if CONFIG_SECTION_DB in self.config:
            if CONFIG_ATTR_CONN_STR in self.config[CONFIG_SECTION_DB]:
                Log.debug(None, CONFIG_CRWLR, LOG_DB_CONNECTION_FROM_CONF_FMT.format(CONFIG_ATTR_CONN_STR))
                return self.config.get(CONFIG_SECTION_DB, CONFIG_ATTR_CONN_STR)
            elif CONFIG_ATTR_DB_PASSWORD in self.config[CONFIG_SECTION_DB]:
                conn_masked = DB_CONNECTION_STRING_FMT.format(self.db_username, STAR * 8, self.db_host, self.db_port,
                                                              self.db_name)
                Log.debug(None, CONFIG_CRWLR, LOG_DB_CONNECTION_STRING_FMT.format(conn_masked))
                return DB_CONNECTION_STRING_FMT.format(self.db_username, self.db_password, self.db_host, self.db_port,
                                                       self.db_name)
            else:
                err_msg = CONF_ERR_DB_PW_NOT_FOUND_FMT.format(CONFIG_ATTR_DB_PASSWORD)
                raise ConfigAttributeMissingError(CONF_ERR.format(err_msg))
        raise ConfigSectionMissingError(CONF_ERR.format(CONF_ERR_DB_SECT_NOT_FOUND))


class Log(object):
    @staticmethod
    def _logger(name=None, obj=None):
        if name:
            return logging.getLogger(name)
        elif obj:
            return logging.getLogger(obj.__class__.__name__)

    @staticmethod
    def debug(obj, name=None, *args):
        Log._logger(obj=obj, name=name)
        if len(args) > 1:
            logging.debug(args[0], args[1:])
        else:
            logging.debug(args[0])

    @staticmethod
    def warning(obj, name=None, *args):
        logger = Log._logger(obj=obj, name=name)
        if len(args) > 1:
            logger.warning(args[0], args[1:])
        else:
            logger.warning(args[0])

    @staticmethod
    def info(obj, name=None, *args):
        logger = Log._logger(obj=obj, name=name)
        if len(args) > 1:
            logger.info(args[0], args[1:])
        else:
            logger.info(args[0])

    @staticmethod
    def error(obj, name=None, *args):
        logger = Log._logger(obj=obj, name=name)
        if len(args) > 1:
            logger.error(args[0], args[1:])
        else:
            logger.error(args[0])

    @staticmethod
    def exception(obj, name=None, *args):
        logger = Log._logger(obj=obj, name=name)
        if len(args) > 1:
            logger.exception(args[0], args[1:])
        else:
            logger.exception(args[0])
