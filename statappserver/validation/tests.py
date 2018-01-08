import warnings
from decimal import Decimal

from validation.schema import Schema


def test_simple_schema():
    schema = Schema({
        'id': int,
        'name': str,
        'age': int,
        'decimal': Decimal,
        'float': float
    })
    data = {
        'id': '12',
        'name': 'Some name',
        'age': 63,
        'decimal': '45.4',
        'float': '45.4'
    }
    expected_result = {
        'id': 12,
        'name': 'Some name',
        'age': 63,
        'decimal': Decimal('45.4'),
        'float': 45.4
    }
    schema.validate(data)
    assert schema.data == expected_result


def test_raise_warning_on_access_data_before_validation():
    with warnings.catch_warnings(record=True) as warns:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        s = Schema({'int': int})
        # access to data before validation
        s.data
        assert len(warns) == 1
        assert issubclass(warns[-1].category, Warning)
        assert ('`data` attribute is empty, maybe you do not call '
                'method `validate(data)` before accessing to '
                'the `data` param or occurs some error which '
                'you does not handle') in str(warns[-1].message)


def test_error_handling():
    s = Schema({'int': int})
    s.validate({'int': '1.2'})
    print(s.data)

if __name__ == '__main__':
    test_simple_schema()
    test_raise_warning_on_access_data_before_validation()
    test_error_handling()