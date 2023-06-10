import os
import pandas as pd

# from AlcoholScoreboard import app

# DATASET_PATH = os.path.join(app.root_path, 'dataset', 'fruitvegprices-2017_2022.csv')
#DATASET_PATH = '/Users/oscarluthje/Desktop/AlcoholScoreboard/dataset/archive/drinks.csv'
DATASET_PATH = 'C:/Users/juand/OneDrive/Documents/DIS/alcoholscoreboard/AlcoholScoreboard/dataset/drinks.csv'


def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        pass
        # for item in choices_list:
        #     setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        # return [(k, v) for k, v in self.__dict__.items()]
        return []

    def values(self):
        # return [v for v in self.__dict__.keys()]
        return []

    def labels(self):
        # return [l for l in self.__dict__.values()]
        return []
    
class ModelChoices2:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]
        

    def values(self):
        return [v for v in self.__dict__.keys()]
        

    def labels(self):
        return [l for l in self.__dict__.values()]
        

df = pd.read_csv(DATASET_PATH, sep=',')

# ProduceCategoryChoices = ModelChoices(df.name.unique())
# ProduceItemChoices = ModelChoices(df.item.unique())
# ProduceVarietyChoices = ModelChoices(df.variety.unique())
# ProduceUnitChoices = ModelChoices(df.unit.unique())

# UserTypeChoices = ModelChoices(['Farmer', 'Customer'])

ProduceCategoryChoices = ModelChoices2(df.country.unique())
ProduceItemChoices = ModelChoices(df.country.unique())
ProduceVarietyChoices = ModelChoices(df.country.unique())
ProduceUnitChoices = ModelChoices(df.country.unique())

UserTypeChoices = ModelChoices(['Farmer', 'Customer'])

# if __name__ == '__main__':
#     print(df.item.unique())
#     print(ProduceItemChoices.choices())
