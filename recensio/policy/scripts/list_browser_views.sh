#!/bin/sh

# Print out the

ZCML=$(find -L $VIRTUAL_ENV/parts/omelette/recensio -name "*.zcml")

for zcml in $ZCML
do
   # echo $zcml
    VIEWS=$VIEWS" "$(xmlstarlet sel -N browser=http://namespaces.zope.org/browser -t -m "//browser:page" -v "@for" -o ":" -v "@name" -o " " $zcml)
done

SORTED_VIEWS=$(echo $VIEWS | sed 's/ /\n/g' | sed 's/\*/all/g' | sort -u)
for VIEW in $SORTED_VIEWS
do
    echo $VIEW
done
