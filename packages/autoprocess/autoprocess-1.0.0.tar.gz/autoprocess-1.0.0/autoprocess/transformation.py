

def log(X):
    for i in X.columns:
        if X[i].dtypes=="float64":
            X[i]=np.log(X[i])
    return X

def min_max(X):
    for i in X.columns:
        if X[i].dtypes=="float64":
            X[i]=(np.mean(X[i])-X[i])/(max(X[i])-min(X[i]))
    return X

def std_scaler(X):
     for i in X.columns:
        if X[i].dtypes=="float64":
            X[i]=(np.mean(X[i])-X[i])/(np.std(X[i]))
     return X    

