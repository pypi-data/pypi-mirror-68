TEST_ODML_FILE = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                 '<?xml-stylesheet type="text/xsl" href="odmlTerms.xsl"?>\n' \
                 '<?xml-stylesheet type="text/xsl" href="odml.xsl"?>\n' \
                 '<odML xmlns:gui="http://www.g-node.org/guiml" version="1.1">\n' \
                    '<version>1</version>\n' \
                    '<date>2015-07-16</date>\n'\
                    '<author>Author</author>\n'\
                    '<section>\n'\
                        '<type>experiment</type>\n'\
                        '<name>Experiment</name>\n'\
                        '<property>\n'\
                          '<name>start-time</name>\n'\
                          '<type>string</type>\n'\
                          '<value>17.12.2013, 10:08:00</value>\n'\
                          '<id>183be569-fb56-4fb7-ae82-8803d21336d2</id>\n'\
                        '</property>\n'\
                        '<property>\n'\
                          '<name>temperature</name>\n'\
                          '<type>string</type>\n'\
                          '<value>23</value>\n'\
                          '<id>bf1b9d02-0ee2-4677-9aed-7cc20aff4aa9</id>\n'\
                        '</property>\n'\
                        '<property>\n'\
                          '<name>scenario-title</name>\n'\
                          '<type>string</type>\n'\
                          '<value>AUDITORY ERP PROTOCOL IN CHILDREN WITH DEVELOPMENTAL COORDINATION DISORDER</value>\n'\
                          '<id>31c10e2d-d8ad-404e-8bda-1e381b08408c</id>\n'\
                        '</property>\n'\
                        '<id>97d939af-6127-4d1d-a3b3-59cf978a76a4</id>\n'\
                    '</section>\n'\
                    '<section>\n'\
                        '<type>collection</type>\n'\
                        '<name>Devices</name>\n'\
                        '<section>\n'\
                          '<type>hardware</type>\n'\
                          '<name>Response button</name>\n'\
                          '<property>\n'\
                            '<name>description</name>\n'\
                            '<type>string</type>\n'\
                            '<value>"A response button is an electrical component that can break an electrical circuit</value>\n'\
                            '<id>15edbf73-dd70-4646-8972-fa1153d400a2</id>\n'\
                          '</property>\n'\
                          '<id>e87285f3-bf85-4cad-9e11-006ed6b2c970</id>\n'\
                        '</section>\n'\
                        '<section>\n'\
                          '<type>hardware</type>\n'\
                          '<name>Power supply</name>\n'\
                          '<property>\n'\
                            '<name>type</name>\n'\
                            '<type>string</type>\n'\
                            '<value>PS607110246wr</value>\n'\
                            '<id>4ce05388-d259-43f5-85cb-49b875ecb669</id>\n'\
                          '</property>\n'\
                          '<id>ae776c94-2885-49a0-a1b1-88ef6e7567f2</id>\n'\
                        '</section>\n'\
                    '</section>\n'\
                    '<id>c876ec98-6152-4fb5-8b2a-ae3ab74b3366</id>\n'\
                    '</odML>\n'

GENERATED_STRUCTURE = {
    'experiment__experiment': {
        'corresponding_term': {'name': 'Experiment', 'type': 'experiment', 'parent_sections': ''},
        'props': {
            'start-time': {
                'type': 'string',
                'example_value': "['17.12.2013, 10:08:00']",
                'corresponding_term': {
                    'name': 'start-time',
                    'type': 'string',
                    'parent_sections': 'experiment__Experiment'}
            },
            'scenario-title': {
                'type': 'string',
                'example_value':
                    "['AUDITORY ERP PROTOCOL IN CHILDREN WITH DEVELOPMENTAL COORDINATION DISORDER']",
                'corresponding_term': {
                    'name': 'scenario-title',
                    'type': 'string',
                    'parent_sections': 'experiment__Experiment'}
            },
            'temperature': {
                'type': 'string',
                'example_value': "['23']",
                'corresponding_term': {
                    'name': 'temperature',
                    'type': 'string',
                    'parent_sections': 'experiment__Experiment'}
            }
        }
    },
    'collection__devices': {
        'corresponding_term': {
            'name': 'Devices',
            'type': 'collection',
            'parent_sections': ''
        },
        'props': {}
    },
    'hardware__response button': {
        'corresponding_term': {
            'name': 'Response button',
            'type': 'hardware',
            'parent_sections': 'collection__Devices'
        },
        'props': {
            'description': {
                'type': 'string',
                'example_value':
                    '[\'"A response button is an electrical component that can break an electrical circuit\']',
                'corresponding_term': {
                    'name': 'description',
                    'type': 'string',
                    'parent_sections': 'collection__Devices___hardware__Response button'}
            }
        }
    },
    'hardware__power supply': {
        'corresponding_term': {
            'name': 'Power supply',
            'type': 'hardware',
            'parent_sections': 'collection__Devices'
        },
        'props': {
            'type': {
                'type': 'string',
                'example_value': "['PS607110246wr']",
                'corresponding_term': {
                    'name': 'type',
                    'type': 'string',
                    'parent_sections': 'collection__Devices___hardware__Power supply'}
            }
        }
    }
}