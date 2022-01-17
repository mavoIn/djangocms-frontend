import importlib

from django.conf import settings
from django.utils.translation import gettext_lazy as _

EMPTY_CHOICE = (("", "------"),)

DEVICE_CHOICES = (
    ("xs", _("Extra small")),  # default <576px
    ("sm", _("Small")),  # default ≥576px
    ("md", _("Medium")),  # default ≥768px
    ("lg", _("Large")),  # default ≥992px
    ("xl", _("Extra large")),  # default ≥1200px
)
DEVICE_SIZES = tuple([size for size, name in DEVICE_CHOICES])

# Only adding block elements
TAG_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_TAG_CHOICES",
    ["div", "section", "article", "header", "footer", "aside"],
)
TAG_CHOICES = tuple((entry, entry) for entry in TAG_CHOICES)

HEADER_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_HEADER_CHOICES",
    (
        ("h1", _("Heading 1"),),
        ("h2", _("Heading 2"),),
        ("h3", _("Heading 3"),),
        ("h4", _("Heading 4"),),
        ("h5", _("Heading 5"),),
    )
)

COLOR_STYLE_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_COLOR_STYLE_CHOICES",
    (
        ("primary", _("Primary")),
        ("secondary", _("Secondary")),
        ("success", _("Success")),
        ("danger", _("Danger")),
        ("warning", _("Warning")),
        ("info", _("Info")),
        ("light", _("Light")),
        ("dark", _("Dark")),
    ),
)

ALIGN_CHOICES = (
    ("text-left", _("Left")),
    ("text-center", _("Center")),
    ("text-right", _("Right")),
)


SPACER_PROPERTY_CHOICES = (
    ("m", "margin"),
    ("p", "padding"),
)

SPACER_SIDE_CHOICES = (
    ("", "*"),
    ("t", "*-top"),
    ("r", "*-right"),
    ("b", "*-bottom"),
    ("l", "*-left"),
    ("x", "*-left & *-right"),
    ("y", "*-top & *-bottom"),
)

SPACER_SIZE_CHOICES = getattr(
    settings,
    "DJANGOCMS_FRONTEND_SPACER_SIZES",
    (
        ("0", "* 0"),
        ("1", "* .25"),
        ("2", "* .5"),
        ("3", "* 1"),
        ("4", "* 1.5"),
        ("5", "* 3"),
    ),
)

framework = getattr(settings, "DJANGOCMS_FRONTEND_FRAMEWORK", "bootstrap5")
theme = getattr(settings, "DJANGOCMS_FRONTEND_THEME", "djangocms_frontend")


def preparator_factory(framework):
    try:
        fr_settings = importlib.import_module(framework)
        if hasattr(fr_settings, "prepare_instance"):
            return fr_settings.prepare_instance
    except ModuleNotFoundError:
        pass
    return lambda *args, **kwargs: None


prepare_instance = preparator_factory(framework)

theme_render_path = f"{theme}.renderer.{framework}"


def get_renderer(my_module):
    def render_factory(name, theme_module, render_module):
        cls = f"{name}RenderMixin"
        return type(
            cls,
            tuple(
                getattr(module, cls, None)
                for module in (render_module, theme_module)
                if module is not None and getattr(module, cls, None) is not None
            ),
            dict(),
        )  # Empty Mix

    if not isinstance(my_module, str):
        my_module = my_module.__name__
    try:
        theme_module = importlib.import_module(theme_render_path)
    except ModuleNotFoundError:
        theme_module = None

    try:
        render_module = importlib.import_module(f"{my_module}.renderer.{framework}")
    except ModuleNotFoundError:
        render_module = None

    return lambda name: render_factory(name, theme_module, render_module)