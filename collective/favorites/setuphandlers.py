# coding=utf-8
from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

from Products.statusmessages.interfaces import IStatusMessage

from logging import getLogger
logger = getLogger('collective')

from collective.favorites import MessageFactory as _



def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.favoritesi_various.txt') is None:
        return

    # Add additional setup code here
    portal = context.getSite()

    tool = getToolByName(portal, 'portal_membership')
    
    # Member Folder necessary for internal Favorites
    #if not tool.getMemberareaCreationFlag():
    tool.setMemberareaCreationFlag(True)
        
    folder = tool.getMembersFolder()
    
    if folder == None:
        folder_id = portal.invokeFactory(type_name="Folder", id=tool.membersfolder_id)
        portal[folder_id].setTitle(tool.membersfolder_id)
        portal[folder_id].setLanguage("")
    
