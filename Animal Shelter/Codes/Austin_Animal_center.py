import pandas as pd
import numpy as np
import pandas_profiling
from datetime import datetime



###======== Intake database ===========

df_in = pd.read_csv('Austin_Animal_Center_Intakes.csv')

# virtual profile - Initial
#prof_in = pandas_profiling.ProfileReport(df_in)
#prof_in.to_file('pandas_profile_IN_initial.html')


### cleaning

df_in.columns = df_in.columns.str.strip()


# animal id ===== what to do with this?
#id_issue = df_in.loc[df_in['Animal ID'].str.contains("A721033", case=False)]
# check non-unique ID
#df_duplicated_in_id = df_in[df_in.duplicated(subset=['Animal ID'], keep=False)]
#df_duplicated_in_all = df_in[df_in.duplicated()]


# cleaning name
df_in['Name'] = df_in['Name'].str.lower().fillna('Unknown')

# cleaning datetime
df_in['DateTime'] = pd.to_datetime(df_in['DateTime'], format='%m/%d/%Y %H:%M:%S %p')
df_in = df_in.drop('MonthYear',1)

# location
#df_in = df_in.drop('Found Location',1)


# cleaning sex upon intake
df_in['Sex upon Intake'] = df_in['Sex upon Intake'].fillna('Unknown')

# Age upon intake

df_in['Age upon Intake'] = df_in['Age upon Intake'].astype(str)

df_in['Age_upon_Intake'] = df_in['Age upon Intake'].str.strip().str.extract(r'(\d+)')
df_in['Age_upon_Intake'] = df_in['Age_upon_Intake'].astype(float)


for i in range(len(df_in['Age_upon_Intake'])):
    if 'weeks' in df_in['Age upon Intake'][i]:
        pd.options.mode.chained_assignment = None
        df_in['Age_upon_Intake'][i] = df_in['Age_upon_Intake'][i]*0.019165
    elif 'months' in df_in['Age upon Intake'][i]:
        pd.options.mode.chained_assignment = None
        df_in['Age_upon_Intake'][i] = df_in['Age_upon_Intake'][i]/12
    elif 'week' in df_in['Age upon Intake'][i]:
        pd.options.mode.chained_assignment = None
        df_in['Age_upon_Intake'][i] = df_in['Age_upon_Intake'][i]*0.019165
    elif 'month' in df_in['Age upon Intake'][i]:
        pd.options.mode.chained_assignment = None
        df_in['Age_upon_Intake'][i] = df_in['Age_upon_Intake'][i]/12
    else:
        pass

df_in = df_in.drop('Age upon Intake',1)


## triming breed
df_in['Mix'] = df_in['Breed'].str.strip().str.extract(r'(Mix|mix)')
df_in['Mix'] = df_in['Mix'].str.replace(r'(Mix|mix)',"Yes")
df_in['Mix'] = df_in['Mix'].fillna('No')

df_in['Breed'] = df_in['Breed'].str.replace(r'(Mix|mix)',"")

df_in = df_in.join(
    df_in['Breed'].str.split('/',expand = True).rename(columns={0:'Breed_1',1:'Breed_2',2:'extra'}))
df_in = df_in.drop('extra',1)
df_in = df_in.drop('Breed',1)

df_in['Breed_2'] = df_in['Breed_2'].fillna('No secondary breed')

# Triming Color
df_in = df_in.join(
    df_in['Color'].str.split('/',expand = True).rename(columns={0:'Color_1',1:'Color_2'}))
df_in = df_in.drop('Color',1)

df_in['Color_2'] = df_in['Color_2'].fillna('No secondary color')


# final cleanings

df_in = df_in.drop_duplicates()
df_in = df_in.drop_duplicates(subset=['Animal ID'])


# virtual profile - Final
#prof_in = pandas_profiling.ProfileReport(df_in)
#prof_in.to_file('pandas_profile_IN_Final.html')


#====================================
##===============================df_out
#=====================================
import pandas as pd
import numpy as np
import pandas_profiling
from datetime import datetime


df_out = pd.read_csv('Austin_Animal_Center_Outcomes.csv')
#prof_out = pandas_profiling.ProfileReport(df_out)
#prof_out.to_file('pandas_profile_OUT_initial.html')

### cleaning

# cleaning name
df_out['Name'] = df_out['Name'].str.lower().fillna('Unknown')

# cleaning datetime
df_out['DateTime'] = pd.to_datetime(df_out['DateTime'], format='%m/%d/%Y %H:%M:%S %p')
df_out = df_out.drop('MonthYear',1)

# change format 'date of birth'
df_out['Date of Birth'] = pd.to_datetime(df_out['Date of Birth'], format='%m/%d/%Y')

# cleaning 'outcome type'
df_out['Outcome Type'] = df_out['Outcome Type'].fillna('Unknown')

# cleaning 'outcome SUBtype'
df_out['Outcome Subtype'] = df_out['Outcome Subtype'].fillna('Unknown')

# missing values (sex upon outcome)
df_out['Sex upon Outcome'] = df_out['Sex upon Outcome'].fillna('Unknown')



# Age upon intake

#df_out['Age upon Outcome'] = df_out['Age upon Outcome'].fillna('Unknown')

df_out['Age upon Outcome'] = df_out['Age upon Outcome'].astype(str)

df_out['Age_upon_Outcome'] = df_out['Age upon Outcome'].str.strip().str.extract(r'(\d+)')
df_out['Age_upon_Outcome'] = df_out['Age_upon_Outcome'].fillna('0')
df_out['Age_upon_Outcome'] = df_out['Age_upon_Outcome'].astype(float)


for i in range(len(df_out['Age upon Outcome'])):
    if 'weeks' in df_out['Age upon Outcome'][i]:
        pd.options.mode.chained_assignment = None
        df_out['Age_upon_Outcome'][i] = df_out['Age_upon_Outcome'][i]*0.019165
    elif 'months' in df_out['Age upon Outcome'][i]:
        pd.options.mode.chained_assignment = None
        df_out['Age_upon_Outcome'][i] = df_out['Age_upon_Outcome'][i]/12
    elif 'week' in df_out['Age upon Outcome'][i]:
        pd.options.mode.chained_assignment = None
        df_out['Age_upon_Outcome'][i] = df_out['Age_upon_Outcome'][i]*0.019165
    elif 'month' in df_out['Age upon Outcome'][i]:
        pd.options.mode.chained_assignment = None
        df_out['Age_upon_Outcome'][i] = df_out['Age_upon_Outcome'][i]/12
    else:
        pass

df_out = df_out.drop('Age upon Outcome',1)


## triming breed
df_out['Mix'] = df_out['Breed'].str.strip().str.extract(r'(Mix|mix)')
df_out['Mix'] = df_out['Mix'].str.replace(r'(Mix|mix)',"Yes")
df_out['Mix'] = df_out['Mix'].fillna('No')

df_out['Breed'] = df_out['Breed'].str.replace(r'(Mix|mix)',"")

df_out = df_out.join(
    df_out['Breed'].str.split('/',expand = True).rename(columns={0:'Breed_1',1:'Breed_2',2:'extra'}))
df_out = df_out.drop('extra',1)
df_out = df_out.drop('Breed',1)

df_out['Breed_2'] = df_out['Breed_2'].fillna('No secundary breed')

# Triming Color
df_out = df_out.join(
    df_out['Color'].str.split('/',expand = True).rename(columns={0:'Color_1',1:'Color_2'}))
df_out = df_out.drop('Color',1)

df_out['Color_2'] = df_out['Color_2'].fillna('No secondary color')


# final cleanings

df_out = df_out.drop_duplicates()
df_out = df_out.drop_duplicates(subset=['Animal ID'])


# virtual profile - Final
#prof_in = pandas_profiling.ProfileReport(df_out)
#prof_in.to_file('pandas_profile_OUT_Final.html')


# check 'domestic shorthair' & 'domestic shorthair MIX'
#breed_check_IN = df_in.loc[df_in['Breed_1'].str.contains("Domestic Shorthair", case=False)]
#breed_check_OUT = df_out.loc[df_out['Breed_1'].str.contains("Domestic Shorthair", case=False)]


#==========================================
# total

df_total = pd.merge(df_in,df_out, how='inner',left_on='Animal ID', right_on='Animal ID') #.drop('Animal ID', axis=1)


# check if columns are the same
#df_total['Name_x'].equals(df_total['Name_y'])
#df_total['Animal Type_x'].equals(df_total['Animal Type_y'])
#df_total['Mix_x'].equals(df_total['Mix_y'])
#df_total['Breed_1_x'].equals(df_total['Breed_1_y'])
#df_total['Breed_2_x'].equals(df_total['Breed_2_y'])
#df_total['Color_1_x'].equals(df_total['Color_1_y'])
#df_total['Color_2_x'].equals(df_total['Color_2_y'])


# new columns

df_total['Location'] = 'Texas'


df_total['Sex'] = "unknown"
for i in range(len(df_total['Sex upon Intake'])):
    if 'Male' in df_total['Sex upon Intake'][i]:
        pd.options.mode.chained_assignment = None
        df_total['Sex'][i] = 'male'
    elif 'Female' in df_total['Sex upon Intake'][i]:
        pd.options.mode.chained_assignment = None
        df_total['Sex'][i] = 'female'
    else:
        pass

# neuter/spay

df_total['neuter/spay'] = "unknown"

for i in range(len(df_total['Sex upon Outcome'])):
    if 'Neutered' in df_total['Sex upon Outcome'][i]:
        pd.options.mode.chained_assignment = None
        df_total['neuter/spay'][i] = 'yes'
    elif 'Spayed' in df_total['Sex upon Outcome'][i]:
        pd.options.mode.chained_assignment = None
        df_total['neuter/spay'][i] = 'yes'
    elif 'Intact' in df_total['Sex upon Outcome'][i]:
        pd.options.mode.chained_assignment = None
        df_total['neuter/spay'][i] = 'no'
    else:
        pass

df_total = df_total.drop(['Sex upon Intake','Sex upon Outcome'], axis=1)

# adopted/non-adopted

df_total['Outcome Type'] = df_total['Outcome Type'].str.lower()

df_total['adopted/non-adopted'] = 'unknown'

adopted = ['adoption','return to owner','rto-adopt']
non_adopted = ['transfer','died','euthanasia','missing','disposal','unknown']

for i in range(len(df_total['Outcome Type'])):
    if df_total['Outcome Type'][i] in adopted:
        df_total['adopted/non-adopted'][i] = 'adopted'
    elif df_total['Outcome Type'][i] in non_adopted:
        df_total['adopted/non-adopted'][i] = 'non-adopted'



# days in shelter
df_total['Days in Shelter'] = (df_total['DateTime_y'] - df_total['DateTime_x'])/ np.timedelta64(1,'D')
df_total['Days in Shelter'] = df_total['Days in Shelter'].astype(int)

# data validation
for i in range(len(df_total['DateTime_y'])):
    if ((df_total['DateTime_y'][i] - df_total['DateTime_x'][i])/ np.timedelta64(1,'D')) < 0:
        df_total['Days in Shelter'][i] = ( df_total['DateTime_x'][i] - df_total['DateTime_y'][i]) / np.timedelta64(1,'D')
    else:
        pass

# Remove equals columns
df_total = df_total.drop(['Name_y','Animal Type_y','Mix_y','Breed_1_y','Breed_2_y','Color_1_y','Color_2_y'],axis=1)

# Rename columns

dict = {'Name_x':'Name',
        'DateTime_x':'DateTime_Intake',
        'Animal Type_x':'Animal_Type',
        'Mix_x':'Mix_Breed',
        'Breed_1_x':'Primary_Breed',
        'Breed_2_x':'Secondary_Breed',
        'Color_1_x':'Main_Color',
        'Color_2_x':'Secondary_Color',
        'DateTime_y':'DateTime_Outcome',
        'Intake Type':'Intake_type',
        'Intake Condition':'Intake_Condition',
        'Outcome Type':'Outcome_Type',
        'Days in Shelter':'Days_in_shelter',
        'Animal ID':'Animal_ID',
        'Found Location':'Found_Location',
        'Outcome Subtype':'Outcome_Subtype'
        }

df_total = df_total.rename(columns= dict,
                           inplace = False)

cols = ['Intake_type','Intake_Condition','Mix_Breed','Primary_Breed','Secondary_Breed','Main_Color','Secondary_Color','Sex','neuter/spay']
df_total[cols] = df_total[cols].astype('category')

col2 = ['DateTime_Intake','DateTime_Outcome','Date of Birth']
df_total[col2] = df_total[col2].astype('datetime64[ns]')

# general clean
df_total = pd.concat([df_total[col].astype(str).str.lower() for col in df_total.columns], axis=1)


# extra cleaning breeds

df_total['Primary_Breed'] = df_total['Primary_Breed'].str.lstrip()
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.rstrip()

df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' shorthair',"")
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' longhair',"")
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' wirehair',"")
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' rough',"")
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' smooth Coat',"")
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' smooth',"")
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' flat Coat',"")
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r' coat',"")


df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'german shepherd','german shepherd dog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'doberman pinsch','doberman pinscher')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'staffordshire','staffordshire bull terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'black mouth cur','mountain cur')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'jack russell terrier','russell terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'rhod ridgeback','rhodesian ridgeback')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'queensland heeler','lancashire heeler')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'american staffordshire bull terrier terrier','american staffordshire terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'bruss griffon','brussels griffon')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'catahoula','catahoula leopard dog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'presa canario','perro de presa canario')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'chesa bay retr','chesapeake bay retriever')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'toy poodle','poodle (toy)')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'miniature poodle','poodle (miniature)')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'standard poodle','poodle (standard)')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'redbone hound','redbone coonhound')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'anatol shepherd','anatolian shepherd dog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'schnauzer giant','giant schnauzer')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'flat retriever','flat-coated retriever')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'english bulldog','bulldog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'chinese sharpei','chinese shar-pei')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'american eskimo','american eskimo dog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'west highland','west highland white terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'softed wheaten terrier','soft coated wheaten terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'english pointer','pointer')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'st. bernard','saint bernard')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'grand basset griffon vendeen','grand basset griffon vendéen')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'sealyham terr','sealyham terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'swiss hound','greater swiss mountain dog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'dachshund stan','dachshund')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'lowchen','löwchen')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'podengo pequeno','portuguese podengo pequeno')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'bouv flandres','bouvier des flandres')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'entlebucher','entlebucher mountain dog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'bedlington terr','bedlington terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'eng toy spaniel','english toy spaniel')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'old bulldog','bulldog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'sussex span','sussex spaniel')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'treeing cur','treeing walker coonhound')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'boykin span','boykin spaniel')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'picardy sheepdog','berger picard')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'port water dog','portuguese water dog')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'glen of imaal','glen of imaal terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'english coonhound','american english coonhound')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'bluetick hound','bluetick coonhound')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'pbgv','petit basset griffon vendéen')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'cavalier span','cavalier king charles spaniel')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'bull terrier miniature', 'miniature bull terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'treeing tennesse brindle', 'treeing tennessee brindle')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'dandie dinmont', 'dandie dinmont terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'dutch sheepdog', 'dutch shepherd')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'germaned pointer','german pointer')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'manchester terrier (standard)','manchester terrier')
df_total['Primary_Breed'] = df_total['Primary_Breed'].str.replace(r'mexican hairless','xoloitzcuintli')




######################################################################### American Kennel Asiociation (All Breeds)

from bs4 import BeautifulSoup
import requests
import re

list_urls = ['https://www.akc.org/dog-breeds/']

kennel_breeds = []

def get_page_links(url):
    baseurl = 'https://www.akc.org/dog-breeds/'
    r = requests.get(url)
    sp = BeautifulSoup(r.text,)
    links = sp.select('h3.breed-type-card__title.mt0.mb0.f-25.py3.px3')
    for link in links:
        breed = link.get_text()
        kennel_breeds.append(breed)


for url in list_urls:
    for j in re.finditer('breeds[/]', url):
        print(j.start(), j.end())
        x = j.end()
        y = range(1,24)
        for z in y:
            next_page = url[:x] + 'page' + '/' + str(z) + '/' + url[x:]
            print(next_page)
            get_page_links(next_page)

for i in range(len(kennel_breeds)):
    kennel_breeds[i] = kennel_breeds[i].lower()


# focus in dogs

#df_total.drop(df_total[df_total['Animal_Type'] != 'dog'].index, inplace=True)

######################################################################################## American Kennel Asiociation (breeds by size)

from bs4 import BeautifulSoup
import requests
import re

list_urls = ['https://www.akc.org/dog-breeds/?size%5B%5D=xsmall',
             'https://www.akc.org/dog-breeds/?size%5B%5D=small',
             'https://www.akc.org/dog-breeds/?size%5B%5D=medium',
             'https://www.akc.org/dog-breeds/?size%5B%5D=large',
             'https://www.akc.org/dog-breeds/?size%5B%5D=xlarge']

xsmall = []
small = []
medium = []
large = []
xlarge = []


def get_page_links(url):
    baseurl = 'https://www.akc.org/dog-breeds/'
    r = requests.get(url)
    sp = BeautifulSoup(r.text,)
    links = sp.select('h3.breed-type-card__title.mt0.mb0.f-25.py3.px3')
    for link in links:
        breed = link.get_text()
        if 'xsmall' in url:
            xsmall.append(breed)
        elif 'small' in url:
            if 'xsmall' not in url:
                small.append(breed)
        elif 'medium' in url:
            medium.append(breed)
        elif 'large' in url:
            if 'xlarge' not in url:
                large.append(breed)
        elif 'xlarge' in url:
            xlarge.append(breed)


for url in list_urls:
    for j in re.finditer('breeds[/]', url):
        print(j.start(), j.end())
        x = j.end()
        y = range(1,12)
        for z in y:
            next_page = url[:x] + 'page' + '/' + str(z) + '/' + url[x:]
            print(next_page)
            get_page_links(next_page)

for i in range(len(xsmall)):
    xsmall[i] = xsmall[i].lower()
for i in range(len(small)):
    small[i] = small[i].lower()
for i in range(len(medium)):
    medium[i] = medium[i].lower()
for i in range(len(large)):
    large[i] = large[i].lower()
for i in range(len(xlarge)):
    xlarge[i] = xlarge[i].lower()


############################################## New variable (Breed size)

df_total['Breed_size'] = 'Unknown'

for i in range(len(df_total['Primary_Breed'])):
    for j in xsmall:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_size'].iloc[i] = 'xsmall'
    for j in small:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_size'].iloc[i] = 'small'
    for j in medium:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_size'].iloc[i] = 'medium'
    for j in large:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_size'].iloc[i] = 'large'
    for j in xlarge:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_size'].iloc[i] = 'xlarge'


##################################################### American Kennel club (trainability)


from bs4 import BeautifulSoup
import requests
import re

list_urls = ['https://www.akc.org/dog-breeds/?trainability%5B%5D=easy-training',
             'https://www.akc.org/dog-breeds/?trainability%5B%5D=eager-to-please',
             'https://www.akc.org/dog-breeds/?trainability%5B%5D=may-be-stubborn',
             'https://www.akc.org/dog-breeds/?trainability%5B%5D=agreeable',
             'https://www.akc.org/dog-breeds/?trainability%5B%5D=independent']

# order and rank (1 -> 5)

easy = []   #1
pleaser = []    #2
stubborn = []   #5
agreeable = []  #3
independent = []    #4


def get_page_links(url):
    baseurl = 'https://www.akc.org/dog-breeds/'
    r = requests.get(url)
    sp = BeautifulSoup(r.text,)
    links = sp.select('h3.breed-type-card__title.mt0.mb0.f-25.py3.px3')
    for link in links:
        breed = link.get_text()
        if 'easy' in url:
            easy.append(breed)
        elif 'please' in url:
            pleaser.append(breed)
        elif 'stubborn' in url:
            stubborn.append(breed)
        elif 'agreeable' in url:
            agreeable.append(breed)
        elif 'independent' in url:
            independent.append(breed)


for url in list_urls:
    for j in re.finditer('breeds[/]', url):
        print(j.start(), j.end())
        x = j.end()
        y = range(1,8)
        for z in y:
            next_page = url[:x] + 'page' + '/' + str(z) + '/' + url[x:]
            print(next_page)
            get_page_links(next_page)

for i in range(len(easy)):
    easy[i] = easy[i].lower()
for i in range(len(pleaser)):
    pleaser[i] = pleaser[i].lower()
for i in range(len(stubborn)):
    stubborn[i] = stubborn[i].lower()
for i in range(len(agreeable)):
    agreeable[i] = agreeable[i].lower()
for i in range(len(independent)):
    independent[i] = independent[i].lower()


#################### new variable (Trainability)

df_total['Trainability'] = 'Unknown'


for i in range(len(df_total['Primary_Breed'])):
    for j in easy:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Trainability'].iloc[i] = 'easy'
    for j in pleaser:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Trainability'].iloc[i] = 'pleaser'
    for j in stubborn:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Trainability'].iloc[i] = 'stubborn'
    for j in agreeable:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Trainability'].iloc[i] = 'agreeable'
    for j in independent:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Trainability'].iloc[i] = 'independent'

##################################################### American Kennel club (main characterictic of breeds)


from bs4 import BeautifulSoup
import requests
import re

list_urls = ['https://www.akc.org/dog-breeds/?characteristic%5B%5D=best-guard-dogs',
             'https://www.akc.org/dog-breeds/?characteristic%5B%5D=best-dogs-for-kids',
             'https://www.akc.org/dog-breeds/?characteristic%5B%5D=best-family-dogs',
             'https://www.akc.org/dog-breeds/?characteristic%5B%5D=smartest-dogs',
             'https://www.akc.org/dog-breeds/?characteristic%5B%5D=hypoallergenic-dogs',
             'https://www.akc.org/dog-breeds/?characteristic%5B%5D=best-dogs-for-apartments-dwellers']


kid_friendly = []    #3
family_dog = []   #4
smartests_dog = []  #3
hypoallergenic_dog = []    #
guard_dog = []
apartment_friendly = []


def get_page_links(url):
    baseurl = 'https://www.akc.org/dog-breeds/'
    r = requests.get(url)
    sp = BeautifulSoup(r.text,)
    links = sp.select('h3.breed-type-card__title.mt0.mb0.f-25.py3.px3')
    for link in links:
        breed = link.get_text()
        if 'guard' in url:
            guard_dog.append(breed)
        elif 'hypoallergenic' in url:
            hypoallergenic_dog.append(breed)
        elif 'family' in url:
            family_dog.append(breed)
        elif 'smartest' in url:
            smartests_dog.append(breed)
        elif 'apartments' in url:
            apartment_friendly.append(breed)
        elif 'kids' in url:
            kid_friendly.append(breed)

for url in list_urls:
    for j in re.finditer('breeds[/]', url):
        print(j.start(), j.end())
        x = j.end()
        y = range(1,8)
        for z in y:
            next_page = url[:x] + 'page' + '/' + str(z) + '/' + url[x:]
            print(next_page)
            get_page_links(next_page)


for i in range(len(kid_friendly)):
    kid_friendly[i] = kid_friendly[i].lower()
for i in range(len(family_dog)):
    family_dog[i] = family_dog[i].lower()
for i in range(len(smartests_dog)):
    smartests_dog[i] = smartests_dog[i].lower()
for i in range(len(hypoallergenic_dog)):
    hypoallergenic_dog[i] = hypoallergenic_dog[i].lower()
for i in range(len(guard_dog)):
    guard_dog[i] = guard_dog[i].lower()
for i in range(len(apartment_friendly)):
    apartment_friendly[i] = apartment_friendly[i].lower()



#################### new variable (Breed_characteristic)

df_total['Breed_characteristic'] = 'Not_define'

for i in range(len(df_total['Primary_Breed'])):
    for j in apartment_friendly:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_characteristic'].iloc[i] = 'apartment_friendly'
    for j in kid_friendly:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_characteristic'].iloc[i] = 'kid_friendly'
    for j in family_dog:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_characteristic'].iloc[i] = 'family_dog'
    for j in smartests_dog:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_characteristic'].iloc[i] = 'smartest_dog'
    for j in hypoallergenic_dog:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_characteristic'].iloc[i] = 'hypoallergenic_dog'
    for j in guard_dog:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Breed_characteristic'].iloc[i] = 'guard_dog'

##################################################### American Kennel club (barking levels)

from bs4 import BeautifulSoup
import requests
import re

list_urls = ['https://www.akc.org/dog-breeds/?barking_level%5B%5D=when-necessary',
             'https://www.akc.org/dog-breeds/?barking_level%5B%5D=infrequent',
             'https://www.akc.org/dog-breeds/?barking_level%5B%5D=medium',
             'https://www.akc.org/dog-breeds/?barking_level%5B%5D=frequent',
             'https://www.akc.org/dog-breeds/?barking_level%5B%5D=likes-to-be-vocal']


rare = []
infrequent = []
medium = []
frequent = []
very_common = []


def get_page_links(url):
    baseurl = 'https://www.akc.org/dog-breeds/'
    r = requests.get(url)
    sp = BeautifulSoup(r.text,)
    links = sp.select('h3.breed-type-card__title.mt0.mb0.f-25.py3.px3')
    for link in links:
        breed = link.get_text()
        if 'necessary' in url:
            rare.append(breed)
        elif 'infrequent' in url:
            infrequent.append(breed)
        elif 'medium' in url:
            medium.append(breed)
        elif 'frequent' in url:
            frequent.append(breed)
        elif 'vocal' in url:
            very_common.append(breed)

for url in list_urls:
    for j in re.finditer('breeds[/]', url):
        print(j.start(), j.end())
        x = j.end()
        y = range(1,13)
        for z in y:
            next_page = url[:x] + 'page' + '/' + str(z) + '/' + url[x:]
            print(next_page)
            get_page_links(next_page)


for i in range(len(rare)):
    rare[i] = rare[i].lower()
for i in range(len(infrequent)):
    infrequent[i] = infrequent[i].lower()
for i in range(len(medium)):
    medium[i] = medium[i].lower()
for i in range(len(frequent)):
    frequent[i] = frequent[i].lower()
for i in range(len(very_common)):
    very_common[i] = very_common[i].lower()

#################### new variable (barking level)

df_total['Barking_level'] = 'Unknown'


for i in range(len(df_total['Primary_Breed'])):
    for j in rare:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Barking_level'].iloc[i] = 'rare'
    for j in infrequent:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Barking_level'].iloc[i] = 'infrequent'
    for j in medium:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Barking_level'].iloc[i] = 'medium'
    for j in frequent:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Barking_level'].iloc[i] = 'frequent'
    for j in very_common:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['Barking_level'].iloc[i] = 'very_common'


##################################################### American Kennel club (activity levels)

from bs4 import BeautifulSoup
import requests
import re

list_urls = ['https://www.akc.org/dog-breeds/?activity_level%5B%5D=calm',
             'https://www.akc.org/dog-breeds/?activity_level%5B%5D=regular-exercise',
             'https://www.akc.org/dog-breeds/?activity_level%5B%5D=energetic',
             'https://www.akc.org/dog-breeds/?activity_level%5B%5D=needs-lots-of-activity']


low = []
medium_low = []
medium_high = []
high = []


def get_page_links(url):
    baseurl = 'https://www.akc.org/dog-breeds/'
    r = requests.get(url)
    sp = BeautifulSoup(r.text,)
    links = sp.select('h3.breed-type-card__title.mt0.mb0.f-25.py3.px3')
    for link in links:
        breed = link.get_text()
        if 'calm' in url:
            low.append(breed)
        elif 'regular' in url:
            medium_low.append(breed)
        elif 'energetic' in url:
            medium_high.append(breed)
        elif 'needs' in url:
            high.append(breed)

for url in list_urls:
    for j in re.finditer('breeds[/]', url):
        print(j.start(), j.end())
        x = j.end()
        y = range(1,12)
        for z in y:
            next_page = url[:x] + 'page' + '/' + str(z) + '/' + url[x:]
            print(next_page)
            get_page_links(next_page)


for i in range(len(low)):
    low[i] = low[i].lower()
for i in range(len(medium_low)):
    medium_low[i] = medium_low[i].lower()
for i in range(len(medium_high)):
    medium_high[i] = medium_high[i].lower()
for i in range(len(high)):
    high[i] = high[i].lower()

#################### new variable (activity level)


df_total['activity_level'] = 'not_define'


for i in range(len(df_total['Primary_Breed'])):
    for j in low:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['activity_level'].iloc[i] = 'low'
    for j in medium_low:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['activity_level'].iloc[i] = 'medium_low'
    for j in medium_high:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['activity_level'].iloc[i] = 'medium_high'
    for j in high:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['activity_level'].iloc[i] = 'high'


##################################################### American Kennel club (group)

from bs4 import BeautifulSoup
import requests
import re

list_urls = ['https://www.akc.org/dog-breeds/?group%5B%5D=sporting',
             'https://www.akc.org/dog-breeds/?group%5B%5D=working',
             'https://www.akc.org/dog-breeds/?group%5B%5D=toy',
             'https://www.akc.org/dog-breeds/?group%5B%5D=herding',
             'https://www.akc.org/dog-breeds/?group%5B%5D=foundation-stock-service',
             'https://www.akc.org/dog-breeds/?group%5B%5D=hound',
             'https://www.akc.org/dog-breeds/?group%5B%5D=terrier',
             'https://www.akc.org/dog-breeds/?group%5B%5D=non-sporting',
             'https://www.akc.org/dog-breeds/?group%5B%5D=miscellaneous-class']


sporting_group = []
working_group = []
toy_group = []
herding_group = []
stock_service_group = []
hound_group = []
terrier_group = []
non_sporting_group = []
miscellaneous_group = []


def get_page_links(url):
    baseurl = 'https://www.akc.org/dog-breeds/'
    r = requests.get(url)
    sp = BeautifulSoup(r.text,)
    links = sp.select('h3.breed-type-card__title.mt0.mb0.f-25.py3.px3')
    for link in links:
        breed = link.get_text()
        if 'sporting' in url:
            if 'non-sporting' not in url:
                sporting_group.append(breed)
        elif 'working' in url:
            working_group.append(breed)
        elif 'toy' in url:
            toy_group.append(breed)
        elif 'herding' in url:
            herding_group.append(breed)
        elif 'stock' in url:
            stock_service_group.append(breed)
        elif 'hound' in url:
            hound_group.append(breed)
        elif 'terrier' in url:
            terrier_group.append(breed)
        elif 'non-sporting' in url:
            non_sporting_group.append(breed)
        elif 'miscellaneous' in url:
            miscellaneous_group.append(breed)


for url in list_urls:
    for j in re.finditer('breeds[/]', url):
        print(j.start(), j.end())
        x = j.end()
        y = range(1,7)
        for z in y:
            next_page = url[:x] + 'page' + '/' + str(z) + '/' + url[x:]
            print(next_page)
            get_page_links(next_page)


for i in range(len(sporting_group)):
    sporting_group[i] = sporting_group[i].lower()
for i in range(len(working_group)):
    working_group[i] = working_group[i].lower()
for i in range(len(toy_group)):
    toy_group[i] = toy_group[i].lower()
for i in range(len(herding_group)):
    herding_group[i] = herding_group[i].lower()
for i in range(len(stock_service_group)):
    stock_service_group[i] = stock_service_group[i].lower()
for i in range(len(hound_group)):
    hound_group[i] = hound_group[i].lower()
for i in range(len(terrier_group)):
    terrier_group[i] = terrier_group[i].lower()
for i in range(len(non_sporting_group)):
    non_sporting_group[i] = non_sporting_group[i].lower()
for i in range(len(miscellaneous_group)):
    miscellaneous_group[i] = miscellaneous_group[i].lower()

#################### new variable (breed_group)

df_total['breed_group'] = 'not_define'


for i in range(len(df_total['Primary_Breed'])):
    for j in sporting_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'sporting_group'
    for j in working_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'working_group'
    for j in toy_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'toy_group'
    for j in herding_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'herding_group'
    for j in stock_service_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'stock_service_group'
    for j in hound_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'hound_group'
    for j in terrier_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'terrier_group'
    for j in non_sporting_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'non_sporting_group'
    for j in miscellaneous_group:
        if j in df_total["Primary_Breed"].iloc[i]:
            df_total['breed_group'].iloc[i] = 'miscellaneous_group'





############################ custom (uk info and others)


for i in range(len(df_total['Primary_Breed'])):
    if 'pit bull' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'medium'
        df_total['Trainability'].iloc[i] = 'agreeable'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'medium'
        df_total['activity_level'].iloc[i] = 'medium_high'
        df_total['breed_group'].iloc[i] = 'working_group'
    if 'alaskan husky' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'medium'
        df_total['Trainability'].iloc[i] = 'agreeable'
        df_total['Breed_characteristic'].iloc[i] = 'Not_define'
        df_total['Barking_level'].iloc[i] = 'very_common'
        df_total['activity_level'].iloc[i] = 'high'
        df_total['breed_group'].iloc[i] = 'sporting_group'
    if 'yorkshire terrier' in df_total["Primary_Breed"].iloc[i]:    # american kennek club (not downloaded)
        df_total['Breed_size'].iloc[i] = 'small'
        df_total['Trainability'].iloc[i] = 'agreeable'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'frequent'
        df_total['activity_level'].iloc[i] = 'medium_low'
        df_total['breed_group'].iloc[i] = 'toy_group'
    if 'feist' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'small'
        df_total['Trainability'].iloc[i] = 'easy'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'rare'
        df_total['activity_level'].iloc[i] = 'medium_low'
        df_total['breed_group'].iloc[i] = 'hound_group'
    if 'american pit bull terrier' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'large'
        df_total['Trainability'].iloc[i] = 'agreeable'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'medium'
        df_total['activity_level'].iloc[i] = 'medium_high'
        df_total['breed_group'].iloc[i] = 'pitbull'
    if 'wire hair fox terrier' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'small'
        df_total['Trainability'].iloc[i] = 'independent'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'frequent'
        df_total['activity_level'].iloc[i] = 'medium_high'
        df_total['breed_group'].iloc[i] = 'terrier_group'
    if 'german pointer' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'large'
        df_total['Trainability'].iloc[i] = 'pleaser'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'medium'
        df_total['activity_level'].iloc[i] = 'high'
        df_total['breed_group'].iloc[i] = 'sporting_group'
    if 'blue lacy' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'large'
        df_total['Trainability'].iloc[i] = 'independent'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'frequent'
        df_total['activity_level'].iloc[i] = 'high'
        df_total['breed_group'].iloc[i] = 'working_group'
    if 'english shepherd' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'large'
        df_total['Trainability'].iloc[i] = 'pleaser'
        df_total['Breed_characteristic'].iloc[i] = 'smartest_dog'
        df_total['Barking_level'].iloc[i] = 'rare'
        df_total['activity_level'].iloc[i] = 'high'
        df_total['breed_group'].iloc[i] = 'herding_group'
    if 'landseer' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'xlarge'
        df_total['Trainability'].iloc[i] = 'pleaser'
        df_total['Breed_characteristic'].iloc[i] = 'guard_dog'
        df_total['Barking_level'].iloc[i] = 'infrequent'
        df_total['activity_level'].iloc[i] = 'medium_low'
        df_total['breed_group'].iloc[i] = 'working_group'
    if 'wirehaired pointing griffon' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'xlarge'
        df_total['Trainability'].iloc[i] = 'pleaser'
        df_total['Breed_characteristic'].iloc[i] = 'smartest_dog'
        df_total['Barking_level'].iloc[i] = 'medium'
        df_total['activity_level'].iloc[i] = 'high'
        df_total['breed_group'].iloc[i] = 'sporting_group'
    if 'patterdale terr' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'small'
        df_total['Trainability'].iloc[i] = 'pleaser'
        df_total['Breed_characteristic'].iloc[i] = 'smartest_dog'
        df_total['Barking_level'].iloc[i] = 'rare'
        df_total['activity_level'].iloc[i] = 'high'
        df_total['breed_group'].iloc[i] = 'terrier_group'
    if 'xoloitzcuintli' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'medium'
        df_total['Trainability'].iloc[i] = 'pleaser'
        df_total['Breed_characteristic'].iloc[i] = 'smartest_dog'
        df_total['Barking_level'].iloc[i] = 'medium'
        df_total['activity_level'].iloc[i] = 'medium_high'
        df_total['breed_group'].iloc[i] = 'stock_service_group'
    if 'kangal' in df_total["Primary_Breed"].iloc[i]:
        df_total['Breed_size'].iloc[i] = 'xlarge'
        df_total['Trainability'].iloc[i] = 'pleaser'
        df_total['Breed_characteristic'].iloc[i] = 'family_dog'
        df_total['Barking_level'].iloc[i] = 'very_common'
        df_total['activity_level'].iloc[i] = 'medium_low'
        df_total['breed_group'].iloc[i] = 'working_group'


#cols2 = ['Breed_size','Trainability','Breed_characteristic','Barking_level','activity_level','Outcome_Type','adopted/non-adopted','breed_group']
#df_total[cols2] = df_total[cols].astype('category')



# save as csv
df_total.to_csv('df_total1.csv')


# Profile creation
prof_total = pandas_profiling.ProfileReport(df_total)
prof_total.to_file('pandas_profile_TOTAL.html')


