from pydantic_extra_types.phone_numbers import PhoneNumber


class RuPhoneNumber(PhoneNumber):
    phone_format = "E164"
    supported_regions = ["RU"]
    default_region_code = "RU"
    max_length = 32
