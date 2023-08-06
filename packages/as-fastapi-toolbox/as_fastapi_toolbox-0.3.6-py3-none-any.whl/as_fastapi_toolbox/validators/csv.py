

class CommaSeparatedValues(str):
    """
    Turn an incoming comma separated values string into a list of strings
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=['1,2,3,4,5']
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        return v.split(',')

    def __repr__(self):
        return f'CommaSeparatedValues({super().__repr__()})'
