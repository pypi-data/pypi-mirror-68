def choose_best_classifier(X, y, kfold = 10, scoring = None,pca_n_components = 2,  figsize = None,  x_ticks_rotation = -40,
                           plt_show = False, print_results = True, dependent_variable = None, verbose = 0, seed_no = 46,  **kwargs):
  '''This method returns mean and variance of k_fold fold cross validation scores and 
  also returns a boxplot of 10 scores for every model
  
  Note:-- all sklearn's estimators have default parameters.
  
  
  k_fold = default is 10
  scoring = default is None, it's scoring matrix for cross_validation, pass it according to your evaluation type
  **kwargs pass parameters of any classifier given below
  names of each classifiers
  
  PCA with LR = LogisticRegression()                 #Principle compnent analysis with Logistic Regression
  Logistic Regression = LogisticRegression()         #Logistic Regression
  LDA = LinearDiscriminantAnalysis()                 #Linear Discriminant analysis
  KNN =  KNeighborsClassifier()                      #K-Nearest Neighbors Classifier
  DTree = DecisionTreeClassifier()                   #Decision Tree Classifier
  RandomForest = RandomForestClassifier()            #Random Forest Classifier
  Naive Bayes =  GaussianNB()                        #Naive Bayes classifier
  SVM = SVC()                                        #Support Vector Machines
  Xgboost = XGBClassifier()                          #XG Boost Classifier
  
  '''
  import numpy as np
  np.random.seed(seed_no)
  import matplotlib.pyplot as plt
  import sys
  from sklearn.model_selection import cross_val_score
  from sklearn.model_selection import cross_val_score
  from sklearn.linear_model import LogisticRegression
  from sklearn.tree import DecisionTreeClassifier
  from sklearn.neighbors import KNeighborsClassifier
  from sklearn.ensemble import RandomForestClassifier
  from xgboost import XGBClassifier
  from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
  from sklearn.decomposition import PCA
  from sklearn.naive_bayes import GaussianNB
  from sklearn.svm import SVC 
  from sklearn.preprocessing import StandardScaler
  
  #name of dependent variable
  if not dependent_variable:
    try:
      dependent_variable = y.name
    except:
      dependent_variable = None
  # prepare configuration for cross validation test harness
  seed = 7
  # prepare models
  pca = PCA(n_components = pca_n_components)
  X_pca = pca.fit_transform(X)
  models = {}
  models['PCA with LR'] = LogisticRegression()
  models['Logistic Regression'] = LogisticRegression()
  models['LDA'] = LinearDiscriminantAnalysis()
  models['KNN'] =  KNeighborsClassifier()
  models['DTree'] =  DecisionTreeClassifier()
  models['RandomForest'] = RandomForestClassifier()
  models['Naive Bayes'] = GaussianNB()
  models['SVM'] =  SVC()
  models['Xgboost'] = XGBClassifier()
  # evaluate each model in turn
  if kwargs:
    for item, values in kwargs.items():
      if type(values) is dict:
        models[item] = models[item].set_params(**values)
      else:
        break

  results = []
  names = []
  l = len(models)
  n = 1
  if print_results:
    print('model name:-- scores mean, (scores variance)')
  for name, model in models.items():
    n += 1
    features = X
    if name == 'PCA with LR':
      features = X_pca.copy()
      print(features.shape)
    if name == 'KNN':
      sc = StandardScaler()
      features = sc.fit_transform(X).copy()

    cv_results = cross_val_score(model, features, y, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = f'{name}: -- {cv_results.mean():.4f}, ({cv_results.std():.4f})'
    if print_results:
      print(msg)
  # boxplot algorithm comparison
  #return names, results
  title = f'Algorithm Comaprision for {dependent_variable}'
  #sys.stdout.write(f'\r Done for {dependent_variable}\'s model')
  if figsize:
    plt.figure(figsize = figsize)
  plt.title(title)
  plt.boxplot(results)
  ypos = np.arange(1, len(names)+1)
  plt.xticks(ypos, names, rotation = x_ticks_rotation)
  sys.stdout.write('\r Done')
  if plt_show:
    plt.show()
