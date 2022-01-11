import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib

import mysql.connector

###-----  MySQL connection-----


# connecting to mysql
db = mysql.connector.connect(
            host = '####',
            user = '####',
            passwd = '####',
            database = 'housing_market'
        )   # The information in this section was anonymize 

# selecting table
cur = db.cursor()
sql_query = "SELECT * FROM housing_market_333"
cur.execute(sql_query)
# importing to dataframe
df_sql_data = pd.DataFrame(cur.fetchall())
db.close()

#----- data cleaning & exploration  -------

df = df_sql_data

# renaming columns
list_names = [
            'identifier',
            'city',
            'price',
            'address',
            'beds',
            'baths',
            'description',
            'features',
            'one_person',
            'one_family',
            'two_plus_people',
            'two_plus_families',
            'age0_to_4',
            'age5_to_9',
            'age10_to_14',
            'age15_to_19',
            'age20_to_34',
            'age35_to_49',
            'age50_to_64',
            'age65_to_79',
            'age80_plus',
            'en_only',
            'fr_only',
            'en_and_fr',
            'other',
            'mother_tongue',
            'owners',
            'renters',
            'life_stage',
            'employment_type',
            'average_household_income',
            'average_number_of_children',
            'no_certificate_diploma_degree',
            'high_school_certificate_or_equivalent',
            'apprenticeship_trade_certificate_diploma',
            'college_non_university_certificate',
            'university_certificate_below_bachelor',
            'university_degree',
            'by_car',
            'by_public_transit',
            'by_walking',
            'by_bicycle',
            'by_other_methods',
            'apartments_low_and_high_rise',
            'houses'

]
num = list(range(0,45))
for i in num:
        print('BEFORE RENAME:', df.columns)
        dict_names = {i : list_names[i] }
        print(dict_names)
        df.rename(columns=dict_names, inplace=True)
        print('AFTER RENAME:', df.columns)


# check shape & type
print('SHAPE OF DATA: ', df.shape)
print('DATA TYPE: ', df.dtypes)


### ----------- triming information -----------

df = df.join(
   df['identifier'].str.split(' ', expand=True).rename(
       columns={0:'MLS', 1:'#', 2:'ID'}
            )
        )
df = df.drop('#',1)

# Standardization of names (cities)

df['city'] = df['city'].str.lower().str.strip().str.extract(r'(vancouver|hamilton|montréal|toronto|mississauga|calgary|ottawa|edmonton|mississauga|winnipeg|brampton)')


# clean prices and convert to int

df['price'] = df['price'].str.replace(r"\D+","").astype('int')

# clean household income and convert to int
df['average_household_income_ctg'] = df['average_household_income'].str.replace(r"\D+","").str[:-2].astype('float')

df['average_household_income_ctg'] = pd.cut(df['average_household_income_ctg'],
                                            bins=[0,25000, 62900, 97900, 244800,776000],
                                            labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])


# clean address
for i in df['address']:
    if "#" in i[0]:
        df['address'] = df['address'].str.replace(r"^[#]","")
    else:
        pass

# get postal code
df['postal_code'] = df.address.str.extract("([A-Z][0-9][A-Z] [0-9][A-Z][0-9])")
df['postal_code'] = df['postal_code'].fillna('Unknown')

# Features and description (deal with missing) - preventive measure

df['description'] = df['description'].fillna('Unknown')
df['features'] = df['features'].fillna('Unknown')


# clean column (beds)
for i in df['beds']:
    try:
        if len(i) >2:
            j = int(i[0]) + int(i[2])
            df['beds'] = df['beds'].replace(i,j)
    except:
        pass
    if 'None' == i:
        df['beds'] = df['beds'].replace('None',"0")
med = df['beds'].median()
df['beds'] = df['beds'].fillna(med)
df=df.astype({"beds":int})


# clean column (baths)
for i in df['baths']:
    try:
        if len(i) >2:
            j = int(i[0]) + int(i[2])
            df['baths'] = df['baths'].replace(i,j)
    except:
        pass
    if 'None' == i:
        df['baths'] = df['baths'].replace('None',"0")
med = df['baths'].median()
df['baths'] = df['baths'].fillna(med)
df=df.astype({"baths":int})


# Categorization of percentages

list_of_categorization = [
            'one_person',
            'one_family',
            'two_plus_people',
            'two_plus_families',
            'age0_to_4',
            'age5_to_9',
            'age10_to_14',
            'age15_to_19',
            'age20_to_34',
            'age35_to_49',
            'age50_to_64',
            'age65_to_79',
            'age80_plus',
            'en_only',
            'fr_only',
            'en_and_fr',
            'other',
            'owners',
            'renters',
            'no_certificate_diploma_degree',
            'high_school_certificate_or_equivalent',
            'apprenticeship_trade_certificate_diploma',
            'college_non_university_certificate',
            'university_certificate_below_bachelor',
            'university_degree',
            'by_car',
            'by_public_transit',
            'by_walking',
            'by_bicycle',
            'by_other_methods',
            'apartments_low_and_high_rise',
            'houses'
]


for i in list_of_categorization:
    try:
        df[i] = df[i].str.replace(r'[%]', '').astype('float')
        df[i] = pd.cut(df[i], bins=[0, 20, 40, 60, 80, 100],
                                  labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        df[i] = df[i].fillna('Very Low')    # the extremely small values (ex:0.0005) were missing
    except:
        pass

### replacing of average_number_of_children

df['average_number_of_children_2'] = df['average_number_of_children'].str.replace(r"\.[0-9]+","").astype('category')



# clean & select the top 3 mother tongues (in the area of the property)

list_of_tongue = df.mother_tongue.str.findall('([a-z]+)')

list0 = [item[0] for item in list_of_tongue] # work well but there is some missing data (try including ddata in the missing seciton)
print(list0)
print(len(list0))

for i in list_of_tongue:
    if len(i) < 3:
        print('initial', i )
        plot_data = [[]]*2
        plot_data[0].append('No lenguage')
        i.append(plot_data)
        i.append(plot_data)
        print('final', i)

list1 = [item[1] for item in list_of_tongue]
print(list1)
print(len(list1))

list2 = [item[2] for item in list_of_tongue]
print(list2)
print(len(list2))

df['top_1_mother_tongue'],df['top_2_mother_tongue'],df['top_3_mother_tongue'] = list0, list1, list2



#------ Checking categories ---------

# numeric columns
df_numeric = df.select_dtypes(include=[np.number])
numeric_cols = df_numeric.columns.values
print(numeric_cols)

# select non numeric columns
df_non_numeric = df.select_dtypes(exclude=[np.number])
non_numeric_cols = df_non_numeric.columns.values
print(non_numeric_cols)

"This procedure was done before and after modifications to the data"




####------------   checking for missing values ----------------- 

# check null
print('NUMBER OF NULL VALUES IN EACH COLUMN', df.isnull().sum())

# heatmap
cols  = df.columns[:]
colours = ['#000099','#ffff00']
sns.heatmap(df[cols].isnull(), cmap = sns.color_palette(colours))

# percentage list

"if it's a larger datset and the visualization takes too long can do this --> % of missing"

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{}-{}%'.format(col, round(pct_missing*100)))

# histogram - missing data

for col in df.columns:
    missing = df[col].isnull()
    num_missing = np.sum(missing)

    if num_missing > 0:
        print('created missing indicator for: {}'.format(col))
        df['{}_ismissing'.format(col)] = missing

"based on indicators, plot it"
ismissing_cols = [col for col in df.columns if 'ismissing' in col]
df['num_missing'] = df[ismissing_cols].sum(axis=1)

df['num_missing'].value_counts().reset_index().sort_values(by='index').plot.bar(x='index', y='num_missing')

"This procedure was done before and after modifications to the data"

"the vast mayority of missing values are so small that the website put them as 'none', instead of 0.0001%" \


# Delivery to tableau

df.to_csv('housing_data_for_tableau.csv')


### irregular  data (outliers)

# ----> numeric
# histogram .
df['price'].hist(bins=100)
# box plot.
df.boxplot(column=['price'])

# ---> categorical
# bar chart -  distribution of a categorical variable
df['life_stage'].value_counts().plot.bar() 
df['employment_type'].value_counts().plot.bar() 
df['houses'].value_counts().plot.bar()



