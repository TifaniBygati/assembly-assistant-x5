from app.response_helpers import group_clients_with_addresses


def test_group_clients_with_addresses_groups_rows_by_client_id():
    payload = [
    {
        "client_id": 1,
        "name": 'Дима',
        "phone": "+79990000001",
        "address_id": 1,
        "street": "Ленина",
        "house": "10",
        "floor": '1',
        "entrance": '1',
        "apartment": "1",
        "comment": "оставить у двери"
    },
    {
        "client_id": 1,
        "name": 'Дима',
        "phone": "+79990000001",
        "address_id": 2,
        "street": "Ленина",
        "house": "10",
        "floor": '1',
        "entrance": '1',
        "apartment": "3",
        "comment": "позвонить за 5 минут"
    },
    {
        "client_id": 2,
        "name": 'Аля',
        "phone": "+79990000002",
        "address_id": 3,
        "street": "Ленина",
        "house": "10",
        "floor": '1',
        "entrance": '1',
        "apartment": "2",
        "comment": "код домофона 1234"
    }
]
    expected = [
        {
            "client_id": 1,
            "name": "Дима",
            "phone": "+79990000001",
            "addresses": [
                {
                    "address_id": 1,
                    "street": "Ленина",
                    "house": "10",
                    "floor": "1",
                    "entrance": "1",
                    "apartment": "1",
                    "comment": "оставить у двери",
                },
                {
                    "address_id": 2,
                    "street": "Ленина",
                    "house": "10",
                    "floor": "1",
                    "entrance": "1",
                    "apartment": "3",
                    "comment": "позвонить за 5 минут",
                },
            ],
        },
        {
            "client_id": 2,
            "name": "Аля",
            "phone": "+79990000002",
            "addresses": [
                {
                    "address_id": 3,
                    "street": "Ленина",
                    "house": "10",
                    "floor": "1",
                    "entrance": "1",
                    "apartment": "2",
                    "comment": "код домофона 1234",
                }
            ],
        },
    ]

    result = group_clients_with_addresses(payload)

    assert result == expected

def test_group_clients_with_addresses_handles_client_without_address():
    payload_left = [
            {
                "client_id": 1,
                "name": "Дима",
                "phone": "+79990000001",
                "address_id": None,
                "street": None,
                "house": None,
                "floor": None,
                "entrance": None,
                "apartment": None,
                "comment": None,
            }
        ]
    expected_left = [
        {
            "client_id": 1,
            "name": "Дима",
            "phone": "+79990000001",
            "addresses": [],
        }
    ]

    result = group_clients_with_addresses(payload_left)

    assert result == expected_left