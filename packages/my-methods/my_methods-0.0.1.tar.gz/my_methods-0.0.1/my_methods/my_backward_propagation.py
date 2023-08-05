def my_backward_propagation(X_opt,y, model = None, adj_r2 = 0):
  '''This method automatically return a model with optimal number of independent variable those are perfect for our dependent variable
  my_backward_propagation(X_opt, model = None, adj_r2 = 0)
  where 
  X_opt = initial features
  
  model = initial model
  
  adj_r2 = initial adjusted r-squared
  
  '''
  import statsmodels.formula.api as sm
  
  #create model
  regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
  pvalues = regressor_OLS.pvalues
  adj_r2_now = regressor_OLS.rsquared_adj
  
  #check if adjusted r2 is greater than previous model's adjusted r2
  #if it is then delete column which have maximum p_values
  #else return this model because when we delete a feature which have maximum p_value then our model's adjusted_r2 is decreasing
  #but we need our model have maximum adjusted_r2 value
  if adj_r2_now > adj_r2:
    #check which independent feature have maximum p_value
    max_pval_col = pvalues.argmax()
    
    #delete feature which have maximum p_value
    X_opt = np.delete(X_opt, max_pval_col, 1)
    
    #recursive this program for next model
    return my_regressor_OLS(X_opt,y, model = regressor_OLS, adj_r2 = adj_r2_now)
  return model
