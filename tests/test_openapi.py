from unittest.mock import create_autospec

from openapi_specgen import (ApiKeyAuth, BearerAuth, OpenApi, OpenApiParam,
                             OpenApiPath, OpenApiResponse, OpenApiSecurity)
from openapi_specgen.schema import OpenApiSchemaResolver

from .utils import DataclassNestedObject, MarshmallowSchema, DataclassEnum


def test_openapi_with_dataclass():
    expected_openapi_dict = {
        'openapi': '3.0.2',
        'info': {
            'title': 'test_api',
            'version': '3.0.2'
        },
        'paths': {
            '/test_path': {
                'get': {
                    'description': '',
                    'summary': '',
                    'operationId': '[get]_/test_path',
                    'responses': {
                        '200': {
                            'description': 'test_response',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': '#/components/schemas/DataclassNestedObject'}
                                }
                            }
                        }
                    },
                    'parameters': [
                        {
                            'required': True,
                            'name': 'test_param',
                            'in': 'query',
                            'schema': {
                                'title': 'Test_Param',
                                'type': 'string'
                            }
                        }
                    ]
                }
            }
        },
        'components': {
            'schemas': {
                'DataclassObject': {
                    'title': 'DataclassObject',
                    'required': ['str_field', 'int_field', 'float_field',
                                 'boolean_field', 'list_field', 'date_field', 'datetime_field'],
                    'type': 'object',
                    'properties': {
                        'str_field': {'type': 'string'},
                        'int_field': {'type': 'integer'},
                        'float_field': {'type': 'number'},
                        'boolean_field': {'type': 'boolean'},
                        'list_field': {'type': 'array', 'items': {}},
                        'date_field': {'type': 'string', 'format': 'date'},
                        'datetime_field': {'type': 'string', 'format': 'date-time'},
                    }
                },
                'DataclassNestedObject': {
                    'title': 'DataclassNestedObject',
                    'required': ['str_field', 'nested_object'],
                    'type': 'object',
                    'properties': {
                        'str_field': {
                            'type': 'string'
                        },
                        'nested_object': {
                            '$ref': '#/components/schemas/DataclassObject'
                        }
                    }
                }
            }

        }
    }

    test_resp = OpenApiResponse('test_response', data_type=DataclassNestedObject)
    test_param = OpenApiParam('test_param', 'query', data_type=str)
    test_path = OpenApiPath('/test_path', 'get', [test_resp], [test_param])
    test_api = OpenApi('test_api', [test_path])
    assert expected_openapi_dict == test_api.as_dict()


def test_openapi_with_enum():
    expected_openapi_dict = {
        'components': {'schemas': {'DataclassEnum': {'properties': {'any_enum_field': {'type': 'string'},
                                                                    'boolean_field': {'type': 'boolean'},
                                                                    'date_field': {'format': 'date',
                                                                                   'type': 'string'},
                                                                    'datetime_field': {'format': 'date-time',
                                                                                       'type': 'string'},
                                                                    'float_field': {'type': 'number'},
                                                                    'int_enum_field': {'type': 'integer'},
                                                                    'int_enum_field3': {'type': 'integer'},
                                                                    'int_field': {'type': 'integer'},
                                                                    'list_field': {'items': {},
                                                                                   'type': 'array'},
                                                                    'str_field': {'type': 'string'}},
                                                     'required': ['str_field',
                                                                  'int_field',
                                                                  'float_field',
                                                                  'boolean_field',
                                                                  'list_field',
                                                                  'date_field',
                                                                  'datetime_field',
                                                                  'any_enum_field',
                                                                  'int_enum_field',
                                                                  'int_enum_field3'],
                                                     'title': 'DataclassEnum',
                                                     'type': 'object'}}},
        'info': {'title': 'test_api', 'version': '3.0.2'},
        'openapi': '3.0.2',
        'paths': {'/test_path': {'get': {'description': '',
                                         'operationId': '[get]_/test_path',
                                         'parameters': [{'in': 'query',
                                                         'name': 'test_param',
                                                         'required': True,
                                                         'schema': {'title': 'Test_Param',
                                                                    'type': 'string'}}],
                                         'responses': {'200': {'content': {'application/json': {
                                             'schema': {'$ref': '#/components/schemas/DataclassEnum'}}},
                                             'description': 'test_response'}},
                                         'summary': ''}}}}
    test_resp = OpenApiResponse('test_response', data_type=DataclassEnum)
    test_param = OpenApiParam('test_param', 'query', data_type=str)
    test_path = OpenApiPath('/test_path', 'get', [test_resp], [test_param])
    test_api = OpenApi('test_api', [test_path])
    assert expected_openapi_dict == test_api.as_dict()


def test_openapi_with_marshmallow():
    expected_openapi_dict = {
        'openapi': '3.0.2',
        'info': {
            'title': 'test_api',
            'version': '3.0.2'
        },
        'security': [
            {'ApiKeyAuth': []},
            {'BearerAuth': []}
        ],
        'paths': {
            '/test_path': {
                'get': {
                    'description': '',
                    'summary': '',
                    'operationId': '[get]_/test_path',
                    'responses': {
                        '200': {
                            'description': 'test_response',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': '#/components/schemas/Marshmallow'}
                                }
                            }
                        }
                    },
                    'parameters': [
                        {
                            'required': True,
                            'name': 'test_param',
                            'in': 'query',
                            'schema': {
                                'title': 'Test_Param',
                                'type': 'string'
                            }
                        }
                    ]
                }
            }
        },
        'components': {
            'schemas': {
                'Marshmallow': {
                    'title': 'Marshmallow',
                    'required': ['str_field'],
                    'type': 'object',
                    'properties': {
                        'str_field': {'type': 'string'},
                        'int_field': {'type': 'integer'},
                        'float_field': {'type': 'number'},
                        'boolean_field': {'type': 'boolean'},
                        'list_field': {'type': 'array', 'items': {'type': 'string'}},
                        'date_field': {'type': 'string', 'format': 'date'},
                        'datetime_field': {'type': 'string', 'format': 'date-time'},
                    }
                }
            },
            'securitySchemes': {
                'ApiKeyAuth': {'in': 'header', 'name': 'X-API-Key', 'type': 'apiKey'},
                'BearerAuth': {'scheme': 'bearer', 'type': 'http'}
            }
        }
    }

    test_resp = OpenApiResponse('test_response', data_type=MarshmallowSchema)
    test_param = OpenApiParam('test_param', 'query', data_type=str)
    test_path = OpenApiPath('/test_path', 'get', [test_resp], [test_param])
    test_security = OpenApiSecurity(bearer_auth=BearerAuth(), api_key_auth=ApiKeyAuth())
    test_api = OpenApi('test_api', [test_path], security=test_security)
    assert expected_openapi_dict == test_api.as_dict()


def test_add_resolver():
    schema_resolver_mock = create_autospec(OpenApiSchemaResolver)

    openapi = OpenApi("test_api", [], schema_resolver=schema_resolver_mock)

    openapi.add_resolver("foo")
    schema_resolver_mock.add_resolver.assert_called_with("foo")


def test_remove_resolver():
    schema_resolver_mock = create_autospec(OpenApiSchemaResolver)

    openapi = OpenApi("test_api", [], schema_resolver=schema_resolver_mock)

    openapi.remove_resolver("foo")
    schema_resolver_mock.remove_resolver.assert_called_with("foo")
