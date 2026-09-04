import unittest
from datetime import datetime

from FB2.Image import Image
from FB2.TitleInfo import TitleInfo
from FB2.builders.TitleInfoBuilder import TitleInfoBuilder


class TitleInfoBuilderTest(unittest.TestCase):
    def test_add_date_uses_supported_subelement_call(self):
        title_info = TitleInfo(date=(datetime(2010, 1, 2), "2010"))

        result = TitleInfoBuilder(titleInfo=title_info).GetResult()

        date = result.find("date")
        self.assertIsNotNone(date)
        self.assertEqual(date.get("value"), "2010-01-02")
        self.assertEqual(date.text, "2010")

    def test_coverpage_precedes_language_as_required_by_fb2_schema(self):
        title_info = TitleInfo(
            coverPageImages=[Image(media_type="image/jpeg", content=b"image")],
            lang="ru",
        )

        result = TitleInfoBuilder(titleInfo=title_info).GetResult()
        tags = [child.tag for child in result]

        self.assertLess(tags.index("coverpage"), tags.index("lang"))


if __name__ == "__main__":
    unittest.main()
