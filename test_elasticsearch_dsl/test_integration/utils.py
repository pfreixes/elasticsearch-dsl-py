from elasticsearch_dsl import DocType, Date, Text, Keyword, construct_field, Mapping

user_field = construct_field('object')
user_field.field('name', 'text', fields={'raw': construct_field('keyword')})

class Repository(DocType):
    owner = user_field
    created_at = Date()
    description = Text(analyzer='snowball')
    tags = Keyword()

    class Meta:
        index = 'git'
        doc_type = 'repos'

class Commit(DocType):
    committed_date = Date()
    authored_date = Date()
    description = Text(analyzer='snowball')

    class Meta:
        index = 'git'
        mapping = Mapping('commits')
        mapping.meta('_parent', type='repos')

COMMIT_DOCS_WITH_MISSING = [
    {'parent': 'elasticsearch-dsl-py', '_id': '0'},                                         # Missing
    {'parent': 'elasticsearch-dsl-py', '_id': '3ca6e1e73a071a705b4babd2f581c91a2a3e5037'},  # Existing
    {'parent': 'elasticsearch-dsl-py', '_id': 'f'},                                         # Missing
    {'parent': 'elasticsearch-dsl-py', '_id': 'eb3e543323f189fd7b698e66295427204fff5755'},  # Existing
]

COMMIT_DOCS_WITH_ERRORS = [
    '0',                                                                                    # Error
    {'parent': 'elasticsearch-dsl-py', '_id': '3ca6e1e73a071a705b4babd2f581c91a2a3e5037'},  # Existing
    'f',                                                                                    # Error
    {'parent': 'elasticsearch-dsl-py', '_id': 'eb3e543323f189fd7b698e66295427204fff5755'},  # Existing
]

