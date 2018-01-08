from validation.errors import ValidationError


def choices(*valid_choices):
    """
    :param valid_choices: valid choices list as positional arguments
    :return: validator object that performs validation
    """
    # we convert validate_choices list to the set object for more quick search
    choices_set = set(valid_choices)
    def validate(val):
        if val in choices_set:
            raise ValidationError(f'Valid choices are {valid_choices}')
    return validate

# todo: create @validator decorator for performing simple True/False validation
# @validator
# def validate_val(val):
#     if val == 'some val':
#         return True