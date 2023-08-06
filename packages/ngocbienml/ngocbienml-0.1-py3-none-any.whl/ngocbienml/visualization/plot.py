import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os
from ..utils.config import picture_path
#from model import Model


class Plot:
    def __init__(self, **kwargs):
        #self.__init__(Model)
        self.name = kwargs['name']
        self.model = kwargs['model']
        self.feature_importance = None
        try:
            self.feature_name = kwargs['feature_name']
        except KeyError:
            self.feature_name = None
        self.args = kwargs
        self.max_feat = 50
        self.color = ['green', 'orange', 'purple', 'blue']

    def get_parameters(self):

        if self.name=='lgb_model':
            self.feature_importance=self.model.feature_importance()
            self.feature_name=self.model.feature_name()
        else:
            feat_name_key=[key for key in self.args.keys() if 'feat' in key and 'name' in key]
            assert len(feat_name_key)==1
            self.feature_name=self.args[feat_name_key[0]]

        if self.name=='lgb_classifier' or self.name=='lgb':
            self.feature_importance=self.model.feature_importances_
        elif self.name=='RF':
            self.feature_importance=self.model.feature_importances_

    def simple_plot(self):

        self.get_parameters()
        dfx=pd.Series(self.feature_importance,index=self.feature_name)
        dfx=dfx.sort_values(ascending=False)
        if len(dfx)>self.max_feat:
            dfx=dfx.iloc[:self.max_feat]
        dfx.plot.bar(figsize=(12,4),color=self.color)
        plt.title('feat importance')
        plt.show()
        path=self.get_path()
        if path is not None:
            plt.savefig(path)

    def plot_lgb(self):

        if 'lgb' in self.args.keys():
            lgb=self.args['lgb']
            ax=lgb.plot_importance(self.model,figsize=(6,8),\
                                   importance_type='gain',\
                                   max_num_features=40,
                                   height=.8,
                                   color=self.color,
                                   grid=False,
                                   )
            plt.sca(ax)
            plt.xticks([],[])
            plt.title('lgb model gain importance')
            plt.show()
        else:
            pass


    def get_path(self):

        if  os.path.isdir(picture_path):
            now=datetime.now()
            current_time=now.strftime("%d %m %y %H %M")  # will add this time to the name of file distinct them
            path = picture_path+current_time+'_picture.png'
            return path
        else:
            return None

    def plot_metric(self):

        if 'lgb' in self.args.keys():
            lgb=self.args['lgb']
            ax=lgb.plot_metric(self.model,figsize=(6,8))
            plt.show()
        else:
            pass

    def plot_metric_and_importance(self):

        if 'lgb' in self.args.keys():
            lgb = self.args['lgb']
            fig, ax = plt.subplots(2, 1)
            fig.subplots_adjust(hspace=.2)
            fig.set_figheight(6)
            fig.set_figwidth(14)
            lgb.plot_metric(self.model, ax=ax[0])
            booster = self.model.booster_  # case of classifier, we must to acces to booster_ instance
            dfx = pd.DataFrame(index=booster.feature_name())
            dfx['gain'] = booster.feature_importance('gain')
            dfx['gain'] = dfx['gain']/dfx.gain.max()
            dfx['split'] = booster.feature_importance('split')
            dfx['split'] = dfx['split']/dfx.split.max()
            dfx = dfx.sort_values('gain', ascending=False).iloc[:self.max_feat]
            dfx.plot.bar(width=0.9, ax=ax[1])
            plt.subplots_adjust(left=None, bottom=.5, right=None, top=None, wspace=None, hspace=None)
            path = self.get_path()
            if path is not None:
                #print('save picture to file')
                plt.savefig(path)
            plt.show()
        else:
            print('nothing to plot')
            pass

    def plot_booster_lgb(self):

        booster = self.model.booster_  # case of classifier, we must to acces to booster_ instance
        dfx = pd.DataFrame(index=lgb.feature_name())
        dfx['gain']=booster.feature_importance('gain')
        dfx['gain']=dfx['gain']/dfx.gain.max()
        dfx['split']=booster.feature_importance('split')
        dfx['split']=dfx['split']/dfx.split.max()
        dfx=dfx.sort_values('split',ascending=False).iloc[:self.max_feat]
        dfx.plot.bar(width=0.9,figsize=(12,3))
        plt.show()
        path = self.get_path()
        if path is not None:
            plt.savefig(path)

    def plot_rf_or_lr(self):
        if self.name.strip().lower() == 'lr':
            feature_importance = abs(self.model.coef_[0])
        elif self.name.strip().lower() == 'rf':
            feature_importance = self.model.feature_importances_
        else:
            return self
        plt.figure(figsize=(13, 4))
        #print('feat name=')
        #print(self.feature_name)
        df = pd.Series(feature_importance, index=self.feature_name).sort_values(ascending=False).iloc[:self.max_feat]
        #print(df)
        plt.bar(range(len(df)), df, color=self.color)
        plt.xticks(range(len(df)), df.index, rotation=90)
        plt.title('Feature Importance Of %s Model'%(self.name.upper()), fontsize=16)
        plt.subplots_adjust(left=None, bottom=.5, right=None, top=None, wspace=None, hspace=None)
        plt.show()
