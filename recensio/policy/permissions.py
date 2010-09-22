from Products.CMFCore import permissions as CMFCorePermissions
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

security = ModuleSecurityInfo('recensio.policy')

security.declarePublic('Permanently delete objects')
MyPermission = 'recensio.policy: Permanently delete objects'
setDefaultRoles(MyPermission, ())
