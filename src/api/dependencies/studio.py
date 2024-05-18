from src.domain.models.studio import Studio
from src.domain.schemas.studio import StudioRead


def convert_model_to_scheme(studio: Studio) -> StudioRead:
    return StudioRead(
        name=studio.name,
        description=studio.description,
        address=studio.address,
        opening_at=studio.opening_at,
        closing_at=studio.closing_at,
        latitude=studio.latitude,
        longitude=studio.longitude,
        site_url=studio.site_url.url,
        contact_phone_number=str(studio.contact_phone_number),
        tg=studio.tg,
        vk=studio.vk,
        whats_app=studio.whats_app,
    )
