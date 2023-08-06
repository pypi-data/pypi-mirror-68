class MyDummyVariable:
  '''it is a class to get dummy variable from a dataframe in this method we are using OneHotEncoder 
    and this method automatically distinguish numeric and categorical columns
    
    =====================================================================================================
    MyDummyVariable(self, drop_first = True, categorical_features = None, all_categorical = False, 
               return_dataframe = True, labeled_features = None, all_labeled = False, unique_threshold = 5, dropna = False)
   =======================================================================================================
   drop_first = default is True, it drops first column for OneHotEncoded Categorical Column
   
   ------------------------------------------------------------------------------------------------------------------
   
   categorical_features = default is None, pass features columns index in a list if you want to specify column on your own
   
   -------------------------------------------------------------------------------------------------------------------
   
   all_categorical = default is False, if it is True then the program consider all the variables as categorical features and this program
                     OneHotEncode all features
                     
   ---------------------------------------------------------------------------------------------------------------------
  
   return_datafram = default is True, if False then it returs a numpy array
   
   ----------------------------------------------------------------------------------------------------------------------
   
   labeled_features = default is None, pass labeled feature index in a list if you want to OneHotEncode specific labeled 
   (numeric column containing less number of unique values) columns into OneHotEncode
   
   ----------------------------------------------------------------------------------------------------------------------
   
   
   all_labeld = default is False, pass it True if you want to OneHotEncode all labeled features when a unique values in any features are
                less than or equeal to unique threshold which is default to 5, you can change
                unique_threshold in next parameter,
   -----------------------------------------------------------------------------------------------------------------------
   
   unique_threshold = default is 5, it is related to all_labeld parameter pass another value if you want to define you onw unique threshold
   
   ------------------------------------------------------------------------------------------------------------------------------------------
   
   drop_na = default is False if Fasle and the dataframe have null values then it may return error, so clean your data frist or pass drop_na = Tru
   
    '''
  #initialize OneHotEncoder for future use when we transform data
  def __init__(self, drop_first = True, categorical_features = None, all_categorical = False, 
               return_dataframe = True, labeled_features = None, all_labeled = False, unique_threshold = 5, drop_na = False):
    self.drop_first = drop_first
    self.categorical_features = categorical_features
    self.all_categorical = all_categorical
    self.return_dataframe = return_dataframe
    self.ohe_encoders = {}
    self.sorted_unique_values = []
    self.labeled_features = labeled_features
    self.unique_threshold = unique_threshold
    self.all_labeled = all_labeled
    self.drop_na = drop_na
  
 
  #fit_transform
  def __repr__(self):
    return f'MyDummyVariable(drop_first = {self.drop_first}, categorical_features = {self.categorical_features},\n \t\t\t \
     all_categorical = {self.all_categorical} ,return_dataframe = {self.return_dataframe},\
     labeld_features = {self.labeled_features}, all_labeled = {self.all_labeled}, unique_threshold = {self.unique_threshold}, drop_na = {self.drop_na})'

  #separate numerica and categorical data
  def separate_data(self, features):
    import numpy as np
    import pandas as pd
    if self.drop_na:
      features = features.dropna()
    if self.categorical_features:
      if 'list' in str(type(self.categorical_features)):
        categorical_data = features.iloc[: ,self.categorical_features]
        if not self.all_categorical:
          numeric_data = features.drop(categorical_data.columns, axis = 1)
        else:
          numeric_data = pd.DataFrame()
      else:
        raise TypeError(f'Type of Categorical_fetures {self.categorical_features} must be list or tuple')
    else:
      categorical_data = features.select_dtypes(include = 'object')
      numeric_data = features.select_dtypes(exclude = 'object')
      
    if self.labeled_features:
      if 'list' in str(type(self.labeled_features)):
        labeled_data = features.iloc[:, self.labeled_features]
        numeric_data = numeric_data.drop(labeled_data.columns, axis = 1)
        categorical_data = pd.concat([categorical_data, labeled_data], axis = 1)
      else:
        raise TypeError('labeled_feature values must be in a list')
    if self.all_labeled:
      labeled_columns = []
      for i in numeric_data.columns:
        if numeric_data[i].nunique() <= self.unique_threshold:
          if numeric_data[i].nunique() <= 2:
            if numeric_data[i].nunique() == 2:
              unique_values = numeric_data[i].unique()
              if not (0 in unique_values and 1 in unique_values):
                labeled_columns.append(i)
            else:
              #useless column all values are same
              numeric_data.drop([i], axis = 1)
          else:
            labeled_columns.append(i)
      #print(numeric_data[labeled_columns])
      categorical_data = pd.concat([categorical_data, numeric_data[labeled_columns]], axis = 1) 
      numeric_data = numeric_data.drop(labeled_columns, axis = 1)
    
    return categorical_data, numeric_data
  
  #combine data
  def combined_dataset(self, categorical_ohe, numeric_data):
    import numpy as np
    import pandas as pd
    #combine categorical_ohe and numeric columns
    ohe_data = np.concatenate([categorical_ohe, numeric_data], axis = 1)
    if self.return_dataframe:
      ohe_data = pd.DataFrame(ohe_data, columns = self.sorted_unique_values + numeric_data.columns.tolist())
    return ohe_data
    
  def fit_transform(self, features):
    '''fit transofrm dataframe into OneHotEncoded dataframe or numpy array
    fit_transfrom(features)
    
    features = a dataframe contaning any datatype
    
    '''
    from sklearn.preprocessing import OneHotEncoder
    import numpy as np
    import pandas as pd
    categorical_data, numeric_data = self.separate_data(features)
    categorical_ohe = None
    #get columns name for OneHotEncoded Dataframe
    for i in categorical_data.columns:
      if self.return_dataframe:
        sorted_u_values = sorted(categorical_data[i].unique())
        if self.drop_first:
          sorted_u_values = sorted_u_values[1:]
        sorted_u_values = [i + '_' + str(j) for j in sorted_u_values]
        self.sorted_unique_values += sorted_u_values
      ohe = OneHotEncoder(handle_unknown = 'ignore', sparse = False)
      encoded_columns = ohe.fit_transform(categorical_data[[i]].values)
      if self.drop_first:
        encoded_columns = encoded_columns[:, 1:]
      self.ohe_encoders[i] = ohe
      if str(type(categorical_ohe)) in "<class 'numpy.ndarray'>":
        categorical_ohe = np.concatenate([categorical_ohe, encoded_columns], axis = 1)
      else:
        categorical_ohe = encoded_columns
    return self.combined_dataset(categorical_ohe, numeric_data)
  
  #transform data
  def transform(self, features):
    '''features must be an dataframe
    it requires an argument features which is a dataframe containing numeric and categorical columns'''
    from sklearn.preprocessing import OneHotEncoder
    import numpy as np
    import pandas as pd
    categorical_data, numeric_data = self.separate_data(features)
    categorical_ohe = None
    for i in categorical_data.columns:
      encoded_columns = self.ohe_encoders[i].transform(categorical_data[[i]].values)
      if self.drop_first:
        encoded_columns = encoded_columns[:, 1:]
      
      if str(type(categorical_ohe)) in "<class 'numpy.ndarray'>":
        categorical_ohe = np.concatenate([categorical_ohe, encoded_columns], axis = 1)
      else:
        categorical_ohe = encoded_columns
        
    return self.combined_dataset(categorical_ohe, numeric_data)
