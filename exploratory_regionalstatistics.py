import os
from datenguidepy import Query, get_regions, get_statistics, get_availability_summary
import matplotlib.pyplot as plt

# overview of region IDS
regions = get_regions()
# get region ID for Berlin and Brandenburg
print(regions[(regions['name']=='Berlin') | (regions['name']=='Brandenburg')]) # 11 & 12

# print subregions
print(regions[regions.parent == '110'])
print(regions[regions.parent == '120'])

# get short names for statistics
stats_names = get_statistics()
print(stats_names.head(10))

# Availability
availability = get_availability_summary()
print(availability.shape)

# Availability for Berlin
availability_berlin = availability[availability['region_name']=='Berlin']
print(availability_berlin.shape) # 1133 statistics
print(availability_berlin.head(20))

# query region Berlin (id == '11')
q = Query.region('11')

# add fields
#q.add_field('BEV001') # Statistik der Geburten
#q.add_field('BEV002') # Statistik der Sterbefaelle
#q.add_field('ERWP06') # Arbeitsmarktstatistik der Bundesagentur für Arbeit
#q.add_field('FLC047') # Agrarstrukturerhebung / Landwirtschaftszählung
#q.add_field('PERS01') # Statistik der öffentlich geförderten Kindertagespflege
#q.add_field('FLCX05') # Flächenerhebung nach Art der tatsächlichen Nutzung
q.add_field('BEV081') # Wanderungsstatistik Zuzuege
q.add_field('BEV082') # Wanderungsstatistik Fortzuege

# get the results as a Pandas DataFrame
df_results = q.results(add_units=True)

# print column names
for col in df_results.columns:
    print(col)

# print head of dataframe
print(df_results.head(10).iloc[:,:7])

# extract relevant columns
df = df_results[['year', 'BEV081', 'BEV082']]

# exploratory line plots
df_subplot = df.plot.line(x='year', y='BEV081', c='Green', label='Zuwanderung')
df.plot.line(x='year', y='BEV082', c='Red', label='Abwanderung', ax=df_subplot)

plt.show()

# export dataframe to csv
df.to_csv(os.getcwd() + '/berlin_regional_statistics.csv')