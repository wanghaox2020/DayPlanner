from django.test import TestCase
from unittest.mock import patch
from .yelp_client import YelpRequest, fetch_many, fetch_by_id, search


class YelpClientTestCase(TestCase):
    def test_fetch_by_id(self):
        yelp_response = {
            "id": "WavvLdfdP6g8aZTtbBQHTw",
            "alias": "gary-danko-san-francisco",
            "name": "Gary Danko",
        }

        with patch.object(YelpRequest, "execute", return_value=yelp_response):
            self.assertEqual(fetch_by_id("WavvLdfdP6g8aZTtbBQHTw"), yelp_response)

    def test_fetch_many(self):
        yelp_response = (
            {
                "id": "WavvLdfdP6g8aZTtbBQHTw",
                "alias": "gary-danko-san-francisco",
                "name": "Gary Danko",
            },
        )

        with patch.object(YelpRequest, "execute", return_value=yelp_response):
            self.assertEqual(
                fetch_many(["WavvLdfdP6g8aZTtbBQHTw", "abc123"]),
                [yelp_response, yelp_response],
            )

    def test_search(self):
        yelp_response = (
            {
                "businesses": [
                    {
                        "id": "WavvLdfdP6g8aZTtbBQHTw",
                        "alias": "gary-danko-san-francisco",
                        "name": "Gary Danko",
                    }
                ]
            },
        )

        with patch.object(YelpRequest, "execute", return_value=yelp_response):
            self.assertEqual((search("some_term", "some_location")), yelp_response)
