# -*- coding: utf-8 -*-
from collections import defaultdict
from logging import getLogger
from plone.memoize import ram
from rdflib.graph import Graph
from rdflib.plugins.parsers.rdfa import RDFaError
from rdflib.term import URIRef
from sparql import IRI
from time import time

import re
import sparql


log = getLogger(__name__)

PREFIX_HEADER = """PREFIX  rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
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
PREFIX  rdagr1:<http://rdvocab.info/Elements/>
"""

QUERY = (
    PREFIX_HEADER
    + """SELECT * WHERE {
    ?docid bibo:isbn "%s".
        ?docid ?p ?o
        } LIMIT 200"""
)

QUERY2 = (
    PREFIX_HEADER
    + """SELECT DISTINCT ?bv_best ?bv_alt WHERE
        {
            ?docid bibo:isbn "%s" .
            ?docid frbr:exemplar ?bv_alt
            OPTIONAL {?docid frbr:exemplar ?bv_best .
                    FILTER regex(?bv_best, "bib/DE-12/")}
        } ORDER BY desc(?bv_best)"""
)


def _iri_cachekey(function, iri, **kw):
    """It's expensive to get remote data and it rarely changes, so we can
    cache this heavily.

    Many queries are repeated e.g. language:
    http://id.loc.gov/vocabulary/iso639-2/ger

    These could be cached for longer
    """
    six_hours = time() // (60 * 60 * 6)
    return (iri, six_hours)


@ram.cache(_iri_cachekey)
def graph_parse(iri, **kw):
    graph = Graph()
    return graph.parse(iri, **kw)


def getLabels(subject_url, graph):
    returnval = {}
    for (predicate, obj) in graph.preferredLabel(URIRef(subject_url)):
        returnval[obj.language] = obj.title()
    return returnval


def genericStore(target_attribute):
    def storeLiteralImpl(obj, returnval):
        if not obj.value.startswith("http"):
            returnval[target_attribute] = obj.value
        else:
            g = graph_parse(obj.value)
            possible_values = getLabels(obj.value, g)
            if "en" in possible_values:
                returnval[target_attribute] = possible_values["en"]
            else:
                log.error("No handler for %s", str(obj))

    return storeLiteralImpl


def list_store(target_attribute):
    def _list_store(obj, returnval):
        if target_attribute in returnval.keys():
            returnval[target_attribute].append(obj.value)
        else:
            returnval[target_attribute] = [obj.value]

    return _list_store


numberStore_re = re.compile("(\d+) S\.")


def numberStore(obj, returnval):
    raw_data = obj.value
    pages = numberStore_re.findall(raw_data)
    if pages:
        returnval["pages"] = pages[0]


def keywords_and_ddc(obj, returnval):
    if "dewey" in unicode(obj).lower():
        return
    raw_data = obj.value
    if raw_data.startswith("http"):
        try:
            g = graph_parse(raw_data, format="application/rdf+xml")
        except Exception as e:
            log.exception(e)
            return
        if [
            x
            for x in g.predicates(
                object=URIRef("http://w3.org/2004/02/skos/core#Concept")
            )
        ]:

            # We don't handle Concepts

            return
        if URIRef("http://www.w3.org/2004/02/skos/core#Concept") in [
            x
            for x in g.objects(
                predicate=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
            )
        ]:
            # We still don't handle Concepts
            return

        if URIRef("http://d-nb.info/vocab/gnd-sc#16.5p") in [
            x
            for x in g.objects(
                predicate=URIRef(
                    "http://d-nb.info/standards/elementset/gnd#gndSubjectCategory"
                )
            )
        ]:

            # We don't handle persons as keywords

            return
        if URIRef("http://d-nb.info/vocab/gnd-sc#16.5") in [
            x
            for x in g.objects(
                predicate=URIRef(
                    "http://d-nb.info/standards/elementset/gnd#gndSubjectCategory"
                )
            )
        ]:

            # OK, I really don't know whats happening right now. THis
            # example is from: http://d-nb.info/gnd/4240685-7

            return
        if URIRef("http://d-nb.info/vocab/gnd-sc#6.6") in [
            x
            for x in g.objects(
                predicate=URIRef(
                    "http://d-nb.info/standards/elementset/gnd#gndSubjectCategory"
                )
            )
        ]:

            # We don't handle organizations as keywords

            return
        if URIRef("http://d-nb.info/vocab/gnd-sc#8.2b") in [
            x
            for x in g.objects(
                predicate=URIRef(
                    "http://d-nb.info/standards/elementset/gnd#gndSubjectCategory"
                )
            )
        ]:

            # We don't handle organizations as keywords (again?)

            return

        possible_values = [
            x.title()
            for x in g.objects(
                predicate=URIRef(
                    "http://d-nb.info/standards/elementset/gnd#preferredNameForTheSubjectHeading"
                )
            )
        ] + [
            x.title()
            for x in g.objects(
                predicate=URIRef(
                    "http://d-nb.info/standards/elementset/gnd#preferredNameForThePlaceOrGeographicName"
                )
            )
        ]
        if possible_values:
            returnval["keywords"].extend(possible_values)
        else:
            log.error("Don't know how to handle this for keyword and ddc: %s", raw_data)
    else:
        if obj.datatype == "http://purl.org/dc/terms/DDC":
            returnval["ddcSubject"].append(obj.value)
        else:
            returnval["keywords"].append(obj.value)


def authorsStore(obj, returnval):
    if not obj.value.startswith("http"):
        returnval["authors"].append(obj.value)
    else:
        try:
            g = graph_parse(obj.value)
        except RDFaError as e:
            log.error(
                "Bad answer from '%s': '%s', ignoring", obj.value, e, exc_info=True
            )
            return
        fullnames = list(
            g.query(
                "PREFIX gnd:<http://d-nb.info/standards/elementset/gnd#>  SELECT ?forename ?surname where {[] gnd:preferredNameEntityForThePerson ?entity . ?entity gnd:forename ?forename ; gnd:surname ?surname}"
            )
        )
        if not fullnames:
            fullnames = list(
                g.query(
                    "PREFIX gnd:<http://d-nb.info/standards/elementset/gnd#>  SELECT ?forename ?surname where {[] gnd:forename ?forename ; gnd:surname ?surname}"
                )
            )

        for (firstname, surname) in fullnames:
            returnval["authors"].append(
                dict(firstname=firstname.title(), lastname=surname.title())
            )


def mergeStore(target_attribute):
    def storeMergeImpl(obj, returnval):
        if not obj.value.startswith("http"):
            value = obj.value
        else:
            g = graph_parse(obj.value)
            possible_values = getLabels(obj.value, g)
            if "en" in possible_values:
                value = possible_values["en"]
            else:
                log.error("No handler for %s", str(obj))
        if returnval[target_attribute]:
            if not value in returnval[target_attribute]:
                returnval[target_attribute] = ", ".join(
                    (returnval[target_attribute], value)
                )
        else:
            returnval[target_attribute] = value

    return storeMergeImpl


def seriesVolumeStore(obj, returnval):
    values = [v.strip() for v in obj.value.rsplit(":", 1)]
    returnval["series"] = returnval["series"] or values[0]
    if not values[0] in returnval["series"]:
        returnval["series"] = "; ".join((returnval["series"], values[0]))
    if len(values) > 1:
        returnval["seriesVol"] = returnval["seriesVol"] or values[1]
        if not values[1] in returnval["seriesVol"]:
            returnval["seriesVol"] = "; ".join((returnval["seriesVol"], values[1]))


HANDLERS = defaultdict(lambda: lambda a, b: None)
HANDLERS["http://iflastandards.info/ns/isbd/elements/P1016"] = genericStore("location")
HANDLERS["http://iflastandards.info/ns/isbd/elements/P1006"] = genericStore("subtitle")
HANDLERS["http://purl.org/dc/elements/1.1/contributor"] = authorsStore
HANDLERS["http://purl.org/dc/elements/1.1/creator"] = authorsStore
# XXX In the tests is an example where both are set. Both isbn setters
# override each other right now!
HANDLERS["http://purl.org/dc/elements/1.1/identifier"] = genericStore("isbn")
HANDLERS["http://purl.org/dc/elements/1.1/language"] = genericStore("language")
HANDLERS["http://purl.org/dc/terms/language"] = genericStore("language")
HANDLERS["http://purl.org/dc/elements/1.1/publisher"] = genericStore("publisher")
HANDLERS["http://purl.org/dc/terms/publisher"] = genericStore("publisher")
HANDLERS["http://purl.org/dc/elements/1.1/subject"] = keywords_and_ddc
HANDLERS["http://purl.org/dc/terms/subject"] = keywords_and_ddc
HANDLERS["http://purl.org/dc/elements/1.1/title"] = genericStore("title")
HANDLERS["http://purl.org/dc/terms/title"] = genericStore("title")
HANDLERS["http://purl.org/dc/terms/creator"] = authorsStore
HANDLERS["http://purl.org/dc/terms/extent"] = numberStore
HANDLERS["http://purl.org/dc/terms/issued"] = genericStore("year")
HANDLERS["http://purl.org/ontology/bibo/editor"] = authorsStore
HANDLERS["http://purl.org/ontology/bibo/isbn"] = genericStore("isbn")
HANDLERS["http://rdvocab.info/Elements/placeOfPublication"] = mergeStore("location")
HANDLERS["http://bsb-muenchen.de/ont/b3katOntology#ddcGeo"] = list_store("ddcPlace")
HANDLERS["http://bsb-muenchen.de/ont/b3katOntology#ddcTime"] = list_store("ddcTime")
HANDLERS["http://purl.org/dc/terms/bibliographicCitation"] = seriesVolumeStore


KNOWN_IGNORED = map(
    IRI,
    [  # What is a country code in the context of a publication anyway
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://www.w3.org/2002/07/owl#sameAs",
        "http://purl.org/vocab/frbr/core#exemplar",
        "http://purl.org/dc/elements/1.1/description",
        "http://purl.org/ontology/bibo/volume",
        "http://xmlns.com/foaf/0.1/homepage",
        "http://purl.org/dc/terms/isPartOf",
        "http://purl.org/dc/terms/identifier",
        "http://purl.org/dc/terms/description",
        "http://www.geonames.org/ontology#countryCode",
        "http://purl.org/dc/terms/hasPart",
        "http://purl.org/dc/terms/alternative",
        "http://id.loc.gov/vocabulary/relators/ctb",
        "http://iflastandards.info/ns/isbd/elements/P1053",
        "http://purl.org/ontology/bibo/edition",
        "http://purl.org/ontology/bibo/oclcnum",
        "http://rdvocab.info/Elements/publicationStatement",
        "http://id.loc.gov/vocabulary/relators/aut",
        "http://rdvocab.info/Elements/otherTitleInformation",
    ],
)


def getMetadata(isbn):
    returnval = {  # dc:creator, bibo:editor, dc:contributor
        "title": None,
        "subtitle": None,
        "authors": [],
        "language": None,
        "isbn": None,
        "ddcSubject": [],
        "location": None,
        "keywords": [],
        "publisher": None,
        "pages": None,
        "series": None,
        "seriesVol": None,
        "year": None,
        "bv": None,
    }
    isbn = isbn.replace("-", "").replace(" ", "")
    service = sparql.Service("http://lod.b3kat.de/sparql")

    # Try to get the BV number
    try:
        Q2 = QUERY2 % isbn
        log.debug("Sparql query for BV number:\n%s" % Q2)
        bv = service.query(Q2).fetchone().next()
        bv = bv[0].value if bv[0] else bv[1].value
        bv = bv.split("/")[-1]
        returnval["bv"] = bv
    except StopIteration:
        pass

    log.debug("Sparql query:\n%s" % (QUERY % isbn))
    result = service.query(QUERY % isbn)
    for (subject, predicate, obj) in result:
        if predicate.value not in HANDLERS and predicate not in KNOWN_IGNORED:
            log.error(
                u"Don't know how to handle %s. Contents: %s",
                str(predicate.value),
                obj.value,
            )
        if predicate in KNOWN_IGNORED:
            log.debug(
                u"We ignore the following information: '%s', Content: '%s'",
                str(predicate.value),
                obj.value,
            )
        HANDLERS[predicate.value](obj, returnval)

    for (key, values) in returnval.items():
        if hasattr(values, "sort"):
            values.sort()
            uniques = []
            for value in values:
                if value not in uniques:
                    uniques.append(value)
            returnval[key] = uniques

    return [returnval]
