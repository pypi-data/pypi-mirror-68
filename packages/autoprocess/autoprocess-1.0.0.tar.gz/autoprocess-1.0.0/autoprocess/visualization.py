


def univariate_count_plot(variable=y,Label="Count"):
    
    return(sns.countplot(variable,label=Label),variable.value_counts()) 


def univariate_box_plot(X,variable_name):
    plt.figure(figsize=(10,10))
    sns.boxplot(X[variable_name])
    plt.xticks(rotation=90)
