
### The project was completed on Codecademy.com

import codecademylib
import pandas as pd
import matplotlib 
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency
import numpy as np

# Read in dataset
species = pd.read_csv('species_info.csv', delimiter = ',')
print species.head(10)

# Count number of different spcies
species_count = species.scientific_name.nunique()
print 'how many different species?', species_count

# Show unique categories 
species_type = species.category.unique()
print 'different categories?', species_type

# Show unique categories 
conservation_statuses = species.conservation_status.unique()
print 'conservation statuses', conservation_statuses

# Count scientific names in each conservation_status
conservation_counts = species.groupby("conservation_status").scientific_name.nunique().reset_index()
print conservation_counts 

# Replace NaN-s 
species.fillna('No Intervention', inplace = True)

# Count scientific names in each conservation_status
conservation_counts_fixed = species.groupby("conservation_status").scientific_name.nunique().reset_index()
print conservation_counts_fixed 

# Count how many species have a certain conservation status in each category?
category_species = species.groupby(["category","conservation_status"]).scientific_name.nunique().reset_index()
print category_species

category_species_pivot=category_species.pivot(
         columns='category',
		     index='conservation_status',
         values='scientific_name').reset_index()
print category_species_pivot

# Calculate number of species by category for pie chart
categpry_type_nr = species.groupby('category').scientific_name.nunique().reset_index()
print 'nr of species in different categories?', categpry_type_nr
species_names_list = categpry_type_nr.category
print species_names_list

species_nr_list = categpry_type_nr.scientific_name
print species_nr_list

plt.pie(species_nr_list, autopct='%0.1f%%')
plt.axis('equal')
plt.legend(species_names_list)
plt.show()

# Make pie chart of endangered species
prot_count_names_before = ['Endangered', 'In Recovery', 'Species of concern', 'Threatened' ]
prot_count_freqs_before = [15, 4, 151, 10]
plt.pie(prot_count_freqs_before, autopct='%0.1f%%')
plt.axis('equal')
plt.legend(prot_count_names_before)
plt.show()

# Copy and pasting following line:
protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
    
print protection_counts

# Make pie chart of conservation statuses
prot_count_names_before = ['Endangered', 'In Recovery', 'Species of concern', 'Threatened' ]
prot_count_freqs_before = [15, 4, 151, 10]
plt.pie(prot_count_freqs_before, autopct='%0.1f%%')
plt.axis('equal')
plt.legend(prot_count_names_before)
plt.show()

# Make pie chart of conservation statuses
prot_count_names = protection_counts.conservation_status
prot_count_freqs = protection_counts.scientific_name
plt.pie(prot_count_freqs, autopct='%0.1f%%')
plt.axis('equal')
plt.legend(prot_count_names)
plt.show()

# Make barchart of conservation status by species
height = protection_counts.scientific_name
nr_ticks = range(len(protection_counts.conservation_status))
plt.figure(figsize=(10,4))
ax = plt.subplot()
plt.bar(nr_ticks, np.log10(height))
ax.set_xticks(nr_ticks)
ax.set_xticklabels(protection_counts.conservation_status, fontsize=12)
plt.title('Conservation Status by Species', fontsize=13)
plt.ylabel('log$_{10}$(Number of Species)', fontsize=13)
plt.show()

# Examine protected/non-protected categories.
statement = lambda x: True if x<>'No Intervention' else False
species['is_protected'] = species.conservation_status.apply(statement)

category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index()
print category_counts.head()

# Create pivot table of category counts
category_pivot=category_counts.pivot(
   columns='is_protected',
   index='category',
   values= 'scientific_name').reset_index()
print category_pivot

# Re-name columns
category_pivot.columns = ['category', 'not_protected','protected']        

category_pivot['percent_protected'] = category_pivot.protected/(category_pivot.protected+category_pivot.not_protected)
print category_pivot


# Calculate chi2 statistics 
contingency = [[30, 146],
              [75, 413]]

chi2, pval, dof, expected = chi2_contingency(contingency)
print pval, 'mammal, bird diff. not significant '

contingency2 = [[5, 73],
              [30, 146]]

chi2_r_m, pval_reptile_mammal, dof_r_m, expected_r_m=chi2_contingency(contingency2) 
print pval_reptile_mammal, 'reptile, mammal significant diff.'

########################## New project: sheep counts ##################################

# Read in data
observations = pd.read_csv('observations.csv')
print observations.head()

# Add new column with is_sheep status
check = lambda x:True if 'Sheep' in x else False
species['is_sheep'] = species.common_names.apply(check)

# Create is_sheep variable
species_is_sheep = species[species.is_sheep == True]

sheep_species = species[(species.is_sheep == True) & (species.category =='Mammal')]
print sheep_species 

# Merge sheep and observation tables
sheep_observations = pd.merge(sheep_species, observations)
print sheep_observations.head()

# Count sheep sightings
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
print obs_by_park

# Create plot of observations
plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name,fontsize=13)
plt.ylabel('Number of Observations',fontsize=18)
plt.title('Observations of Sheep per Week',fontsize=18)
plt.show()

# Calculate minimum detectable effect
baseline = 15.
minimum_detectable_effect = 100.*5./15.
print minimum_detectable_effect

sample_size_per_variant = 510.

# Check how much time is needed to for minimum detectable effect
yellowstone_weeks_observing = sample_size_per_variant/507.
print yellowstone_weeks_observing, 'weeks are needed at Yellowstone'

bryce_weeks_observing = sample_size_per_variant/250.
print bryce_weeks_observing, 'weeks are needed at Bryce'

smokey_weeks_observing = sample_size_per_variant/149.
print smokey_weeks_observing, 'weeks are needed at Smoky'

