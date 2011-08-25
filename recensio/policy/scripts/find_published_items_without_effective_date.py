from DateTime import DateTime


portal = app.recensio
broken = portal.portal_catalog.search({
        "review_state":"published",
        'effective': {
            "query":DateTime('1000/01/02 1:00:00 GMT+0'),
            "range":"max"
            }})

broken_csv = open("broken.csv", "w")

broken_csv.write("'url', 'effective', 'effective_date'\n")

for i in broken:
    broken_csv.write(
        "'%s', '%s', '%s'\n" %(
            i.getObject().absolute_url(), i.effective(), i.effective_date
            ))
