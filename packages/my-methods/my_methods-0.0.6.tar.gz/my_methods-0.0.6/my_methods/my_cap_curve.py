def my_cap_curve(model, X, y, figsize = (10, 5),legend_font_size = 10,loc = 'best',
                 linewidth = 2,label_font_size = 10, poly_features = False, extra_name = None):
  import matplotlib.pyplot as plt
  import numpy as np
  import my_global_variables
  from sklearn.metrics import roc_curve, auc
  class_name = model.__class__.__name__
  if poly_features:
    class_name = class_name + '_poly'
  if extra_name:
    class_name += '_' + extra_name
  total = len(y)
  class_1_count = np.sum(y)
  class_0_count = total - class_1_count
  probs = model.predict_proba(X)
  probs = probs[:, 1]
  model_y = [y for _, y in sorted(zip(probs, y), reverse = True)]
  y_values = np.append([0], np.cumsum(model_y))
  x_values = np.arange(0, total + 1)
  # Area under Random Model
  a = auc([0, total], [0, class_1_count])

  # Area between Perfect and Random Model
  aP = auc([0, class_1_count, total], [0, class_1_count, class_1_count]) - a

  # Area between Trained and Random Model
  aR = auc(x_values, y_values) - a
  plt.figure(figsize = (figsize))
  plt.plot([0, total], [0, class_1_count], c = 'r', linestyle = '--', label = 'Random Model')
  plt.plot([0, class_1_count, total], [0, class_1_count, class_1_count], c = 'grey', linewidth = linewidth, label = 'Perfect Model')
  plt.plot(x_values, y_values, c = 'b', label = f'{class_name} Classifier Accuracy Rate = {aR/aP}', linewidth = linewidth)
  plt.xlabel('Total observations', fontsize = label_font_size)
  plt.ylabel('Class 1 observations', fontsize = label_font_size)
  plt.title('Cumulative Accuracy Profile', fontsize = label_font_size)
  plt.legend(loc = loc, fontsize = legend_font_size)
  plt.show()
  my_global_variables.model_cap_scores[class_name] = aR/aP
