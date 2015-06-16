from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover.tiles.collection import ICollectionTile, CollectionTile
from zope.interface.declarations import implements


class IIsotopeCollectionTile(ICollectionTile):
    """ """


class IsotopeCollectionTile(CollectionTile):
    implements(IIsotopeCollectionTile)
    index = ViewPageTemplateFile('isotopecollection.pt')
    short_name = u'Isotope Collection tile'
