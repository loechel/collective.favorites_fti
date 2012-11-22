# coding=utf-8

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from plone.uuid.interfaces import IUUID

from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

from Products.statusmessages.interfaces import IStatusMessage

from Products.ATContentTypes.lib import constraintypes
from plone.dexterity.utils import createContentInContainer

from logging import getLogger
logger = getLogger('collective.favorites')

from collective.favorites import MessageFactory as _


def createFavFolder(event):
    request = event.object.REQUEST
    
    home_folder = getToolByName(event.object, 'portal_membership').getHomeFolder()
    
    if home_folder != None:
        if not home_folder.has_key('favorites'):
            #favFolder = home_folder.invokeFactory(type_name="Favorites Folder", id='favorites', language= '')
            typestool = getToolByName(self.context, 'portal_types')
            typestool.constructContent(type_name="Favorites Folder", container=home_folder, id='favorites')
            home_folder['favorites'].setTitle('Favorites')
            home_folder['favorites'].setExcludeFromNav(True)

class FavoriteView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    # BrowserView helper method
    def getUID(self):
        """ AT and Dexterity compatible way to extract UID from a content item """
        # Make sure we don't get UID from parent folder accidentally
        context = self.context.aq_base
        # Returns UID of the context or None if not available
        # Note that UID is always available for all Dexterity 1.1+
        # content and this only can fail if the content is old not migrated
        uuid = IUUID(context, None)
        return uuid

class AddFavoriteView(FavoriteView):
    
    def __call__(self):
        self.messages = IStatusMessage(self.request)
        
        link_id = self.context.id
        link_title = self.context.title
        link_url = self.context.absolute_url()
        link_uid = self.getUID()
        
        typestool = getToolByName(self, 'portal_types')
        home_folder = getToolByName(self, 'portal_membership').getHomeFolder()
        
        if home_folder == None:
            msgid = _(u"no_home_folder_msg", default=u"User did not have a Home Folder, could not create Favorite Link for ${path}" , mapping={ u"path" : link_url})
            translated = self.context.translate(msgid)
            self.messages.add(translated, type=u"warn")
            #self.messages.add(_(u"User did not have a Home Folder, could not create Favorite Link for %s") % link_url, type=u"warn")
        else:
            if not home_folder.has_key('favorites'):
                fav = typestool.constructContent(type_name="Favorites Folder", container=home_folder, id='favorites')
                home_folder[fav].setTitle(_(u"Favorites"))
                home_folder['favorites'].setExcludeFromNav(True)
            fav = home_folder['favorites']
            if not fav.has_key('fav'+link_uid):
                link = createContentInContainer(fav, "Favorite", checkConstrains=False, id='fav' + link_uid, title='fav'+link_uid, target_uid = link_uid)
                
                msgid = _(u"fav_created_msg", default=u"Favorites Link created for ${path}" , mapping={ u"path" : link_url})
                translated = self.context.translate(msgid)
                self.messages.add(translated, type=u"info")
                #self.messages.add(_(u"Favorites Link created for %s") % link_url, type=u"info")
            else:           
                msgid = _(u"fav_doubled_msg", default=u"Favorites Link already exists for ${path}" , mapping={ u"path" : link_url})
                translated = self.context.translate(msgid)
                self.messages.add(translated, type=u"warn")
                #self.messages.add(_(u"Favorites Link already exists for %s") % link_url, type=u"warn")
        return self.request.RESPONSE.redirect(self.context.absolute_url())
    
class RemoveFavoriteView(FavoriteView):

    def __call__(self):
        self.messages = IStatusMessage(self.request)
        
        link_uid = self.getUID()
        
        typestool = getToolByName(self, 'portal_types')
        home_folder = getToolByName(self, 'portal_membership').getHomeFolder()
        fav_folder = home_folder['favorites']
        try: 
            fav_folder.manage_delObjects(['fav'+link_uid])
            
            self.messages.add(_(u"Favorite deleted") , type=u"info")
        except:
            self.messages.add(_(u"Could not delete Favorite") , type=u"error")
        return self.request.RESPONSE.redirect(self.context.absolute_url())

class ExistsFavoriteView(FavoriteView):
    
    def __call__(self):
        link_uid = self.getUID()
        
        typestool = getToolByName(self, 'portal_types')
        home_folder = getToolByName(self, 'portal_membership').getHomeFolder()
        
        if home_folder != None and home_folder.has_key('favorites') and home_folder['favorites'].has_key('fav'+link_uid):
            return True
        return False

