from us_geo_helper import USGeoHelper
import math
import pandas as pd
import unittest

class GeoTests(unittest.TestCase):
    def assertLatLong(self, ll1, ll2):
        self.assertAlmostEqual(ll1[0], ll2[0], places=2)
        self.assertAlmostEqual(ll1[1], ll2[1], places=2)

class SingleTests(GeoTests):
    def test_zips(self):
        u = USGeoHelper()
        self.assertLatLong(u.zipToCoord(12065), (42.852, -73.786))

        # 10009 in NYC; 1. lots of people 2. land_mi2 < 1
        self.assertGreater(u.zipInfo(10009)[0], 50000)
        self.assertLess(u.zipInfo(10009)[2], 1)

        # not a real zip code
        with self.assertRaises(KeyError):
            u.zipToCoord(90200)

    def test_cities(self):
        u = USGeoHelper()
        self.assertLatLong(u.stateCityToCoord("NY", "New York"), (40.664, -73.939))

        # LA has at least 1 million people
        self.assertGreater(u.stateCityInfo("ca", "los angeles")[0], 1e6)
        # Carmel NY not in df; check online lookup
        self.assertLatLong(u.stateCityToCoord("Ny", "carmel"), (41.430, -73.680))

    def test_inv(self):
        u = USGeoHelper()
        self.assertEqual(u.coordToZip(42.852, -73.786), 12065)
        self.assertEqual(u.coordToStateCity(40.664, -73.939), ("ny", "new york"))

class DataFrameTests(GeoTests):
    def test_zipToStateCity(self):
        u = USGeoHelper()
        og = pd.DataFrame([[85719, 0], [94043, None], [1234, 2], [90200, 3], [None, 4]])
        og.columns = ["zip", "n"]
        df = u.zipToStateCityDf(og, "zip", False)
        df.set_index("zip", inplace=True)

        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.loc[85719, "state"], "az")
        self.assertEqual(df.loc[85719, "city"], "south tucson")
        self.assertEqual(df.loc[94043, "city"], "mountain view")

        # when using online, nothing gets left out except the None
        df = u.zipToStateCityDf(og, "zip", True)
        self.assertEqual(df.shape[0], 4)
        # cutoff too strict; nothing makes it past
        df = u.zipToStateCityDf(og, "zip", True, 0.0001)
        self.assertEqual(df.shape[0], 0)

    def test_cleanZips(self):
        u = USGeoHelper()
        og = pd.DataFrame([[85719, 0], [94043, None], [1234, 2], [90200, 3], [None, 4]])
        og.columns = ["zip", "n"]

        df = u.cleanZips(og, "zip")
        df.set_index("zip", inplace=True)

        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.loc[85719, "n"], 0)
        self.assertTrue(math.isnan(df.loc[94043, "n"]))

        df = u.cleanZips(og, "zip", True)
        # everything but None is kept
        self.assertEqual(df.shape[0], 4)

        df = u.cleanZips(og, "zip", True, 0.0001)
        # even though online, only existing can get through this tight cutoff
        self.assertEqual(df.shape[0], 2)

    def test_stateCityToZip(self):
        u = USGeoHelper()
        og = pd.DataFrame([["la", "armagh", None], ["ma", "boston", 2], ["ca", "los Angeles", 3]])
        og.columns = ["state", "city", "n"]

        df = u.stateCityToZipDf(og, "state", "city", False)
        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.loc[1, "zip"], 2127)
        self.assertEqual(df.loc[2, "zip"], 90034)
        df = u.stateCityToZipDf(og, "state", "city", True)
        self.assertEqual(df.shape[0], 3)
        self.assertEqual(df.loc[0, "zip"], 71354)

if __name__ == "__main__":
    unittest.main()
