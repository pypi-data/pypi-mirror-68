def plot_text(text, figsize = (20, 1.5)):
  plt.figure(figsize = figsize)
  plt.text(.5, 0.5, s = text, size= 40,
           ha="center", va="center",
           bbox=dict(boxstyle="round",
                     facecolor = 'blue',
                     ec=(1., 0.5, 0.5),
                     fc=(1., 0.8, 0.8),
                     ))
  sns.despine(left = True, bottom = True)
  plt.xticks([])
  plt.yticks([])
  plt.show()
