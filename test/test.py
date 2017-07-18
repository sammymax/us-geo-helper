from us-geo-helper import USGeoHelper
import pandas as pd

u = USGeoHelper()
df = pd.DataFrame([[12065, 94043, 1234, 90200, None], [0, None, 2, 3, 4]])
df = df.transpose()
df.columns = ["zip", "n"]
print(df)
print(u.zipToStateCityDf(df, "zip", False))
print(u.zipToStateCityDf(df, "zip", False, 3.5))
print(u.zipToStateCityDf(df, "zip", True))

print("\n\n\n")
print(u.cleanZips(df, "zip"))
print(u.cleanZips(df, "zip", True))
print(u.cleanZips(df, "zip", True, 5))

df2 = pd.DataFrame([["ny", "clifton park", None], ["ma", "boston", 2], ["ca", "los Angeles", 3]])
df2.columns = ["state", "city", "n"]
print("\n\n\n")
print(df2)
print(u.stateCityToZipDf(df2, "state", "city", False))
print(u.stateCityToZipDf(df2, "state", "city", True))
