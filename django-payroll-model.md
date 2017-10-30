- The raw data

```python
data = """Alfred,M,14,69,112.5
Alice,F,13,56.5,84
Barbara,F,13,65.3,98
Carol,F,14,62.8,102.5
Henry,M,14,63.5,102.5
James,M,12,57.3,83
Jane,F,12,59.8,84.5
Janet,F,15,62.5,112.5
Jeffrey,M,13,62.5,84
John,M,12,59,99.5
Joyce,F,11,51.3,50.5
Judy,F,14,64.3,90
Louise,F,12,56.3,77
Mary,F,15,66.5,112
Philip,M,16,72,150
Robert,M,12,64.8,128
Ronald,M,15,67,133
Thomas,M,11,57.5,85
William,M,15,66.5,112"""


from django.db import models

class Student(models.Model):
    name = models.TextField()
    sex = models.CharField(max_length=1)
    age = models.IntegerField(default=-1)
    weight = models.DecimalField(max_digits=6, decimal_places=1)
    height = models.DecimalField(max_digits=6, decimal_places=1)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class Relationship(models.Model):
    manager = models.ForeignKey(Student, on_delete=models.CASCADE)
    employee = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='employee')

    class Meta:
        unique_together = ('manager', 'employee')

for row in data.split('\n'):
    name, sex, age, weight, height = row.strip().split(',')
    current = Student(name=name, sex=sex, age=int(age), weight=float(weight), height=float(height))
    current.save()
```
