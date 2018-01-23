"""Activity Configuration"""

from collections import OrderedDict as odict

ACTIVITY_CONFIG = odict([
    ('Upload', odict([
        ('Fields', odict([
            ('id', ['display']),
            ('thesis_title', ['create', 'update', 'display']),
            ('content', ['create', 'update', 'display']),
            ('keywords', ['create', 'update', 'display']),
            ('abstract', ['create', 'update', 'display']),
            ('creation_date', ['display']),
            ('last_updated', ['display'])
        ])),
    ])),
    ('Distribution', odict([
        ('Fields', odict([
            ('reviewer1', ['create', 'update', 'display']),
            ('reviewer2', ['create', 'update', 'display']),
            ('reviewer3', ['create', 'update', 'display']),
            ('creation_date', ['display']),
            ('last_updated', ['display'])
        ])),
    ])),
    ('Review', odict([
        ('Fields', odict([
            ('conclusion', ['create', 'update', 'display']),
            ('creation_date', ['display']),
            ('last_updated', ['display'])
        ])),
        ('Relations', odict([
            ('ReviewLine', odict([
                ('result', ['create', 'update', 'display']),
            ]))
        ]))
    ]))
])

#  config for Corge commented out to demonstrate that config is optional

# field configuration for WYSIWYG editor

WYSIWYG_CONFIG = {
    'Upload': ['abstract']
}

# custom form registration

FORM_CONFIG = {
}
