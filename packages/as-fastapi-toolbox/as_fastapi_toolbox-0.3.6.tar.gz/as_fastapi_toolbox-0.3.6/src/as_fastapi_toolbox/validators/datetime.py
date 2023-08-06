from pytz import utc
from datetime import datetime
from pydantic.validators import parse_datetime


class DateTimeUTC(str):
    """
    Turn an incoming datetime into a utc datetime
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=['2020-01-08T00:18:30.602000']
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        dt = parse_datetime(v)
        if cls._is_aware(dt):
            dt = dt.astimezone(utc).replace(tzinfo=None)
        return dt

    def __repr__(self):
        return f'DateTimeUTC({super().__repr__()})'

    # https://stackoverflow.com/a/27596917
    @classmethod
    def _is_aware(cls, dt: datetime) -> bool:
        return (
            dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None
        )
