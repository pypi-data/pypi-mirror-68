
path1 = 'C:\\Users\\os_biennn\\Desktop\\bitbucket\\dmprepo\
\\dmprepo\\dmprepo\\source-code\\machine_learning\\ML_Python'
path2 = '\\income_prediction\\data\\dataset_gui_anhBien\\dataset_income\\'
path_month2 = path1+path2+'dataset_2Month.csv'
path_month3 = path1+path2+'dataset_3Month.csv'
picture_path = 'to_add_corect_path'
model_path = path1+'\\income_prediction_project\\data\\model\\'

params = {'feature_fraction': 0.7319044104939286,
          'max_depth': 65,
          'min_child_weight': 1e-05,
          'min_data_in_leaf': 47,
          'n_estimators': 497,
          'num_leaves': 45,
          'reg_alpha': 0,
          'reg_lambda': 50,
          'metric': 'auc',
          'eval_metric': 'auc',
          'subsample': 0.5380272330885912}


params = {
    'early_stopping_rounds': 100,
    'max_depth': 40,
    'random_state': 49,
    'metric': 'auc',
    'eval_metric': 'auc',
    'min_data': 100,
    'reg_alpha': 0.1,
    'min_data_in_leaf': 30,
    'feature_fraction': 0.8,
    'is_unbalance': True,
    'n_estimators': 500,
    'subsample': 0.9,
    'learning_rate': 0.05
}
