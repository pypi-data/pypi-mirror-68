def my_roc_curve(model, X_test, y_test, fig_size = (10, 5),legend_font_size = 10, loc = 'best', linewidth = 2,
                 label_font_size = 10, poly_features = False, extra_name = None, output = True):
  '''
  model : trained model on training data
  
  X_test: validation features
  y_test: validation target variable
  output : default True 
               it returns fpr, tpr, threshold
  
  '''
  import my_global_variables
  import matplotlib.pyplot as plt
  import numpy as np
  from sklearn.metrics import roc_curve, auc
  class_name = model.__class__.__name__
  if poly_features:
    class_name += '_poly'
  if extra_name:
    class_name += '_' + extra_name
  y_proba = model.predict_proba(X_test)
  proba = y_proba[:, 1]
  fpr, tpr, thresholds = roc_curve(y_test, proba)
  ##AUC
  roc_auc = auc(fpr, tpr)
  label = f'{class_name} -- {roc_auc}'
  plt.plot(fpr, tpr, c = 'g', label = label, linewidth = linewidth)
  plt.xlabel('False Positive Rate(1 - Specificity)', fontsize = label_font_size)
  plt.ylabel('True Positive Rate(Senstitivity)', fontsize = label_font_size)
  plt.title('Receiver Operating Characteristic', fontsize = label_font_size)
  plt.legend(loc = loc, fontsize = legend_font_size)
  plt.show()
  my_global_variables.model_roc_auc[class_name] = roc_auc
  my_global_variables.model_fpr_tpr_thresholds[class_name] = (fpr, tpr, thresholds)
