import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from .models import Questionnaire,Datainserted

# Assuming you have fetched the relevant data from your models
# Replace 'YourQuestionnaireObject' and 'YourMatierObject' with the actual objects you have
questionnaire = Questionnaire.objects.get(id=17)
matier = Questionnaire.objects.get(id=17).matier

# Fetch Datainserted objects for the specific questionnaire and matier
data_objects = Datainserted.objects.filter(questionnaire=questionnaire, matier_code=matier.code)

# Group data by section
sections_data = {}
for obj in data_objects:
    if obj.section not in sections_data:
        sections_data[obj.section] = {'Non': 0, 'Plutôt non': 0, 'Plutôt oui': 0, 'Oui': 0}
    sections_data[obj.section][obj.selected_choice] += obj.weight

# Prepare data for radar chart
categories = ['Non', 'Plutôt non', 'Plutôt oui', 'Oui']
data = {'group': [section.name for section in sections_data.keys()]}
for category in categories:
    data[category] = [sections_data[section][category] for section in sections_data.keys()]

df = pd.DataFrame(data)

# Plot the radar chart
plt.clf()
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

ax = plt.subplot(111, polar=True)
plt.title(f'Radar Chart for {questionnaire.name} - {matier.code}')

plt.xticks(angles[:-1], categories, color='red', size=8)
ax.set_rlabel_position(0)

plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=7)
plt.ylim(0, 100)

for row in df.itertuples(index=False):
    values = row[1:]
    values += values[:1]
    ax.plot(angles, values, linewidth=3, linestyle='solid', label=row[0])

ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.show()
