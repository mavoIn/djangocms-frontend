from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.helpers import get_plugin_template

from . import forms, models
from .constants import CAROUSEL_TEMPLATE_CHOICES
from .. import carousel
from ... import settings

mixin_factory = settings.get_renderer(carousel)


@plugin_pool.register_plugin
class CarouselPlugin(mixin_factory("Carousel"), CMSPluginBase):
    """
    Components > "Carousel" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    name = _("Carousel")
    module = _("Interface")
    model = models.Carousel
    form = forms.CarouselForm
    allow_children = True
    child_classes = ["CarouselSlidePlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    ("carousel_aspect_ratio", "carousel_interval"),
                    ("carousel_controls", "carousel_indicators"),
                    ("carousel_keyboard", "carousel_wrap"),
                    ("carousel_ride", "carousel_pause"),
                )
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "template",
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, "carousel", "carousel", CAROUSEL_TEMPLATE_CHOICES
        )


@plugin_pool.register_plugin
class CarouselSlidePlugin(mixin_factory("CarouselSlide"), CMSPluginBase):
    """
    Components > "Carousel Slide" Plugin
    https://getbootstrap.com/docs/5.0/components/carousel/
    """

    name = _("Carousel slide")
    module = _("Interface")
    model = models.CarouselSlide
    form = forms.CarouselSlideForm
    allow_children = True
    parent_classes = ["CarouselPlugin"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "carousel_image",
                    "carousel_content",
                )
            },
        ),
        (
            _("Link settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("external_link", "internal_link"),
                    ("mailto", "phone"),
                    ("anchor", "target"),
                ),
            },
        ),
        (
            _("Advanced settings"),
            {
                "classes": ("collapse",),
                "fields": (
                    "tag_type",
                    "attributes",
                ),
            },
        ),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance.parent.get_plugin_instance()[0],
            "carousel",
            "slide",
            CAROUSEL_TEMPLATE_CHOICES,
        )