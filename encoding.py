# modules we'll use
import pandas as pd
import numpy as np

# helpful character encoding module
import charset_normalizer

# set seed for reproducibility
np.random.seed(0)

# start with a string
before = "This is the euro symbol: €"

# check to see what datatype it is
type(before)

# encode it to a different encoding, replacing characters that raise errors
after = before.encode("utf-8", errors="replace")

# check the type
type(after)

# start with a string
before = "This is the euro symbol: €"

# encode it to a different encoding, replacing characters that raise errors
after = before.encode("ascii", errors = "replace")

# convert it back to utf-8
print(after.decode("ascii"))

# We've lost the original underlying byte string! It's been 
# replaced with the underlying byte string for the unknown character :(

# try to read in a file not in UTF-8
kickstarter_2016 = pd.read_csv("../input/kickstarter-projects/ks-projects-201612.csv")


##############################
# pandas problem read csv encoding UTF-8-SIG Error tokenizing data error Buffer overf
df = pd.read_csv('req01.csv',lineterminator='\r')

# TODO: Load in the DataFrame correctly.
with open("../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv", 'rb') as rawdata:
    result = charset_normalizer.detect(rawdata.read(26000))
print(result)
police_killings = pd.read_csv("../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv",encoding='windows-1250')
# {'encoding': 'windows-1250', 'language': 'English', 'confidence': 1.0}

# TODO: Save the police killings dataset to CSV
police_killings.to_csv("my_file.csv")


################################
# Read and store content 
# of an excel file  
read_file = pd.read_excel ("Test.xlsx") 
  
# Write the dataframe object 
# into csv file 
read_file.to_csv ("Test.csv",  
                  index = None, 
                  header=True) 
    
# read csv file and convert  
# into a dataframe object 
df = pd.DataFrame(pd.read_csv("Test.csv"))
