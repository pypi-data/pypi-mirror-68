import pytest
import numpy as np
from random import randint, choices


from hangar.typesystem import StringVariableShape


class TestInvalidValues:

    @pytest.mark.parametrize('coltype', ['ndarray', np.ndarray, 32, {'foo': 'bar'}, ascii])
    def test_column_type_must_be_str(self, coltype):
        with pytest.raises(ValueError):
            StringVariableShape(dtype=str, column_layout='flat', column_type=coltype)

    @pytest.mark.parametrize('collayout', ['f', 'n', None, 32, {'foo': 'bar'}, ascii])
    def test_column_layout_must_be_valid_value(self, collayout):
        with pytest.raises(ValueError):
            StringVariableShape(dtype=str, column_layout=collayout)

    @pytest.mark.parametrize('backend', ['00', 24, {'30': '30'}, ('30',), ['50',], ascii, 'None'])
    def test_variable_shape_backend_code_valid_value(self, backend):
        with pytest.raises(ValueError):
            StringVariableShape(dtype=str, column_layout='flat', backend=backend)

    @pytest.mark.parametrize('opts', ['val', [], (), [('k', 'v')], 10, ({'k': 'v'},), ascii])
    def test_backend_options_must_be_dict_or_nonetype(self, opts):
        with pytest.raises(TypeError):
            StringVariableShape(dtype=str, column_layout='flat', backend='30', backend_options=opts)

    def test_backend_must_be_specified_if_backend_options_provided(self):
        with pytest.raises(ValueError):
            StringVariableShape(dtype=str, column_layout='flat', backend_options={})

    @pytest.mark.parametrize('schema_type', ['fixed_shape', True, 'str', np.uint8, 3, ascii])
    def test_variable_shape_must_have_variable_shape_schema_type(self, schema_type):
        with pytest.raises(ValueError):
            StringVariableShape(dtype=str, column_layout='flat', schema_type=schema_type)


# ----------------------- Fixtures for Valid Schema ---------------------------


@pytest.fixture(params=['nested', 'flat'], scope='class')
def column_layout(request):
    return request.param


@pytest.fixture(params=['30'], scope='class')
def backend(request):
    return request.param


@pytest.fixture(params=[{}], scope='class')
def backend_options(request):
    return request.param


@pytest.fixture(scope='class')
def valid_schema(column_layout, backend, backend_options):
    schema = StringVariableShape(
        dtype=str, column_layout=column_layout, backend=backend, backend_options=backend_options)
    return schema


class TestValidSchema:

    @pytest.mark.parametrize('data', [
        'hello', 'world how are you?', '\n what\'s up',
        'loob!', 'a\xac\u1234\u20ac\U00008000', 'lol'
    ])
    def test_valid_data(self, valid_schema, data):
        res = valid_schema.verify_data_compatible(data)
        assert res.compatible is True
        assert res.reason == ''

    @pytest.mark.parametrize('data', [chr(24523), chr(253), chr(6222)])
    def test_large_unicode_codepoints_strings_compatible(self, valid_schema, data):
        res = valid_schema.verify_data_compatible(data)
        assert res.compatible is True
        assert res.reason == ''

    def test_strings_over_2MB_size_not_allowed(self, valid_schema):
        data = ''.join(['a' for _ in range(2_000_001)])
        res = valid_schema.verify_data_compatible(data)
        assert res.compatible is False



