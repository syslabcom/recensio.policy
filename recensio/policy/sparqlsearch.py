#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
from rdflib.graph import Graph
from rdflib.plugins.parsers.rdfa import RDFaError
from rdflib.term import URIRef
import re

import sparql
from sparql import IRI

from logging import getLogger

log = getLogger(__name__)

QUERY = \
    '''PREFIX  rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX  owl:<http://www.w3.org/2002/07/owl#>
PREFIX  dc:<http://purl.org/dc/elements/1.1/>
PREFIX  dcterms:<http://purl.org/dc/terms/>
PREFIX  dcmitype:<http://purl.org/dc/dcmitype/>
PREFIX  bibo:<http://purl.org/ontology/bibo/>
PREFIX  frbr:<http://purl.org/vocab/frbr/core#>
PREFIX  event:<http://purl.org/NET/c4dm/event.owl#>
PREFIX  foaf:<http://xmlns.com/foaf/0.1/>
PREFIX  skos:<http://w3.org/2004/02/skos/core#>
PREFIX  geonames:<http://www.geonames.org/ontology#>
PREFIX  marcrel:<http://id.loc.gov/vocabulary/relators/>

PREFIX  bibo:<http://purl.org/ontology/bibo/>

SELECT * WHERE {
    ?docid bibo:isbn "%s".
        ?docid ?p ?o
        }LIMIT 200'''


def getLabels(subject_url, graph):
    retval = {}
    for (predicate, obj) in graph.preferredLabel(URIRef(subject_url)):
        retval[obj.language] = obj.title()
    return retval


def genericStore(target_attribute):

    def storeLiteralImpl(obj, retval):
        if not obj.value.startswith('http'):
            retval[target_attribute] = obj.value
        else:
            g = Graph()
            g.parse(obj.value)
            possible_values = getLabels(obj.value, g)
            if 'en' in possible_values:
                retval[target_attribute] = possible_values['en']
            else:
                log.error('No handler for %s', str(obj))

    return storeLiteralImpl


numberStore_re = re.compile('(\d+) S\.')


def numberStore(obj, retval):
    raw_data = obj.value
    pages = numberStore_re.findall(raw_data)
    if pages:
        retval['pages'] = pages[0]


def keywords_and_ddc(obj, retval):
    if 'dewey' in unicode(obj).lower():
        return
    raw_data = obj.value
    if raw_data.startswith('http'):
        g = Graph()
        g.parse(raw_data, format='application/rdf+xml')
        if [x for x in
            g.predicates(object=URIRef('http://w3.org/2004/02/skos/core#Concept'
            ))]:

            # We don't handle Concepts

            return
        possible_values = [x.title() for x in
                           g.objects(predicate=URIRef('http://d-nb.info/standards/elementset/gnd#preferredNameForTheSubjectHeading'
                           ))] + [x.title() for x in
                                  g.objects(predicate=URIRef('http://d-nb.info/standards/elementset/gnd#preferredNameForThePlaceOrGeographicName'
                                  ))]
        if possible_values:
            retval['keywords'].extend(possible_values)
        else:
            log.error("Don't know how to handle this: %s", raw_data)
    else:
        if obj.datatype == 'http://purl.org/dc/terms/DDC':
            retval['ddc'] = obj.value
        else:
            retval['keywords'].append(obj.value)


def authorsStore(obj, retval):
    if not obj.value.startswith('http'):
        retval['authors'].append(obj.value)
    else:
        g = Graph()
        try:
            g.parse(obj.value)
        except RDFaError, e:
            log.error("Bad answer from '%s': '%s', ignoring",
                      obj.value, e, exc_info=True)
            return
        firstnames = [x.title() for x in
                      g.objects(predicate=URIRef('http://d-nb.info/standards/elementset/gnd#forename'
                      ))]
        surnames = [x.title() for x in
                    g.objects(predicate=URIRef('http://d-nb.info/standards/elementset/gnd#surname'
                    ))]
        firstname = (firstnames[0] if firstnames else None)
        surname = (surnames[0] if surnames else None)
        retval['authors'].append(dict(firstname=firstname,
                                 lastname=surname))

HANDLERS = defaultdict(lambda : lambda a, b: None)
HANDLERS['http://purl.org/dc/elements/1.1/title'] = genericStore('title'
        )
HANDLERS['http://purl.org/dc/terms/extent'] = numberStore
HANDLERS['http://purl.org/dc/terms/issued'] = genericStore('year')
HANDLERS['http://purl.org/dc/elements/1.1/creator'] = authorsStore
HANDLERS['http://purl.org/dc/elements/1.1/contributor'] = authorsStore
HANDLERS['http://purl.org/ontology/bibo/editor'] = authorsStore
HANDLERS['http://purl.org/ontology/bibo/isbn'] = genericStore('isbn')
HANDLERS['http://purl.org/dc/elements/1.1/language'] = \
    genericStore('language')
HANDLERS['http://rdvocab.info/Elements/placeOfPublication'] = \
    genericStore('location')
HANDLERS['http://purl.org/dc/elements/1.1/subject'] = keywords_and_ddc
HANDLERS['http://purl.org/dc/elements/1.1/publisher'] = \
    genericStore('publisher')

KNOWN_IGNORED = map(IRI, [
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
    'http://www.w3.org/2002/07/owl#sameAs',
    'http://purl.org/dc/elements/1.1/description',
    'http://purl.org/ontology/bibo/volume',
    'http://xmlns.com/foaf/0.1/homepage',
    'http://purl.org/vocab/frbr/core#exemplar',
    'http://purl.org/dc/terms/isPartOf',
    ])


def getMetadata(isbn):
    retval = {  # dc:creator, bibo:editor, dc:contributor
        'title': None,
        'subtitle': None,
        'authors': [],
        'language': None,
        'isbn': None,
        'ddc': None,
        'location': None,
        'keywords': [],
        'publisher': None,
        'pages': None,
        'year': None,
        }

    isbn = isbn.replace('-', '').replace(' ', '')
    service = sparql.Service('http://lod.b3kat.de/sparql')
    result = service.query(QUERY % isbn)
    for (subject, predicate, obj) in result:
        if predicate.value not in HANDLERS and predicate \
            not in KNOWN_IGNORED:
            log.error('Don\'t know how to handle %s', str(predicate))
        HANDLERS[predicate.value](obj, retval)
    for (key, values) in retval.items():
        if hasattr(values, 'sort'):
            values.sort()
            uniques = []
            for value in values:
                if value not in uniques:
                    uniques.append(value)
            retval[key] = uniques
    return retval
