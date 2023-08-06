def choose_best_regressor(X, y, C = 1.0,figsize = None, n_neighbors = 5, max_depth = 10,k_fold = 10,
                           svc_kernel = 'rbf', n_components = 2, max_depth_xgb = 4, n_estimators = 10, x_ticks_rotation = -40,
                           plt_show = False, print_results = True, dependent_variable = None, verbose = 0):
  import matplotlib.pyplot as plt
  import sys
  import numpy as np
  from sklearn.model_selection import cross_val_score
  from sklearn.linear_model import LinearRegression
  from sklearn.linear_model import Ridge
  from sklearn.linear_model import Lasso
  from sklearn.tree import DecisionTreeRegressor
  from sklearn.neighbors import KNeighborsRegressor
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.decomposition import PCA
  
  #name of dependent variable
  if not dependent_variable:
    try:
      dependent_variable = y.name
    except:
      dependent_variable = None
  # prepare configuration for cross validation test harness
  seed = 7
  # prepare models
  pca = PCA(n_components = n_components)
  X_pca = pca.fit_transform(X)
  models = []
  models.append(('LR', LinearRegression()))
  models.append(('PCA with LR', LinearRegression()))
  models.append(('Lasso', Lasso()))
  models.append(('Ridge', Ridge()))
  models.append(('KNN', KNeighborsRegressor(n_neighbors = n_neighbors)))
  models.append(('DTree', DecisionTreeRegressor(max_depth = max_depth)))
  models.append(('RandomForest', RandomForestRegressor(n_estimators = n_estimators, max_depth = max_depth)))
  # evaluate each model in turn
  results = []
  names = []
  l = len(models)
  n = 1
  for name, model in models:
    if verbose:
      sys.stdout.write(f'\r running {k_fold} cross validation for {dependent_variable}\'s Regressor model No. {n}/{l}')
    n += 1
    features = X
    if name == 'PCA with LR':
      features = X_pca
    cv_results = cross_val_score(model, features, y, cv = k_fold, verbose = 0)
    results.append(cv_results)
    names.append(name)
    msg = f'{name} Regressor: mean = {cv_results.mean()}, std = {cv_results.std()}'
    if print_results:
      print('\n', msg)
  # boxplot algorithm comparison
  title = f'Algorithm Comaprision for {dependent_variable}'
  sys.stdout.write(f'\r Done for {dependent_variable}\'s model')
  if figsize:
    plt.figure(figsize = figsize)
  plt.title(title)
  plt.boxplot(results)
  ypos = np.arange(1, len(names)+1)
  plt.xticks(ypos, names, rotation = x_ticks_rotation)
  sys.stdout.write('\r Done')
  if plt_show:
    plt.show()
