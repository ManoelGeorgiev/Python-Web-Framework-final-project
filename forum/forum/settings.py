import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ir+x=4a(hsmn29y0)+r8fryb0uotiw0pav%tsi-o%e1%i%^40^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forum.accounts',
    'forum.main',
    'hitcount',
    'tinymce',
    'django_bleach',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'forum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'forum.common.context_processors.categories',
                'forum.common.context_processors.search',
            ],
        },
    },
]

WSGI_APPLICATION = 'forum.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'forum',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_root'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.ForumUser'

# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = [
    'p', 'b', 'i', 'u', 'em', 'strong', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'span', 'ul', 'li', 'br',
    'code',
    'iframe', "tt", "blockquote", "hr", "ol", "dd", "dt", "img", "sub", "sup", "table", "thead", "tbody", "tfoot", "tr",
    "th", "td",
]

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style', 'src', "id", "alt", "class", "width", "height", ]

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = [":active", "::after (:after)", "align-content", "align-items", "align-self",
                         "all", "<angle>", "animation", "animation-delay", "animation-direction",
                         "animation-duration", "animation-fill-mode", "animation-iteration-count",
                         "animation-name", "animation-play-state", "animation-timing-function",
                         "@annotation", "annotation()", "attr()", "::backdrop", "backface-visibility",
                         "background", "background-attachment", "background-blend-mode",
                         "background-clip", "background-color", "background-image", "background-origin",
                         "background-position", "background-repeat", "background-size", "<basic-shape>",
                         "::before (:before)", "<blend-mode>", "blur()", "border", "border-bottom",
                         "border-bottom-color", "border-bottom-left-radius",
                         "border-bottom-right-radius", "border-bottom-style", "border-bottom-width",
                         "border-collapse", "border-color", "border-image", "border-image-outset",
                         "border-image-repeat", "border-image-slice", "border-image-source",
                         "border-image-width", "border-left", "border-left-color", "border-left-style",
                         "border-left-width", "border-radius", "border-right", "border-right-color",
                         "border-right-style", "border-right-width", "border-spacing", "border-style",
                         "border-top", "border-top-color", "border-top-left-radius",
                         "border-top-right-radius", "border-top-style", "border-top-width",
                         "border-width", "bottom", "box-decoration-break", "box-shadow", "box-sizing",
                         "break-after", "break-before", "break-inside", "brightness()", "calc()",
                         "caption-side", "ch", "@character-variant", "character-variant()", "@charset",
                         ":checked", "circle()", "clear", "clip", "clip-path", "cm", "color", "<color>",
                         "columns", "column-count", "column-fill", "column-gap", "column-rule",
                         "column-rule-color", "column-rule-style", "column-rule-width", "column-span",
                         "column-width", "content", "contrast()", "<counter>", "counter-increment",
                         "counter-reset", "@counter-style", "cubic-bezier()", "cursor",
                         "<custom-ident>", ":default", "deg", ":dir()", "direction", ":disabled",
                         "display", "@document", "dpcm", "dpi", "dppx", "drop-shadow()", "element()",
                         "ellipse()", "em", ":empty", "empty-cells", ":enabled", "ex", "filter",
                         ":first", ":first-child", "::first-letter", "::first-line",
                         ":first-of-type", "flex", "flex-basis", "flex-direction",
                         "flex-flow", "flex-grow", "flex-shrink", "flex-wrap", "float", ":focus",
                         "font", "@font-face", "font-family", "font-feature-settings",
                         "@font-feature-values", "font-kerning", "font-language-override", "font-size",
                         "font-size-adjust", "font-stretch", "font-style", "font-synthesis",
                         "font-variant", "font-variant-alternates", "font-variant-caps",
                         "font-variant-east-asian", "font-variant-ligatures", "font-variant-numeric",
                         "font-variant-position", "font-weight", "<frequency>", ":fullscreen", "grad",
                         "<gradient>", "grayscale()", "grid", "grid-area", "grid-auto-columns",
                         "grid-auto-flow", "grid-auto-position", "grid-auto-rows", "grid-column",
                         "grid-column-start", "grid-column-end", "grid-row", "grid-row-start",
                         "grid-row-end", "grid-template", "grid-template-areas", "grid-template-rows",
                         "grid-template-columns", "height", ":hover", "hsl()", "hsla()", "hue-rotate()",
                         "hyphens", "hz", "<image>", "image()", "image-rendering", "image-resolution",
                         "image-orientation", "ime-mode", "@import", "in", ":indeterminate", "inherit",
                         "initial", ":in-range", "inset()", "<integer>", ":invalid", "invert()",
                         "isolation", "justify-content", "@keyframes", "khz", ":lang()", ":last-child",
                         ":last-of-type", "left", ":left", "<length>", "letter-spacing",
                         "linear-gradient()", "line-break", "line-height", ":link", "list-style",
                         "list-style-image", "list-style-position", "list-style-type", "margin",
                         "margin-bottom", "margin-left", "margin-right", "margin-top", "marks", "mask",
                         "mask-type", "matrix()", "matrix3d()", "max-height", "max-width", "@media",
                         "min-height", "minmax()", "min-width", "mix-blend-mode", "mm", "ms",
                         "@namespace", ":not()", ":nth-child()", ":nth-last-child()",
                         ":nth-last-of-type()", ":nth-of-type()", "<number>", "object-fit",
                         "object-position", ":only-child", ":only-of-type", "opacity", "opacity()",
                         ":optional", "order", "@ornaments", "ornaments()", "orphans", "outline",
                         "outline-color", "outline-offset", "outline-style", "outline-width",
                         ":out-of-range", "overflow", "overflow-wrap", "overflow-x", "overflow-y",
                         "padding", "padding-bottom", "padding-left", "padding-right", "padding-top",
                         "@page", "page-break-after", "page-break-before", "page-break-inside", "pc",
                         "<percentage>", "perspective", "perspective()", "perspective-origin",
                         "pointer-events", "polygon()", "position", "<position>", "pt", "px", "quotes",
                         "rad", "radial-gradient()", "<ratio>", ":read-only", ":read-write", "rect()",
                         "rem", "repeat()", "::repeat-index", "::repeat-item",
                         "repeating-linear-gradient()", "repeating-radial-gradient()", ":required",
                         "resize", "<resolution>", "rgb()", "rgba()", "right", ":right", ":root",
                         "rotate()", "rotatex()", "rotatey()", "rotatez()", "rotate3d()", "ruby-align",
                         "ruby-merge", "ruby-position", "s", "saturate()", "scale()", "scalex()",
                         "scaley()", "scalez()", "scale3d()", ":scope", "scroll-behavior",
                         "::selection", "sepia()", "<shape>", "shape-image-threshold", "shape-margin",
                         "shape-outside", "skew()", "skewx()", "skewy()", "steps()", "<string>",
                         "@styleset", "styleset()", "@stylistic", "stylistic()", "@supports", "@swash",
                         "swash()", "symbol()", "table-layout", "tab-size", ":target", "text-align",
                         "text-align-last", "text-combine-upright", "text-decoration",
                         "text-decoration-color", "text-decoration-line", "text-decoration-style",
                         "text-indent", "text-orientation", "text-overflow", "text-rendering",
                         "text-shadow", "text-transform", "text-underline-position", "<time>",
                         "<timing-function>", "top", "touch-action", "transform", "transform-origin",
                         "transform-style", "transition", "transition-delay", "transition-duration",
                         "transition-property", "transition-timing-function", "translate()",
                         "translatex()", "translatey()", "translatez()", "translate3d()", "turn",
                         "unicode-bidi", "unicode-range", "unset", "<uri>", "url()", "<user-ident>",
                         ":valid", "::value", "var()", "vertical-align", "vh", "@viewport",
                         "visibility", ":visited", "vmax", "vmin", "vw", "white-space", "widows",
                         "width", "will-change", "word-break", "word-spacing", "word-wrap",
                         "writing-mode", "z-index", ]

TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime
            contextmenu directionality searchreplace wordcount 
            autolink lists print
            ''',
    'toolbar1': '''
            preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'statusbar': True,
}
