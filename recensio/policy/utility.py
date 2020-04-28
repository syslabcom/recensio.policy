from lxml import etree
from datetime import datetime

from zope.interface import implements

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry

from recensio.policy.interfaces import IOAIUtility

from copy import deepcopy
from ZTUtils import make_query
from recensio.contenttypes.config import PORTAL_TYPES

from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

browsing_facets = ["ddcPlace", "ddcTime", "ddcSubject"]
filter_facets = ["languageReview"]


class Reader(object):
    def parser(self, ns):
        return lambda name, element: etree.ETXPath("{%s}%s" % (ns, name))(element)

    def parseDate(self, element):
        datetimeFMT = "%Y-%m-%dT%H:%M:%S"
        dateFMT = "%Y-%m-%d"
        try:
            return datetime.strptime(element.text[:19], datetimeFMT)
        except ValueError:
            return datetime.strptime(element.text[:10], dateFMT)

    def __call__(self, element):
        # STEP 1 Unpack OAI Container
        retval = {}
        oai_ns = "http://www.openarchives.org/OAI/2.0/"
        oai_parser = self.parser(oai_ns)
        container = etree.ETXPath("/{%s}OAI-PMH" % oai_ns)(element)[0]
        container_date = oai_parser("responseDate", container)[0]
        container_date = self.parseDate(container_date)
        retval["oai_retrieved"] = container_date
        request = oai_parser("request", container)[0]
        errors = oai_parser("error", container)
        if errors:
            raise Exception(etree.tostring(element))
        record_container = oai_parser("GetRecord", container)[0]
        record = oai_parser("record", record_container)[0]
        record_header = oai_parser("header", record)[0]
        record_identifier = oai_parser("identifier", record_header)[0].text
        retval["oai_identifier"] = record_identifier
        record_datestamp = oai_parser("datestamp", record_header)[0]
        record_datestamp = self.parseDate(record_datestamp)
        retval["oai_timestamp"] = record_datestamp
        record_setspec = oai_parser("setspec", record_header)
        retval["oai_sets"] = [x.text for x in record_setspec]
        record_status = oai_parser("statusType", record_header)
        if record_status:
            assert len(record_status) == 1, (
                "Never tested, since optional" " feature has never been used"
            )

            assert record_status.text == "deleted", (
                "Never tested, since" " optional feature has never been used"
            )
            retval["oai_deleted"] = True
        else:
            retval["oai_deleted"] = False
        record_metadata = oai_parser("metadata", record)
        assert len([x for x in record_metadata]) == 1, "Not implemented"
        retval.update(self.parseDC(record_metadata))
        record_about = oai_parser("about", record)
        assert not record_about, "Not implemented"
        return retval

    def parseDC(self, record_metadata):
        oai_parser = self.parser("http://www.openarchives.org/OAI/2.0/oai_dc/")
        dc_parser = self.parser("http://purl.org/dc/elements/1.1/")
        dcnode = oai_parser("dc", record_metadata[0])[0]
        retval = {}
        retval["dc_title"] = []
        retval["dc_creator"] = []
        retval["dc_subject"] = []
        retval["dc_description"] = []
        retval["dc_publisher"] = []
        retval["dc_contributor"] = []
        retval["dc_date"] = []
        retval["dc_type"] = []
        retval["dc_format"] = []
        retval["dc_identifier"] = []
        retval["dc_source"] = []
        retval["dc_language"] = []
        retval["dc_relation"] = []
        retval["dc_coverage"] = []
        retval["dc_rights"] = []
        for elem in dc_parser("title", dcnode):
            retval["dc_title"].append(elem.text)
        for elem in dc_parser("creator", dcnode):
            retval["dc_creator"].append(elem.text)
        for elem in dc_parser("subject", dcnode):
            retval["dc_subject"].append(elem.text)
        for elem in dc_parser("description", dcnode):
            retval["dc_description"].append(elem.text)
        for elem in dc_parser("publisher", dcnode):
            retval["dc_publisher"].append(elem.text)
        for elem in dc_parser("contributor", dcnode):
            retval["dc_contributor"].append(elem.text)
        for elem in dc_parser("date", dcnode):
            retval["dc_date"].append(self.parseDate(elem))
        for elem in dc_parser("type", dcnode):
            retval["dc_type"].append(elem.text)
        for elem in dc_parser("format", dcnode):
            retval["dc_format"].append(elem.text)
        for elem in dc_parser("identifier", dcnode):
            retval["dc_identifier"].append(elem.text)
        for elem in dc_parser("source", dcnode):
            retval["dc_source"].append(elem.text)
        for elem in dc_parser("language", dcnode):
            retval["dc_language"].append(elem.text)
        for elem in dc_parser("relation", dcnode):
            retval["dc_relation"].append(elem.text)
        for elem in dc_parser("coverage", dcnode):
            retval["dc_coverage"].append(elem.text)
        for elem in dc_parser("rights", dcnode):
            retval["dc_rights"].append(elem.text)
        return retval


registry = MetadataRegistry()
registry.registerReader("oai_dc", Reader())


class OAIProvider(object):
    def __init__(self, url):
        self.client = Client(url, registry)

    def getMetadata(self, id, year):

        import pdb

        pdb.set_trace()


class OAIUtility(object):
    implements(IOAIUtility)
    known_providers = {}
    for url in ["http://www.syslab.com"]:
        known_providers[url] = OAIProvider(url)

    def getOAIProvider(self, url):
        try:
            return self.known_providers[url]
        except KeyError:
            return KeyError(
                "There is no provider for the URL: " '"%s" registered' % url
            )

    def getKnownOAIProviders(self):
        return self.known_providers.keys()


def getSelectedQuery(
    selected, params=None, facet_fields=browsing_facets, queryparam="fq"
):
    """ construct a query that gets faceting info with the specified fields selected,
        i.e. set as fq (filter query) fields. Selected should be a dict with field
        (=attribute) names mapped to lists of values
    """
    if not params:
        params = {"facet": "true", "facet.field": facet_fields}
    for field, values in selected.items():
        for name in values:
            if name:
                if queryparam == "fq":
                    params.setdefault(queryparam, []).append(
                        '%s:"%s"' % (field, name.encode("utf-8"))
                    )
                else:
                    params.setdefault(queryparam, []).append(name.encode("utf-8"))
    return make_query(params, doseq=True)


def convertFacets(
    fields,
    context=None,
    request={},
    filter=None,
    facet_fields=browsing_facets,
    queryparam="fq",
):
    """ convert facet info to a form easy to process in templates """
    info = []
    params = request.copy()  # request needs to be a dict, i.e. request.form
    facets = facet_fields
    params["facet.field"] = facets = list(facets)
    fq = params.get(queryparam, [])
    if isinstance(fq, basestring):
        fq = params[queryparam] = [fq]
    selected = set([facet.split(":", 1)[0].strip("+") for facet in fq])
    selected = selected.intersection(set(browsing_facets))
    for field, values in fields.items():
        counts = []
        second = lambda a, b: cmp(b[1], a[1])
        for name, count in sorted(values.items(), cmp=second):
            p = deepcopy(params)
            # p.setdefault(queryparam, []).append('%s:"%s"' % (field, name.encode('utf-8')))
            if filter is None or filter(name, count):
                counts.append(
                    dict(
                        name=name,
                        count=count,
                        query=getSelectedQuery(
                            {field: [name]},
                            params=p,
                            facet_fields=facet_fields,
                            queryparam=queryparam,
                        ),
                    )
                )
        if counts:
            info.append(dict(title=field, counts=counts))
    if facets:  # sort according to given facets (if available)

        def pos(item):
            try:
                return facets.index(item)
            except ValueError:
                return len(facets)  # position the item at the end

        func = lambda a, b: cmp(pos(a), pos(b))
    else:  # otherwise sort by title
        func = lambda a, b: cmp(a["title"], b["title"])
    return sorted(info, cmp=func)


def getMemberInfo(memberId=None):
    """ As in membership tool, but add academic title."""
    portal = getSite()
    mtool = getToolByName(portal, "portal_membership")
    if not memberId:
        member = mtool.getAuthenticatedMember()
    else:
        member = mtool.getMemberById(memberId)

    if member is None:
        return None

    memberinfo = {
        "fullname": member.getProperty("fullname"),
        "description": member.getProperty("description"),
        "location": member.getProperty("location"),
        "language": member.getProperty("language"),
        "home_page": member.getProperty("home_page"),
        "username": member.getUserName(),
        "has_email": bool(member.getProperty("email")),
        "academic_title": member.getProperty("academic_title"),
        "preferred_language": member.getProperty("preferred_language"),
    }

    return memberinfo
