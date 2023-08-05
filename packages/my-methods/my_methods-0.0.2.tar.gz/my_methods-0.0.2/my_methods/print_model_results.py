def print_model_results(X_train, X_test,y_train, y_test, model, add_variable = True, extra_name = None, classification = True):
  '''
  
  X_train = traning features
  X_test = test features
  y_train = training target
  y_test = test target
  model = estimator or classfifier
  add_variable = default is True (to add classifier or other details like cm, roc , auc,  into my_global_variable)
  exra_name = when add_variable is default it saves model or it's details with some extra names in my_global_variables
  classification = True if False it consider it is a regression problem and shows regression metrics
  
  
  also it returns trained model
  
  return : saved model
  '''
  import my_global_variables
  from sklearn.metrics import confusion_matrix, classification_report
  from sklearn.metrics import confusion_matrix, classification_report
  class_name = model.__class__.__name__
  if extra_name:
    class_name += '_' + extra_name
  model.fit(X_train, y_train)
  ts = model.score(X_train, y_train)
  print(F' Train score is {ts}')
  print('\n')
  tst = model.score(X_test, y_test)
  print(f'Test score is {tst}')
  print('\n\n')
  y_pred = model.predict(X_test)
  if classification:
    tcm = confusion_matrix(y_train, model.predict(X_train))
    print(f'Train confusion matrix is \n {tcm}\n')
    ttcm = confusion_matrix(y_test, y_pred)
    print(f'Test confusion matrix is \n {ttcm}')
    print('\n\n')
    print(f'Test Set classification report is \n {classification_report(y_test, y_pred)}')
  if add_variable:
      my_global_variables.model_score[class_name] = {'train':ts, 'test': tst}
      if classification:
        my_global_variables.model_cm[class_name] = {'train':tcm, 'test':ttcm}
      my_global_variables.my_models[class_name] = model
  return model
