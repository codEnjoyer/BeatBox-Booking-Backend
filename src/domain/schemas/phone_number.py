from pydantic_extra_types.phone_numbers import PhoneNumber as PNumber


class PhoneNumber(PNumber):
    phone_format = "E164"
    supported_regions = ["RU"]
    default_region_code = "RU"
