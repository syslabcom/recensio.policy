from ftw.upgrade import UpgradeStep
from plone import api
from plone.memoize.instance import memoize
from Products.Archetypes.exceptions import ReferenceException
from recensio.contenttypes.interfaces import IReview
from recensio.contenttypes.setuphandlers import initGndContainer
from zope.annotation.interfaces import IAnnotations
import logging
import transaction

logger = logging.getLogger(__name__)


class MigrateToNewPersonContentType(UpgradeStep):
    """Migrate to new Person content type."""

    @property
    @memoize
    def gnd_view(self):
        return api.content.get_view(
            name="gnd",
            context=self.portal,
            request=self.portal.REQUEST,
        )

    def __call__(self):
        self.install_upgrade_profile()

        initGndContainer()

        catalog = api.portal.get_tool("portal_catalog")
        b_start = 0
        b_size = 1000
        while True:
            brains = catalog(
                object_provides=IReview.__identifier__, b_start=b_start, b_size=b_size
            )
            for brain in brains[b_start : b_start + b_size]:
                if not brain:
                    logger.info("Skipping empty brain")
                    continue
                try:
                    obj = brain.getObject()
                except Exception as e:
                    logger.exception(e)
                    continue
                self._migrate_one(obj)
            transaction.commit()
            b_start = b_start + b_size
            if b_start >= len(brains):
                break

    def _migrate_one(self, obj):
        changed = False
        annotations = IAnnotations(obj)
        prefix = "Archetypes.storage.AnnotationStorage"
        for fieldname in ["authors", "editorial", "reviewAuthors", "curators"]:
            field = obj.getField(fieldname)
            if not field:
                continue
            accessor = field.getAccessor(obj)
            new_value = accessor() or []

            old_value = annotations.get("-".join([prefix, fieldname]))
            if not old_value:
                continue
            for person in old_value:
                lastname = person["lastname"]
                firstname = person["firstname"]
                if not (firstname or lastname):
                    continue

                results = self.gnd_view.find(
                    firstname=firstname,
                    lastname=lastname,
                    solr=False,  # solr is only committed on transaction commit
                )
                if results:
                    if len(results) > 1:
                        logger.info(
                            'Ambiguous name "{}, {}", picking {}'.format(
                                lastname,
                                firstname,
                                results[0].getPath(),
                            )
                        )
                    new_value.append(results[0].getObject())
                else:
                    new_value.append(
                        self.gnd_view.createPerson(
                            firstname=firstname,
                            lastname=lastname,
                        )
                    )
            if new_value and new_value != accessor():
                mutator = obj.getField(fieldname).getMutator(obj)
                try:
                    mutator(new_value)
                except Exception:
                    logger.warning("Could not set {} reference on {} to {}".format(
                        fieldname, "/".join(obj.getPhysicalPath()), new_value
                    ))
                    continue
                changed = True

            del annotations["-".join([prefix, fieldname])]
        if changed:
            logger.info("Migrated {}".format("/".join(obj.getPhysicalPath())))
