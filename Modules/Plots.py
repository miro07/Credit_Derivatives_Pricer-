import seaborn as sns
import matplotlib.pyplot as plt
import itertools

def distrubitions_plot(labels,*argv):
    plt.style.use('seaborn-darkgrid')
    for arg,lb in itertools.zip_longest(argv,labels):
        sns.distplot(arg, hist=False,rug=True, kde=True,
                    kde_kws={'shade': True, 'linewidth': 3},label= lb)
    plt.legend(prop={'size': 16}, title='Correlation')
    plt.title('Density Plot with Multiple Default Time')
    plt.xlabel('Default Time')
    plt.ylabel('Density')
    plt.show()
def dot_plot(labels,*argv):
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    dim=[]
    labs=[]
    for arg,lb in itertools.zip_longest(argv,labels):
        dim.append(arg)
        labs.append(lb)

    ax.scatter(dim[0],dim[1], dim[2])
    ax.set_xlabel(labs[0])
    ax.set_ylabel(labs[1])
    ax.set_zlabel(labs[2])

    plt.show()
