## Script (Python) "handle_change"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=info
##title=
##
rwh = context.restrictedTraverse("@@recensio_workflow_helper")
rwh.handleTransition(info)
