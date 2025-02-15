from django.core.management.base import BaseCommand
from gs_scholar.models import Questionnaire, Datainserted,Section

class Command(BaseCommand):
    help = 'Your help message here'
    def handle(self, *args, **options):
        import matplotlib.pyplot as plt
        import pandas as pd
        from math import pi
        
        # Assuming you have fetched the relevant data from your models
        # Replace 'YourQuestionnaireObject' and 'YourMatierObject' with the actual objects you have
        questionnaire = Questionnaire.objects.get(id=17)
        matier = Questionnaire.objects.get(id=17).matier
        
        # Fetch Datainserted objects for the specific questionnaire and matier
        data_objects = Datainserted.objects.filter(questionnaire=questionnaire, matier_code=matier.code)
        sections_to_exclude = Section.objects.all().order_by('-order')[:4]
        data_objects = data_objects.exclude(section__in=sections_to_exclude)
        # Group data by section
        sections_data = {}
        for obj in data_objects:
            if obj.section not in sections_data:
                sections_data[obj.section] = {'pourcentage': 0}
            sections_data[obj.section]['pourcentage'] = Datainserted.calculate_percentage_for_section(questionnaire, obj.section)
        
        # Prepare data for radar chart
        data = {'group': [section.name for section in sections_data.keys()]}
        data['pourcentage'] = [data['pourcentage'] * 100 for data in sections_data.values()]
        
        df = pd.DataFrame(data)
        
        # Plot the radar chart
        plt.clf()
        N = len(df['group'])
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        
        ax = plt.subplot(111, polar=True)
        plt.title(f' {matier.code}')
        def add_line_breaks(name):
            words = name.split(' ')
            if len(words) > 4:
                words.insert(4, '\n')
            return ' '.join(words)
        
        # Add line breaks for every fourth space in section names
        tick_labels = [add_line_breaks(name) for name in df['group']]
        plt.xticks(angles[:-1], tick_labels, color='red', size=8)
        ax.set_rlabel_position(0)
        
        plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=7)
        plt.ylim(0, 100)
        
        values = df['pourcentage'].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=3, linestyle='solid')
        ax.fill(angles, values, 'b', alpha=0.1)
        plt.show()
        
        

        self.stdout.write(self.style.SUCCESS('Successfully ran the plot command'))