if __name__ == '__main__':
    import pandas as pd
    from pathlib import Path
    import seaborn as sns
    import matplotlib.pyplot as plt

    datPath = Path('Data/QPM.DAT').resolve()
    colNames = ['lam1', 'lam2', 'period', 'tempbw', 'grpvel1', 'grpvel2', 'grpvelblue', 'gdd1', 'gdd2', 'gddblue']
    df = pd.read_table(datPath,
                       names=colNames,
                       sep='\s+')
    # sns.lineplot(data=df,x='period', y='lam2')
    print(df[df['lam2']==1300])
    # print(df[df['lam2'] > 1998][df['lam2'] < 2002])
    print(df.loc[(df['lam2'] > 1998) & (df['lam2'] < 2002)])

    # plt.show()



