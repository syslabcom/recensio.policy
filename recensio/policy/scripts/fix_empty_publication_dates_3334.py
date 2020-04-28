from DateTime import DateTime
import transaction

portal = app.recensio
broken = portal.portal_catalog.search(
    {
        "review_state": "published",
        "effective": {"query": DateTime("1000/01/02 1:00:00 GMT+0"), "range": "max"},
    }
)

for i, brain in enumerate(broken):
    obj = brain.getObject()
    effective_date = None
    for history in obj.workflow_history["simple_publication_workflow"]:
        if history["action"] == "publish":
            publication_date = history["time"]
            if publication_date > effective_date:
                effective_date = publication_date
    if str(obj.effective()) == "1000/01/01":
        # Just to be extra sure we don't clobber existing dates
        obj.setEffectiveDate(effective_date)
        obj.reindexObject()
        print("Fixed effective_date for %s" % obj.absolute_url())

    if i % 20:
        transaction.commit()

transaction.commit()
