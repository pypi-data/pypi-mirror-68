
def get_insights(file):
    import pandas as pd
    data = pd.read_csv(file)
    print("This data has",len(data.columns),"columns")
    print("Name includes:",data.columns)
    print("It has ",data.isnull().sum().sum(),"missing values")
    print("The missing value columns is",data.columns[data.isnull().any()].tolist())
    print(data.describe())



def pre_test(data,col,col2):
    from scipy.stats import ttest_ind
    from scipy.stats import f_oneway
    from scipy.stats import friedmanchisquare
    from scipy.stats import kruskal
    control = data[data[col]==0]
    exp = data[data[col]==1]
    for i in range(len(data.columns)):
        if data.columns[i] != col or col2:
            if data.dtypes[i] != object:
                print("Variance check for:",data.columns[i])
                stat, p = kruskal(control.iloc[:,i],exp.iloc[:,i])
                print('stat=%.3f, p=%.3f' % (stat, p))
                if p > 0.05:
                    print('They are the same')
                else:
                    print('They are different')
            else:
                print("Variance check for:",data.columns[i])
                stat, p = f_oneway(control.iloc[:,i].value_counts(),exp.iloc[:,i].value_counts())
                print('stat=%.3f, p=%.3f' % (stat, p))
                if p > 0.05:
                    print('They are the same')
                else:
                    print('They are different')
        else: pass


def final_test(data,col,col2):
    #col = str(col)
    #col2 = str(col2)
    control = data[data[col]==0]
    exp = data[data[col]==1]
    stat, p = ttest_ind(control[col2].values,exp[col2].values,equal_var=False)
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
        print('They are the same')
    else:
        print('They are different')

