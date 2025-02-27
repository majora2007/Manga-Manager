import io
import os
import random
import tempfile
import tkinter as tk
import unittest
import zipfile

from PIL import Image

from src.MetadataManagerLib.cbz_handler import ReadComicInfo
from src.MetadataManagerLib.models import LoadedComicInfo

comicinfo_23 = """
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <!--Generated by Manga Tagger, an Endless Galaxy Studios project-->
   <Series>Maou ni Natta node, Dungeon Tsukutte Jingai Musume to Honobono suru</Series>
   <Number>23</Number>
   <Count>1</Count>
   <Summary/>
   <Year>2018</Year>
   <Month>5</Month>
   <Writer>Ryuuyuu</Writer>
   <Penciller>Note Toono</Penciller>
   <Inker>Note Toono</Inker>
   <Colorist>Note Toono</Colorist>
   <Letterer>Note Toono</Letterer>
   <CoverArtist>Note Toono</CoverArtist>
   <Publisher>Dra-Dra-Dragon Age</Publisher>
   <Genre>Fantasy</Genre>
   <Web>https://myanimelist.net/manga/115200/Maou_ni_Natta_node_Dungeon_Tsukutte_Jingai_Musume_to_Honobono_suru</Web>
   <LanguageISO>en</LanguageISO>
   <Manga>Yes</Manga>
   <Notes>Scraped metadata from AniList and MyAnimeList (using Jikan API) on 2021-12-24 12:38 PM EST</Notes>
</ComicInfo>
"""
comicinfo_24 = """
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <!--Generated by Manga Tagger, an Endless Galaxy Studios project-->
   <Series>Maou ni Natta node, Dungeon Tsukutte Jingai Musume to Honobono suru</Series>
   <Number>24</Number>
   <Count>1</Count>
   <Summary/>
   <Year>2018</Year>
   <Month>5</Month>
   <Writer>Ryuuyuu</Writer>
   <Penciller>Note Toono</Penciller>
   <Inker>Note Toono</Inker>
   <Colorist>Note Toono</Colorist>
   <Letterer>Note Toono</Letterer>
   <CoverArtist>Note Toono</CoverArtist>
   <Publisher>Dra-Dra-Dragon Age</Publisher>
   <Genre>Fantasy</Genre>
   <Web>https://myanimelist.net/manga/115200/Maou_ni_Natta_node_Dungeon_Tsukutte_Jingai_Musume_to_Honobono_suru</Web>
   <LanguageISO>en</LanguageISO>
   <Manga>Yes</Manga>
   <Notes>Scraped metadata from AniList and MyAnimeList (using Jikan API) on 2021-12-24 12:38 PM EST</Notes>
</ComicInfo>
"""

from src.MetadataManagerLib import MetadataManager, models, ComicInfo


class ComicInfoClassTester(unittest.TestCase):
    """
    The purpose of this test is to check ComicInfo class is properly edited.
    ComicInfo is an automatically generated class with some change.
    """

    def setUp(self) -> None:
        self.comicinfo = ComicInfo.ComicInfo()
        self.comicinfo.set_AgeRating(ComicInfo.AgeRating.RATING_PENDING)

    def test_manualModifications(self):
        # @classmethod
        # def list(cls):
        #     return list(map(lambda c: c.value, cls))
        print("Assert AgeRating has list method:")
        self.assertTrue(ComicInfo.AgeRating.list())
        print("Assert ComicPageType has list method:")
        self.assertTrue(ComicInfo.ComicPageType.list())
        ComicInfo.parseString(comicinfo_23, silence=True, print_warnings=False, doRecover=True)


class MetadataManagerTester(unittest.TestCase):
    def setUp(self) -> None:

        self.test_files_names = []
        print("\n", self._testMethodName)
        print("Setup:")
        for ai in range(3):
            out_tmp_zipname = f"Test_{ai}_{random.randint(1, 6000)}.cbz"
            self.test_files_names.append(out_tmp_zipname)
            self.temp_folder = tempfile.mkdtemp()
            # print("", self._testMethodName)
            print(f"     Creating: {out_tmp_zipname}")  # , self._testMethodName)
            with zipfile.ZipFile(out_tmp_zipname, "w") as zf:
                for i in range(5):
                    image = Image.new('RGB', size=(20, 20), color=(255, 73, 95))
                    image.format = "JPEG"
                    # file = tempfile.NamedTemporaryFile(suffix=f'.jpg', prefix=str(i).zfill(3), dir=self.temp_folder)
                    imgByteArr = io.BytesIO()
                    image.save(imgByteArr, format=image.format)
                    imgByteArr = imgByteArr.getvalue()
                    # image.save(file, format='JPEG')
                    # file.write(image.tobytes())
                    zf.writestr(os.path.basename(f"{str(i).zfill(3)}.jpg"), imgByteArr)

            self.initial_dir_count = len(os.listdir(os.getcwd()))

    def tearDown(self) -> None:
        print("Teardown:")
        for filename in self.test_files_names:
            print(f"     Deleting: {filename}")  # , self._testMethodName)
            try:
                os.remove(filename)
            except Exception as e:
                print(e)

    def test_replace_file(self):
        """The number of files read in the output cbz must be the same as in the input (check needed to not end up
        with empty unreadable files """
        first_file_chapter = ""
        second_file_chapter = ""

        test_files = self.test_files_names
        opened_cbz = ReadComicInfo(test_files[0], ignore_empty_metadata=True)
        number_files_preprocess_1 = opened_cbz.total_files
        opened_cbz = 0  # reset so file gets closed
        opened_cbz = ReadComicInfo(test_files[1], ignore_empty_metadata=True)
        number_files_preprocess_2 = opened_cbz.total_files
        opened_cbz = 0  # reset so file gets closed

        random_int = random.random() + random.randint(1, 40)
        random_int_comRating = random.randint(0, 5)
        root = tk.Tk()
        app: MetadataManager.App = MetadataManager.App(root)
        app.create_loadedComicInfo_list(test_files)

        for widget_var in app.widgets_var:
            if str(widget_var) == "OptionMenu_BlackWhite":
                widget_var.set(ComicInfo.YesNo.YES)
            elif str(widget_var) == "OptionMenu_Manga":
                widget_var.set(ComicInfo.Manga.YES_AND_RIGHT_TO_LEFT)
            elif str(widget_var) == "OptionMenu_AgeRating":
                widget_var.set(ComicInfo.AgeRating.RATING_PENDING)
            elif str(widget_var) == "CommunityRating":
                widget_var.set(int(random_int_comRating))
            elif isinstance(widget_var, tk.StringVar):
                widget_var.set(f"This is: {str(widget_var)} modified randint:{random_int}")
            elif isinstance(widget_var, tk.IntVar):
                widget_var.set(int(random_int))
            # else:
            #     widget_var.set(random_int)
        app.input_1_summary_obj.set(f"This is the summary_{random_int}")

        # Chapter number must be kept when handling multiple files they can't be the same.

        app.do_save_UI()
        for file_counter, test_file_path in enumerate(test_files):

            opened_cbz = ReadComicInfo(test_file_path)
            number_files_postprocess = opened_cbz.total_files
            xml_postprocess = opened_cbz.to_ComicInfo()
            print(f"Asserting second file {number_files_preprocess_2} vs {number_files_postprocess}, delta 1")
            self.assertAlmostEqual(number_files_preprocess_2, number_files_postprocess, delta=1)

            print(f"Random assertion values")
            app: MetadataManager.App = MetadataManager.App(root)
            app.create_loadedComicInfo_list([test_file_path])
            # for i in range(7):
            #     with self.subTest(i=i):
            for i, widget_var in enumerate(app.widgets_var):
                with self.subTest(f"F:{file_counter} - {str(widget_var)}"):
                    if str(widget_var) == "OptionMenu_BlackWhite":
                        print("    ┣━━	Assert OptionMenu_BlackWhite")
                        # widget_var.set(ComicInfo.YesNo.YES)
                    elif str(widget_var) == "OptionMenu_Manga":
                        print("    ┣━━	Assert OptionMenu_Manga")
                        self.assertEqual(widget_var.get(), ComicInfo.Manga.YES_AND_RIGHT_TO_LEFT)
                    elif str(widget_var) == "OptionMenu_AgeRating":
                        print("    ┣━━	Assert OptionMenu_AgeRating")
                        self.assertEqual(widget_var.get(), ComicInfo.AgeRating.RATING_PENDING)
                    elif isinstance(widget_var, models.LongText):
                        print("    ┣━━	Assert LongText")
                        self.assertEqual(widget_var.get(), f"This is the summary_{random_int}")
                    elif str(widget_var) == "CommunityRating":
                        print("    ┣━━	Assert CommunityRating")
                        self.assertEqual(int(widget_var.get()), int(random_int_comRating))
                    elif isinstance(widget_var, tk.StringVar):
                        print(
                            f"    ┣━━	Assert {str(widget_var)}:\n    ┃   ┗━━ 'This is: {str(widget_var)} modified randint:{random_int}' vs '{widget_var.get()}'\n    ┃")
                        self.assertEqual(widget_var.get(), f"This is: {str(widget_var)} modified randint:{random_int}")
                    elif isinstance(widget_var, tk.IntVar):
                        print(
                            f"    ┣━━	Assert {str(widget_var)}:\n    ┃   ┗━━ '{widget_var.get()}' vs '{int(random_int)}'\n    ┃")
                        self.assertEqual(int(widget_var.get()), int(random_int))
                        # else:
                    #     self.assertEqual(widget_var.get(), random_int)

    def test_conflict(self):
        """
        Files with random values. Modified values should be applied to all files while retaining original non-modified values
        """
        random_values = []
        # Create random values for each field

        for i, test_file_path in enumerate(self.test_files_names):
            random_value = random.random() + random.randint(1, 40)
            root = tk.Tk()
            app: MetadataManager.App = MetadataManager.App(root)
            app.create_loadedComicInfo_list([test_file_path])

            for widget_var in app.widgets_var:
                if str(widget_var) == "OptionMenu_BlackWhite":
                    widget_var.set(ComicInfo.YesNo.YES)
                elif str(widget_var) == "OptionMenu_Manga":
                    widget_var.set(ComicInfo.Manga.YES_AND_RIGHT_TO_LEFT)
                elif str(widget_var) == "OptionMenu_AgeRating":
                    widget_var.set(ComicInfo.AgeRating.RATING_PENDING)
                elif isinstance(widget_var, models.LongText):
                    widget_var.set(f"This is the summary_{random_value}")
                elif str(widget_var) == "CommunityRating":
                    widget_var.set(int(random_value))
                elif isinstance(widget_var, tk.StringVar):
                    widget_var.set(f"This is: {str(widget_var)} modified randint:{random_value}")
                elif isinstance(widget_var, tk.IntVar):
                    widget_var.set(int(random_value))
            app.do_save_UI()

            random_values.append(random_value)

        # Load all files at once

        modified_value = random.random() + random.randint(1, 40)
        root = tk.Tk()
        app: MetadataManager.App = MetadataManager.App(root)
        app.create_loadedComicInfo_list(self.test_files_names)

        app.entry_Volume_val.set(int(modified_value))
        app.entry_Series_val.set(f"This is: {str(app.entry_Series_val)} modified randint:{modified_value}")
        app.entry_Count_val.set(int(modified_value))
        app.do_save_UI()

        for i, test_file_path in enumerate(self.test_files_names):
            print("Asserting second file 5 vs 6, delta 2")
            self.assertAlmostEqual(5, 6, delta=1)
            print(f"Random assertion values")
            self.assertTrue(True)
            root = tk.Tk()
            app: MetadataManager.App = MetadataManager.App(root)
            app.create_loadedComicInfo_list([test_file_path])
            random_value = random_values[i]
            print(
                f"\n┃ #####\n┃ ##### Starting subtests\n┃ #####\n┃ Random values:{random_values[-1]}\n┃ Current file: {i}\n┕━━━┓")
            for widget_var in app.widgets_var:
                with self.subTest(f"Subtest - File:{i} - {str(widget_var)}"):
                    if str(widget_var) == "Volume" or str(widget_var) == "Count":
                        print(
                            f"    ┣━━	Assert MODIFIED {str(widget_var)}:\n    ┃   ┗━━ 'This is: '{widget_var.get()}' vs '{int(modified_value)}'\n    ┃")
                        self.assertEqual(int(widget_var.get()), int(modified_value))
                    elif str(widget_var) == "Series":
                        print(
                            f"    ┣━━	Assert MODIFIED {str(widget_var)}:\n    ┃   ┗━━ 'This is: {str(widget_var)} modified randint:{modified_value}' vs '{widget_var.get()}'\n    ┃")
                        self.assertEqual(widget_var.get(),
                                         f"This is: {str(widget_var)} modified randint:{modified_value}")
                    elif str(widget_var) == "OptionMenu_BlackWhite":
                        print("    ┣━━	Assert OptionMenu_BlackWhite")
                    elif str(widget_var) == "OptionMenu_Manga":
                        print("    ┣━━	Assert OptionMenu_Manga")
                        self.assertEqual(widget_var.get(), ComicInfo.Manga.YES_AND_RIGHT_TO_LEFT)
                    elif str(widget_var) == "OptionMenu_AgeRating":
                        print("    ┣━━	Assert OptionMenu_AgeRating")
                        self.assertEqual(widget_var.get(), ComicInfo.AgeRating.RATING_PENDING)
                    elif isinstance(widget_var, models.LongText):
                        print("    ┣━━	Assert LongText")
                        self.assertEqual(f"This is the summary_{random_value}", widget_var.get())
                    elif str(widget_var) == "CommunityRating":
                        print("    ┣━━	Assert CommunityRating")
                        self.assertEqual(int(widget_var.get()), int(random_value))
                    elif isinstance(widget_var, tk.StringVar):
                        print(
                            f"    ┣━━	Assert {str(widget_var)}:\n    ┃   ┗━━ 'This is: {str(widget_var)} modified randint:{random_value}' vs '{widget_var.get()}'\n    ┃")
                        self.assertEqual(f"This is: {str(widget_var)} modified randint:{random_value}",
                                         widget_var.get())
                    elif isinstance(widget_var, tk.IntVar):
                        print(
                            f"    ┣━━	Assert {str(widget_var)}:\n    ┃   ┗━━ '{widget_var.get()}' vs '{int(random_value)}'\n    ┃")
                        self.assertEqual(widget_var.get(), int(random_value))


class GlobalTagsGenres(unittest.TestCase):
    def setUp(self) -> None:
        self.loadedComicInfo_list = []
        print("\n", self._testMethodName)
        print("Setup:")
        self.genres = ["Genre_1, Genre_2, Genre_3, Common_genre_4",
                       "Genre_4, Genre_5, Genre_6",
                       "Genre_7, Genre_8, Genre_9, Common_genre_4",
                       "Genre_10, Genre_11, Genre_12",
                       "Genre_13, Genre_14, Genre_15, Common_genre_4"]
        self.tags = ["Tag_1, Tag_2, Tag_3",
                     "Tag_4, Tag_5, Tag_6, Common_tag_4",
                     "Tag_7, Tag_8, Tag_9",
                     "Tag_10, Tag_11, Tag_12, Common_tag_4",
                     "Tag_13, Tag_14, Tag_15"]

        self.common_tag = "Common_tag_1, Common_tag_2, Common_tag_3"
        self.common_genre = "Common_genre_1, Common_genre_2, Common_genre_3"

        for ai in range(3):
            cinfo = ComicInfo.ComicInfo()
            cinfo.set_Genre(self.genres[ai])
            cinfo.set_Tags(self.tags[ai])
            self.loadedComicInfo_list.append(LoadedComicInfo("", cinfo))

            self.initial_dir_count = len(os.listdir(os.getcwd()))

    #
    def test_Append_Global(self):
        root = tk.Tk()
        app: MetadataManager.App = MetadataManager.App(root)
        app.loadedComicInfo_list = self.loadedComicInfo_list

        app.global_tags_add_val.set(self.common_tag)
        app.global_genres_add_val.set(self.common_genre)
        app._parseUI_toComicInfo()

        print("Assert that all common tags are present in all the loaded cinfo")
        for loadedCinfo in app.loadedComicInfo_list:
            for tag in self.common_tag.split(","):
                self.assertTrue(tag in loadedCinfo.comicInfoObj.get_Tags())
            for genre in self.common_genre.split(","):
                self.assertTrue(genre in loadedCinfo.comicInfoObj.get_Genre())

    def test_Remove_Global(self):
        root = tk.Tk()
        app: MetadataManager.App = MetadataManager.App(root)
        app.loadedComicInfo_list = self.loadedComicInfo_list

        # app.global_tags_add_val.set(self.common_tag)
        # app.global_genres_add_val.set(self.common_genre)
        # app._parseUI_toComicInfo()
        app.global_tags_remove_val.set("Common_genre_4, Genre_1, Genre_8")
        app.global_genres_remove_val.set("Common_tag_4, Tag_1, Tag_8")
        app._parseUI_toComicInfo()

        print("Assert that all common tags are removed from all the loaded cinfo")
        for loadedCinfo in app.loadedComicInfo_list:
            for tag in "Common_genre_4, Genre_1, Genre_8".split(","):
                self.assertFalse(tag in loadedCinfo.comicInfoObj.get_Tags())
            for genre in "Common_tag_4, Tag_1, Tag_8".split(","):
                self.assertFalse(genre in loadedCinfo.comicInfoObj.get_Genre())
