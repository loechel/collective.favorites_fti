# coding=utf-8

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

from Products.statusmessages.interfaces import IStatusMessage

from logging import getLogger
logger = getLogger('netstal')

from netstal.theme import MessageFactory as _

def createFavFolder(event):
    request = event.object.REQUEST

    home_folder = getToolByName(event.object, 'portal_membership').getHomeFolder()
    if home_folder != None:        
        if not home_folder.has_key('favorites'):
            favFolder = home_folder.invokeFactory(type_name="Folder", id='favorites', language= '')
            home_folder['favorites'].setTitle('Favorites')


class AddFavoriteView(BrowserView):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.messages = IStatusMessage(self.request)
        
        link_id = self.context.id
        link_title = self.context.title
        link_url = self.context.absolute_url()
        
        home_folder = getToolByName(self, 'portal_membership').getHomeFolder()
        
        if home_folder != None:
            if not home_folder.has_key('favorites'):
                home_folder.invokeFactory(type_name="Folder", id='favorites', Title='Favorites', language= '')
            else:
                fav = home_folder['favorites']
                if not fav.has_key(link_id):
                    link = fav.invokeFactory(type_name="Link", id=link_id, language= '')
                    fav[link].setTitle(link_title)
                    
                    fav[link].setRemoteUrl(link_url)
                    self.messages.add(_(u"Favorites Link created for %s") % link_url, type=u"info")
                else:           
                    self.messages.add(_(u"Favorites Link already exists for %s") % link_url, type=u"warn")
        return self.request.RESPONSE.redirect(self.context.absolute_url())
    
