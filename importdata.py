import os
import django
import pandas as pd
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mychart.settings')
django.setup()

from mysite.models import Population
df = pd.read_excel("population-112.xls")
data = df[['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2']]
data.columns = data.loc[1]
data.drop(index=data.index[:6], axis=0, inplace=True)
data.drop(data[data['性別']=='計'].index, axis=0, inplace=True)
data['區 域 別'].fillna(method="ffill", inplace=True)
data.fillna(method="ffill", inplace=True)
for d in data.values.tolist():
    rec = Population.objects.filter(name=d[0])
    if len(rec) == 0:
        if d[1]=='男':
            new_rec = Population(name=d[0], male=d[2])
        else:
            new_rec = Population(name=d[0], female=d[2])
        new_rec.save()
    elif len(rec) == 1:
        if d[1]=='男':
            rec[0].name = d[0]
            rec[0].male = d[2] 
        else:
            rec[0].name = d[0]
            rec[0].female = d[2] 
        rec[0].save()
        
