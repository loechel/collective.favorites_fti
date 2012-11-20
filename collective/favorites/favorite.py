from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder

from zope.interface import invariant, Invalid, Interface, implements
from AccessControl import ClassSecurityInfo

from z3c.form import group, field

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.app.uuid.utils import uuidToObject

from collective.favorites import MessageFactory as _

from logging import getLogger
logger = getLogger('collective.favorite')


# Interface class; used to define content-type schema.

class IFavorite(form.Schema):
    """
    An internal Favorite
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/favorite.xml to define the content type
    # and add directives here as necessary.
    
    #form.model("models/favorite.xml")

    title = schema.TextLine(title = _(u'Title'), description = _(""))

    description = schema.Text(title = _(u'Description'), description = _(""))

    target_uid = schema.ASCIILine(title = _(u'Target UID'), description = _(u""))

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Favorite(dexterity.Item):
    grok.implements(IFavorite)
    
    # Add your class methods and properties here

    def target(self):
        obj = uuidToObject(self.target_uid)
        if not obj:
            # Could not find object
            raise RuntimeError(u"Could not look-up UUID:", self.target_uid)
        return obj
        
    @property
    def title(self):
        if self.target_uid != None:
            return self.target().title
        else:
            return ""

    @title.setter
    def title(self, value):
        return

    @property
    def description(self):
        if self.target_uid != None:
            return self.target().Description()
        else:
            return ""

    @description.setter
    def description(self, value):
        return
        
# View class
# The view will automatically use a similarly named template in
# favorite_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class FavoriteView(grok.View):
    grok.context(IFavorite)
    grok.require('zope2.View')
    
    grok.name('view')
    
    security = ClassSecurityInfo()

        
    def render(self):
        target = self.context.target()
        return self.request.RESPONSE.redirect(target.absolute_url())
