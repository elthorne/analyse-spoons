import json
from unittest import mock

import pytest

from services.process_and_store_input import process_cards, extract_integers, convert_name_to_date, save_dict_to_json


def test_process_cards_returns_expected_result():
    # arrange
    mock_data = {
        "cards": [
            {
                "benedict": "cumberbatch",
                "labels": [],
                "name": "---SUN 30TH APRIL--- (5)",
            },
            {
                "benedettini": "cabinetry",
                "labels": [],
                "name": " front room (5)",
            },
            {
                "billybob": "crackerjack",
                "labels": [
                    {
                        "banana": "clipperton",
                        "color": "purple",
                    }
                ],
                "name": "kitchen (3)",
            },
            {
                "bonkyhurt": "cutiebrunch",
                "labels": [],
                "name": "---SAT 29TH APRIL--- (10)",
            },
            {
                "bubblenut": "cutiepie",
                "labels": [
                    {
                        "benefit": "cosmetics",
                        "color": "orange",
                    }
                ],
                "name": "living room (7)",
            },
            {
                "brendadirk": "cramplescrunch",
                "labels": [],
                "name": "living room (7)",
            },
        ],
    }
    mock_json_input = json.dumps(mock_data)
    mock_filename = "butternut/crinklefries"

    # act
    with mock.patch("builtins.open", mock.mock_open(read_data=mock_json_input)):
        result = process_cards(mock_filename)

    # assert
    assert type(result) == dict
    assert len(result) == 2
    assert result == {
        '2023-04-29': [
            {
                'colors': ['orange'],
                'name': 'living room (7)'
            },
            {
                'name': 'living room (7)'
            },
            {
                'Total': 14
            }
        ],
        '2023-04-30': [
            {
                'name': ' front room (5)'
            },
            {
                'colors': ['purple'],
                'name': 'kitchen (3)'
            },
            {
                'Total': 8
            }
        ]
    }


@pytest.mark.parametrize("test_input, expected_output",
                         [
                             ("(1)", 1),
                             ("(5)", 5),
                             ("(20)", 20),
                             ("(1", 0),
                             ("2)", 0),
                             ("13", 0),
                             ("foo", 0),

                         ])
def test_extract_integers_returns_expected_result(test_input, expected_output):
    # act
    result = extract_integers(test_input)

    # assert
    assert result == expected_output


@pytest.mark.parametrize("test_input, expected_output",
                         [
                             ('---SAT 29TH APRIL--- (10)', '2023-04-29'),
                             ('---SUN 30TH APRIL--- (5)', '2023-04-30'),
                         ])
def test_convert_name_to_date_returns_expected_result(test_input, expected_output):
    # arrange and act
    result = convert_name_to_date(test_input)

    # assert
    assert result == expected_output


def test_save_dict_to_json_raises_an_exception():
    # arrange
    mock_file = mock.mock_open()
    mock_file.side_effect = Exception("Bundleup Catchyourdeath is incorrect")

    mock_data = {"foo": "bar"}
    mock_filename = "YYYY-MM-encrypted_data.json"

    # act and assert
    with pytest.raises(Exception):
        with mock.patch("builtins.open", mock_file):
            save_dict_to_json(mock_data, mock_filename)
