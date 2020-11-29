import pandas, re, os


class CollectionFolder:
    def __init__(self, path):
        pass



class CollectionObject:

    collectors = ()

    def __init__(self, path):

        if path.endswith('.xls') or path.endswith('.xlsx'):
            self.df = pandas.read_excel(path)
        elif path.endswith('.csv'):
            self.df = pandas.read_csv(path)
        else:
            raise TypeError('Incorrect file format - Excel/Csv expected but {format} was given'
                            .format(format = re.search('\..*$', path).group()))

        self.year = re.search('_\d\d\d\d_', path).group()[1:-1]
        self.mc_series = self.df[self.df.columns[0]]
        self.new_buildings_series = self.df[self.df.columns[1]]


    def collect(self):
        pass

    def plot(self):
        pass



file = CollectionObject('A1302_SOP03_TB_MM_00_2002_26_F_GR.xls')
file2 = CollectionObject('A1302_SOP03_TB_MM_00_2009_26_F_GR.xlsx')

print (file.df, file.new_buildings_series)
print(file.df._info_axis)

print(set([1,2,2,2,2,4,5,6,7]))
print(set([1,1,1,2,2,3,3,3,5,6,7,10,11,12]))

print(set([1,2,2,2,2,4,5,6,7]) - set([1,1,1,2,2,3,3,3,5,6,7,10,11,12]))