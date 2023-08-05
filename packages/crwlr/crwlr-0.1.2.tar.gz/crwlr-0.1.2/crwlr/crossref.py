#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import uuid4

from pybliometrics.scopus.author_search import AuthorSearch

from crwlr.database import DReference, DedupSingleton, malf_scopus_crit, malf_crossref_crit, DMedium, DAuthor, \
    FPublication, MalformedPublication, malf_crossref_warn, bulk_load
from crwlr.helper import reference_title, check_re_match
from crwlr.statics import CROSSREF_DICTKEY_YEAR, CROSSREF_DICTKEY_AUTHOR, CROSSREF_YEAR_REGEX, CROSSREF_DICTKEY_DOI, \
    CROSSREF_DICTKEY_KEY, CROSSREF_DICTKEY_UNSTRUCTURED, NO_PUBLICATION_NAME, NO_INSERT, NO_SRCTYPE, NO_LANGUAGE, \
    NO_DATE, UNKNOWN_AUTHOR, QUERY_SCOPUS_AUTHOR_FMT, NO_ABSTRACT, NO_TITLE, DATA_SOURCE_CROSSREF, DUPLICATE_DOI, \
    DUPLICATE_PUBLICATION, DUPLICATE_TITLE, CROSSREF_TL, NO_REFERENCES, IGNORED, QUERY_CROSSREF, \
    CROSSREF_DEBUG_DOI_NOT_FOUND_FMT
from crwlr.types import CrossRefRetrieval, Log


def query_crossref(pub_l: list):
    from crossref_commons import retrieval as crossref_retrieval
    retrieval_l = []
    for pub in pub_l:
        try:
            d_ = crossref_retrieval.get_publication_as_json(pub.doi)
            retrieval_l.append(CrossRefRetrieval(pub.doi, pub.abstract, d_))
        except ValueError:
            # It seems that not all publications are available in CrossRef
            Log.debug(None, QUERY_CROSSREF, CROSSREF_DEBUG_DOI_NOT_FOUND_FMT.format(pub.doi))

    return retrieval_l


def transform_references(retrieval: CrossRefRetrieval):
    ref_l = []
    pub_id = str(uuid4())

    if isinstance(retrieval.references, bool):
        return False, False

    for reference in retrieval.references:
        if CROSSREF_DICTKEY_YEAR not in reference or CROSSREF_DICTKEY_AUTHOR not in reference:
            # too many references are unstructured data which does not payoff
            # to interpret
            continue

        title = reference_title(reference)

        if title is False:
            # a reference needs a title
            continue

        id_ = str(uuid4())
        year = check_re_match(CROSSREF_YEAR_REGEX, reference[CROSSREF_DICTKEY_YEAR])
        author = reference[CROSSREF_DICTKEY_AUTHOR]
        ref_id = reference[CROSSREF_DICTKEY_DOI] if CROSSREF_DICTKEY_DOI in reference else reference[
            CROSSREF_DICTKEY_KEY]
        fulltext = reference[CROSSREF_DICTKEY_UNSTRUCTURED] if CROSSREF_DICTKEY_UNSTRUCTURED in reference else ''

        r_ = DReference(id=id_, pub_id=pub_id, ref_id=ref_id, title=title, year=year,
                        authors=author, fulltext=fulltext)

        ref_l.append(r_)

    return pub_id, ref_l


def transform_medium(retrieval: CrossRefRetrieval):
    dedup = DedupSingleton()
    med_title = retrieval.medium_title

    if isinstance(med_title, bool):
        # No medium type at all
        malf_scopus_crit(doi=retrieval.doi, reason=NO_PUBLICATION_NAME, action=NO_INSERT)

    # deduplication check
    medium_id = dedup.medium(med_title)
    if isinstance(medium_id, str):
        # medium found
        return medium_id

    type_short, type_long = retrieval.medium_type
    if isinstance(type_short, bool):
        # Unexpected medium type
        return malf_crossref_crit(doi=retrieval.doi, reason=NO_SRCTYPE, action=NO_INSERT)

    id_ = str(uuid4())

    medium = DMedium(id=id_, type_short=type_short, type_long=type_long, name=med_title.lower())
    dedup.add_medium(medium)
    return medium


def transform_language(retrieval: CrossRefRetrieval):
    lang_id = retrieval.lang_id
    if isinstance(lang_id, bool):
        malf_crossref_crit(doi=retrieval.doi, reason=NO_LANGUAGE, action=NO_INSERT)
    return lang_id


def transform_date(retrieval: CrossRefRetrieval):
    date_id = retrieval.date_id
    if isinstance(date_id, bool):
        return malf_crossref_crit(doi=retrieval.doi, reason=NO_DATE, action=NO_INSERT)
    return date_id


def transform_author(retrieval: CrossRefRetrieval):
    dedup = DedupSingleton()

    given_name, surname = retrieval.first_author

    if isinstance(given_name, bool):
        return malf_crossref_crit(doi=retrieval.doi, reason=UNKNOWN_AUTHOR, action=NO_INSERT)
    # Duplication check
    author_id = dedup.names(given_name, surname)
    if isinstance(author_id, str):
        # author found, exists = id
        return author_id

    # new author -> Search scopus
    q = QUERY_SCOPUS_AUTHOR_FMT.format(given_name, surname)
    authors = AuthorSearch(q).authors
    if authors:
        # scopus found an author, take the first one (we cant tell which is the right one)
        a = authors[0]
        id_ = str(uuid4())
        author = DAuthor(id=id_, given_name=a.givenname, surname=a.surname, indexed_name='', auid='',
                         afid=a.affiliation_id, affiliation_name=a.affiliation, city=a.city, country=a.country)
        dedup.add_author(author)
        return author

    # No author found
    return malf_crossref_crit(doi=retrieval.doi, reason=UNKNOWN_AUTHOR, action=NO_INSERT)


def transform_publication(retrieval: CrossRefRetrieval, author_id, medium_id, date_id, lang, reference_id):
    dedup = DedupSingleton()

    url = retrieval.url

    abstract = retrieval.abstract
    if isinstance(abstract, bool):
        # no abstract
        return malf_crossref_crit(doi=retrieval.doi, reason=NO_ABSTRACT, action=NO_INSERT)

    primary_title = retrieval.primary_title
    if isinstance(primary_title, bool):
        return malf_crossref_crit(doi=retrieval.doi, reason=NO_TITLE, action=NO_INSERT)

    name_of_database = retrieval.db
    if isinstance(name_of_database, bool):
        name_of_database = DATA_SOURCE_CROSSREF

    # Duplication checks
    # check if keys already exist in db => Duplicate
    doi_exists = dedup.doi(retrieval.doi)
    if doi_exists:
        return malf_crossref_crit(doi=retrieval.doi, reason=DUPLICATE_DOI, action=NO_INSERT)

    keys_exist = dedup.fact_keys(lang, str(date_id), author_id, medium_id)
    if keys_exist:
        return malf_crossref_crit(doi=retrieval.doi, reason=DUPLICATE_PUBLICATION, action=NO_INSERT)

    title_exists = dedup.title(primary_title)

    if title_exists:
        return malf_crossref_crit(doi=retrieval.doi, reason=DUPLICATE_TITLE, action=NO_INSERT)

    f = FPublication(doi=retrieval.doi, title_primary=primary_title, abstract=abstract, db=name_of_database,
                     url=url, lang_id=lang, author_id=author_id, medium_id=medium_id, reference_id=reference_id,
                     date_id=date_id)

    dedup.add_fact(f)
    return f


def crossref_tl(retrieval_l: list):
    auth_l = []
    med_l = []
    malf_l = []
    fact_l = []
    refs_l = []

    Log.info(None, CROSSREF_TL, '220; Transform')

    for retrieval in retrieval_l:
        doi = retrieval.doi

        author = transform_author(retrieval)
        if isinstance(author, DAuthor):
            # new Author
            auth_l.append(author)
            author_id = author.id
        elif isinstance(author, str):
            # Author exists
            author_id = author
        elif isinstance(author, MalformedPublication):
            # no author found
            malf_l.append(author)
            Log.debug(None, CROSSREF_TL, 'malf author => skip ({0})'.format(doi))
            continue
        else:
            raise ValueError('author is not DAuthor, str or MalformedPublication, but: {0}'.format(type(author)))

        medium = transform_medium(retrieval)

        if isinstance(medium, DMedium):
            # new Medium
            med_l.append(medium)
            medium_id = medium.id
        elif isinstance(medium, str):
            # Medium exists
            medium_id = medium
        elif isinstance(medium, MalformedPublication):
            malf_l.append(medium)
            Log.debug(None, CROSSREF_TL, 'malf medium => skip ({0})'.format(doi))
            continue
        else:
            raise ValueError('medium is not DMedium, str or MalformedPublication, but: {0}'.format(type(author)))

        date_id = transform_date(retrieval)

        if isinstance(date_id, MalformedPublication):
            malf_l.append(date_id)
            Log.debug(None, CROSSREF_TL, 'malformed date => skip ({0})'.format(doi))
            continue

        lang = transform_language(retrieval)

        if isinstance(lang, MalformedPublication):
            malf_l.append(lang)
            Log.debug(None, CROSSREF_TL, 'malformed language => skip ({0})'.format(doi))
            continue

        reference_id, references = transform_references(retrieval)
        if isinstance(references, list):
            refs_l.extend(references)
        else:
            reference_id = ''
            malf_l.append(malf_crossref_warn(doi=doi, reason=NO_REFERENCES, action=IGNORED))

        fact = transform_publication(retrieval, author_id, medium_id, date_id, lang, reference_id)

        if isinstance(fact, MalformedPublication):
            malf_l.append(fact)
            continue

        fact_l.append(fact)

    Log.info(None, CROSSREF_TL, '230; Load')

    bulk_load(auth_l)
    bulk_load(med_l)
    bulk_load(malf_l)
    bulk_load(refs_l)
    bulk_load(fact_l)

    Log.info(None, CROSSREF_TL, '231; malformed_publications, #: {}'.format(len(malf_l)))
    Log.info(None, CROSSREF_TL, '232; authors, #: {}'.format(len(auth_l)))
    Log.info(None, CROSSREF_TL, '233; mediums, #: {}'.format(len(med_l)))
    Log.info(None, CROSSREF_TL, '234; references, #: {}'.format(len(refs_l)))
    Log.info(None, CROSSREF_TL, '235; facts, #: {}'.format(len(fact_l)))
