# coding=utf-8

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from plone.uuid.interfaces import IUUID

from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

from Products.statusmessages.interfaces import IStatusMessage

from Products.ATContentTypes.lib import constraintypes

from logging import getLogger
logger = getLogger('collective.favorites')

from collective.favorites import MessageFactory as _



def createFavFolder(event):
    request = event.object.REQUEST
    
    home_folder = getToolByName(event.object, 'portal_membership').getHomeFolder()
    
    if home_folder != None:
        if not home_folder.has_key('favorites'):
            #favFolder = home_folder.invokeFactory(type_name="collective.favorites.favoritesfolder", id='favorites', language= '')
            typestool = getToolByName(self.context, 'portal_types')
            typestool.constructContent(type_name="collective.favorites.favoritesfolder", container=home_folder, id='favorites')
            home_folder['favorites'].setTitle('Favorites')


class AddFavoriteView(BrowserView):
    
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

    def __call__(self):
        self.messages = IStatusMessage(self.request)
        
        link_id = self.context.id
        link_title = self.context.title
        link_url = self.context.absolute_url()
        link_uid = self.getUID()
        
        #import ipdb; ipdb.set_trace()
        
        typestool = getToolByName(self, 'portal_types')
        home_folder = getToolByName(self, 'portal_membership').getHomeFolder()
        
        if home_folder == None:
            self.messages.add(_(u"User did not have a Home Folder, could not create Favorite Link for %s") % link_url, type=u"warn")
        else:
            if not home_folder.has_key('favorites'):
                #home_folder.invokeFactory(type_name="collective.favorites.favoritesfolder", id='favorites', Title='Favorites', language= '')
                fav = typestool.constructContent(type_name="collective.favorites.favoritesfolder", container=home_folder, id='favorites')
                home_folder[fav].setTitle(_(u"Favorites"))
            fav = home_folder['favorites']
            if not fav.has_key('fav'+link_uid):
                
                import ipdb; ipdb.set_trace()
                
                link = typestool.constructContent(type_name="collective.favorites.favorite", container=fav, id='fav' + link_uid, target_uid = link_uid)
                #link = fav.invokeFactory(type_name="collective.favorites.favorite", id='fav' + link_uid, language= '')
                #fav[link].setTitle(link_title)
                
                #fav[link].setRemoteUrl(link_url)
                fav[link].target_uid = link_uid
                self.messages.add(_(u"Favorites Link created for %s") % link_url, type=u"info")
            else:           
                self.messages.add(_(u"Favorites Link already exists for %s") % link_url, type=u"warn")
        return self.request.RESPONSE.redirect(self.context.absolute_url())
    
