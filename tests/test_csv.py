import os.path
import pandas as pd
from unittest import TestCase

import ffmeta
from ffmeta.settings import METADATA_FILE

# This indirect way of getting to the folder is needed so that we can initiate the tests both from within this folder
# as well as from outside it (e.g. for Travis Integration)
CSV_FILE_PATH = os.path.join(os.path.dirname(ffmeta.__file__), METADATA_FILE)


class CsvTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        # Since creating the DataFrame is a semi-expensive operation,
        # we do that as a class method and avoid doing it as part of setUp
        cls.df = pd.read_csv(
            CSV_FILE_PATH,
            encoding="utf-8"
        )

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTypes(self):
        """
        All rows should have a 'type' which matches our predefined list.
        :return:
        """
        types = ["Binary", "Continuous", "Ordered Categorical", "Unordered Categorical", "String", "ID Number"]
        self.assertEqual(len(self.df[self.df.type.notnull()][~self.df.type.isin(types)]), 0)

    def testWave(self):
        """
        All rows should have a 'wave' which matches our predefined list.
        :return:
        """
        waves = ["Baseline", "Year 1", "Year 3", "Year 5", "Year 9", "Year 15"]
        self.assertEqual(len(self.df[self.df.wave.notnull()][~self.df.wave.isin(waves)]), 0)

    def testScope(self):
        """
        All rows should have a 'n_cities_asked' which matches our predefined list.
        :return:
        Come back to this when the metadata file is up to date
        """
        self.assertEqual(len(self.df[self.df.n_cities_asked.notnull()][~self.df.n_cities_asked.isin([2, 15, 16, 18, 20])]), 0)

    def testRespondent(self):
        """
        All rows should have a 'respondent' that comes from one of our instruments
        :return:
        """
        respondents = ['Father', 'Mother', 'Child Care Provider', 'Interviewer', 'Primary Caregiver', 'Child', 'Teacher', 'Couple']
        self.assertEqual(len(self.df[self.df.respondent.notnull()][~self.df.respondent.isin(respondents)]), 0)

    def testSources(self):
        """
        All rows should have a 'source' from our predefined list
        :return:
        """
        sources = ['constructed', 'idnum', 'questionnaire', 'weight']
        self.assertEqual(len(self.df[self.df.source.notnull()][~self.df.source.isin(sources)]), 0)

    def testWarning(self):
        """
        All rows should have a warning code from the set of strings
        :return:
        """
        warnings = ["A survey Yes/No variable that has 'No' coded to 0 instead of 2",
                    "Misordered Categorical (outcomes do not have a contstant scale)",
                    "A unique outcome is coded as a negative value",
                    "Variable has outcomes which override a continuous answer set",
                    "Missing data is coded as something other than the default"]
        self.assertEqual(len(self.df[self.df.warning.notnull()][~self.df.warning.isin(warnings)]), 0)


