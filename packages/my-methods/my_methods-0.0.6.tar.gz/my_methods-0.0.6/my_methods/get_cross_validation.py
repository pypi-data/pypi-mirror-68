def get_cross_validation(X, y, model, cv = 10, print_out = True, add_variable = True, poly_features = False, extra_name = None):
  import my_global_variables
  import numpy as np
  class_name = model.__class__.__name__
  if poly_features:
    class_name += '_poly'
  if extra_name:
    class_name += '_' + extra_name
  from sklearn.model_selection import cross_val_score
  cross_val_scores = cross_val_score(model, X, y, cv = cv)
  mean = np.mean(cross_val_scores)
  variance = cross_val_scores.std()
  if add_variable:
    my_global_variables.model_cross_validation[class_name] = {'mean':mean, 'variance': variance}
  if print_out:
    print(f'{cv} fold cross-validation for -- {class_name}-- Model \n\n')
    print(f'cross validation score for {cv} fold cross-validation is:-- \n {cross_val_scores}\n\n')
    print(f'variance in scores for {cv} fold cross-validationn for {model.__class__.__name__}:-- {variance}\n\n')
    return f'Mean for {cv} fold cross-validation score:-- {mean}'
  return mean
