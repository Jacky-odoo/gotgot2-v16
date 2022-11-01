# See LICENSE file for full copyright and licensing details.

{
    "name": "Web Widget Multiple Image v13.0",
    "version": "13.0.1.0.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    "category": "Image",
    "complexity": "easy",
    "depends": ["product"],
    "license": "AGPL-3",
    "summary": "Multiple web images widget",
    "data": [
        "security/ir.model.access.csv",
        # "view/templates.xml",
        "view/product_view.xml",
    ],
    'assets': {
        'web.assets_backend': [
            "web_widget_multi_image/static/library/lightbox/css/lightbox.css",
            "web_widget_multi_image/static/src/css/hoverbox.css",
            "web_widget_multi_image/static/library/lightbox/js/jquery.lightbox.js",
            "web_widget_multi_image/static/src/js/multi_image.js",
        ],
    },
    "website": "http://www.serpentcs.com",
    "qweb": ["static/src/xml/image_multi.xml"],
    "installable": True,
    "auto_install": False,
}
