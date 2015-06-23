from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.collection import ICollectionTile, CollectionTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.autoform import directives as form
from zope import schema
from zope.interface.declarations import implements


class IIsotopeCollectionTile(ICollectionTile):
    """ """

    form.omitted('column_width')
    form.no_omit(ITileEditForm, 'column_width')
    column_width = schema.Int(
        title=u"Column width",
        description=u'Numeric width',
        required=False,
        default=250,
    )

    form.omitted('column_gutter')
    form.no_omit(ITileEditForm, 'column_gutter')
    column_gutter = schema.Int(
        title=u"Column gutter",
        description=u'Numeric space between columns',
        required=False,
        default=15,
    )

    form.omitted('image_scale_dir')
    form.no_omit(ITileEditForm, 'image_scale_dir')
    image_scale_dir = schema.TextLine(
        title=u"Image scale crop direction",
        description=u"Can be 'thumbnail' (uncropped) or 'down' (cropped)",
        required=False,
        default=u'thumbnail',
    )

    form.omitted('column_css_class')
    form.no_omit(IDefaultConfigureForm, 'column_css_class')
    form.widget(column_css_class='collective.cover.tiles.' \
        'configuration_widgets.cssclasswidget.CSSClassFieldWidget')
    column_css_class = schema.Choice(
        title=u"Column CSS Class",
        required=False,
        vocabulary='collective.cover.TileStyles',
        default=u'tile-default',
    )


class IsotopeCollectionTile(CollectionTile):
    implements(IIsotopeCollectionTile)
    index = ViewPageTemplateFile('isotopecollection.pt')
    short_name = u'Isotope Collection tile'

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._has_image_field(item) and self._field_is_visible('image'):
            tile_conf = self.get_tile_configuration()
            image_conf = tile_conf.get('image', None)
            if image_conf:
                scaleconf = image_conf['imgsize']
                # scale string is something like: 'mini 200:200'
                # we need the name only: 'mini'
                if scaleconf == '_original':
                    scale = None
                else:
                    scale = scaleconf.split(' ')[0]
                scales = item.restrictedTraverse('@@images')
                crop_dir = self.data.get('image_scale_dir', 'thumbnail')
                return scales.scale('image', scale, direction=crop_dir)

    @property
    def column_css_class(self):
        # XXX fixme
        tile_conf = self.get_tile_configuration()
        return tile_conf.get('column_css_class', {}).values()[0][0]
