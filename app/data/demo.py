from datetime import time, timezone

from models import Studio, Room
from schemas.room import RoomCreate
from schemas.studio import StudioCreate
from services.room import RoomService
from services.studio import StudioService


async def load_studios() -> list[Studio]:
    studio_service = StudioService()
    studios = [
        StudioCreate(
            name="Soprano",
            description="Школа вокала",
            opening_at=time(hour=5, minute=0, second=0, tzinfo=timezone.utc),
            closing_at=time(hour=16, minute=0, second=0, tzinfo=timezone.utc),
            latitude=56.819691,
            longitude=60.618217,
            site="https://sopranoekat.ru",
            contact_phone_number="+7 (343) 310-00-81",
            tg=None,
            vk="https://vk.com/soprano.ekat",
            whats_app=None,
        ),
        StudioCreate(
            name="Moz-Art",
            description="Творческие лекции, мастер-классы, аренда "
            "пространства для вашего творчества",
            opening_at=time(hour=4, minute=0, second=0, tzinfo=timezone.utc),
            closing_at=time(hour=16, minute=0, second=0, tzinfo=timezone.utc),
            latitude=56.836771,
            longitude=60.609368,
            site="https://moz-art-school.ru",
            contact_phone_number="+7 (966) 669-20-16",
            tg=None,
            vk="https://vk.com/mozartekb",
            whats_app="https://wa.me/79025026723",
        ),
        StudioCreate(
            name="Alter Ego Music",
            description="Наша звукозаписывающая студия ориентирована на "
            "исполнителей любого уровня мастерства, в том числе и "
            "на тех, кому предстоит петь впервые. Поэтому мы "
            "оснастили нашу студию самым современным "
            "оборудованием, программным обеспечением и "
            "высококлассными звукорежиссерами.",
            opening_at=time(hour=5, minute=0, second=0, tzinfo=timezone.utc),
            closing_at=time(hour=17, minute=0, second=0, tzinfo=timezone.utc),
            latitude=56.838164,
            longitude=60.611138,
            site="https://alteregomusic.ru",
            contact_phone_number="+7 (912) 693-19-54",
            tg=None,
            vk="https://vk.com/alter_egomusic",
            whats_app="https://wa.me/79126931954",
        ),
        StudioCreate(
            name="Мьюзик Студио",
            description="Music Studio — профессиональная студия звукозаписи в "
            "Екатеринбурге. У нас вы можете записать песню, "
            "заказать аранжировку или минусовку, записать любой "
            "музыкальный инструмент. Опытная команда в сочетании "
            "с профессиональным оборудованием помогут реализовать "
            "аудио-проекты любой сложности и стилистики.",
            opening_at=time(hour=0, minute=0, second=0, tzinfo=timezone.utc),
            closing_at=time(hour=19, minute=0, second=0, tzinfo=timezone.utc),
            latitude=56.838105,
            longitude=60.623571,
            site="https://musicstudioekb.ru/",
            contact_phone_number="+7 (908) 923-13-94",
            tg=None,
            vk="https://vk.com/muzstudio",
            whats_app="https://wa.me/79089231394",
        ),
    ]
    created_studios = []
    for studio in studios:
        created_studio = await studio_service.create_if_not_exists(studio)
        created_studios.append(created_studio)
    return created_studios


async def load_rooms(studios: list[Studio]) -> list[Room]:
    soprano, mozart, alter_ego, music_studio, *_ = studios
    room_service = RoomService()
    soprano_room = await room_service.create_if_not_exists(
        soprano.id,
        RoomCreate(
            name="Основная",
            description=None,
            equipment="Современное, новое оборудование",
            additional_services="Комфортная обстановка, чай, кофе, печеньки, "
            "конфеты :)",
        ),
    )
    mozart_rooms = [
        await room_service.create_if_not_exists(
            mozart.id,
            RoomCreate(
                name="Кабинет для занятий №1",
                description="Кабинет оснащён всем необходимым для "
                "индивидуальных музыкальных занятий или занятий "
                "до 4х человек. Акустическое фортепиано – "
                "приятный бонус для пианистов. Кабинет удобно "
                "расположен рядом с метро «Площадь 1905 года» в "
                "административном здании. У нас в офисе "
                "разуваются, каждый день проходит влажная уборка, "
                "можно взять с собой чистую сменную обувь, "
                "есть тапочки.",
                equipment="Акустическое фортепиано, электронное фортепиано, "
                "колонка, микрофон, стойка для микрофона, пюпитр ("
                "пульт), 4 стула",
                additional_services="Кулер с водой, тапочки",
            ),
        ),
        await room_service.create_if_not_exists(
            mozart.id,
            RoomCreate(
                name="Кабинет для занятий №2",
                description="Кабинет оснащён всем необходимым для "
                "индивидуальных музыкальных занятий или занятий "
                "до 2х человек. В кабинете стоит акустическое "
                "фортепиано. Кабинет удобно расположен рядом с "
                "метро «Площадь 1905 года» в административном "
                "здании. У нас в офисе разуваются, каждый день "
                "проходит влажная уборка, можно взять с собой "
                "чистую сменную обувь, есть тапочки.",
                equipment="Акустическое фортепиано, 2 стула",
                additional_services="Кулер с водой, тапочки",
            ),
        ),
    ]
    alter_ego_room = await room_service.create_if_not_exists(
        alter_ego.id,
        RoomCreate(
            name="Основная",
            description=None,
            equipment="Вокал, клавишные, гитара, барабаны",
            additional_services=None,
        ),
    )
    music_studio_rooms = [
        await room_service.create_if_not_exists(
            music_studio.id,
            RoomCreate(
                name="Большая комната (деревянная)",
                description="Студия звукозаписи. 3 этаж, студия 325",
                equipment="Гитарный усилитель Mesa Boogie Triple Rectifier "
                "Guitar Amp Head, гитарный кабинет MARSHALL 1960AV, "
                "гитарный кабинет RANDALL RD412-DE, "
                "два ламповых комбо-усилителя Marshall DSL-401, "
                "басовый усилитель ASHDOWN MAG-300H EVO2, "
                "кабинет басовый ASHDOWN MAG-115 deep",
                additional_services=None,
            ),
        ),
        await room_service.create_if_not_exists(
            music_studio.id,
            RoomCreate(
                name="Малая комната (синяя)",
                description="3 этаж, студия 329",
                equipment="Кабинет басовый ASHDOWN MAG-210T, "
                "басовый усилитель Ampeg SVT 4 PRO, "
                "кабинет басовый Ampeg SVT-810E, "
                "усилитель Crown СС-4000",
                additional_services=None,
            ),
        ),
        await room_service.create_if_not_exists(
            music_studio.id,
            RoomCreate(
                name="\"Цветная\" комната",
                description="3 этаж, студия 336",
                equipment="Пассивная акустическая система Yamaha S215V, "
                "вокальные микрофоны AKG D5S, Shure SM58, "
                "Sennheiser E815S, E810S, ElectroVoice N/D 967, "
                "микшерный пульт Soundcraft EPM12, EPM8",
                additional_services=None,
            ),
        ),
        await room_service.create_if_not_exists(
            music_studio.id,
            RoomCreate(
                name="Барабанная комната (детская)",
                description="3 этаж, студия 330",
                equipment="Tama Starclassic birth/bubinga. Сделана из Березы "
                "и Бубинги\n"
                "22″х20″ Вass Drum\n"
                "14″х5.5″ Snare Drum\n"
                "8″х10″ Тоm\n"
                "9″х12″ Тоm\n"
                "14″х16″ Floor Tom\n"
                "16″х18″ Floor Tom\n"
                "\n"
                "RMV Custom Drums (Made in Brazil). "
                "Сделана из Бразильского клёна Bapeva\n"
                "20×18″ Вass Drum\n"
                "14×5.5″ Snare Drum\n"
                "8×10″ Tom\n"
                "9×12″ Tom\n"
                "14×16″ Floor Tom",
                additional_services="Мониторы для барабанщика: "
                "Kempton, AxelVox",
            ),
        ),
        await room_service.create_if_not_exists(
            music_studio.id,
            RoomCreate(
                name="Барабанная комната (барабанная)",
                description="3 этаж, студия 329",
                equipment="Tama Starclassic birth/bubinga. Сделана из Березы "
                "и Бубинги\n"
                "22″х20″ Вass Drum\n"
                "14″х5.5″ Snare Drum\n"
                "8″х10″ Тоm\n"
                "9″х12″ Тоm\n"
                "14″х16″ Floor Tom\n"
                "16″х18″ Floor Tom\n"
                "\n"
                "RMV Custom Drums (Made in Brazil). "
                "Сделана из Бразильского клёна Bapeva\n"
                "20×18″ Вass Drum\n"
                "14×5.5″ Snare Drum\n"
                "8×10″ Tom\n"
                "9×12″ Tom\n"
                "14×16″ Floor Tom",
                additional_services="Мониторы для барабанщика: "
                "Kempton, AxelVox",
            ),
        ),
    ]
    return [soprano_room, *mozart_rooms, alter_ego_room, *music_studio_rooms]


async def load_demo_data() -> None:
    studios = await load_studios()
    _ = await load_rooms(studios)
