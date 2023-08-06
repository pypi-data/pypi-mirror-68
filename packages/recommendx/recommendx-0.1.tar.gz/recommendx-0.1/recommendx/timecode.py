import numpy as np
import pandas as pd

__all__ = ['RWT']

class RWT:
    
    def __init__(self, reg = 0.02, lr = 0.005, n_epochs = 100, n_factors = 50,
                init_mean = 0, init_std_dev = 0.01):
        self.reg = reg
        self.lr = lr
        self.n_epochs = n_epochs
        self.n_factors = n_factors
        self.init_mean = init_mean
        self.init_std_dev = init_std_dev
        
        self.intercept_ = None
        self.B = None
        self.bu = None
        self.alpha_ = None
        self.Z = None
        self.X = None
        self.n_users = None
        self.n_items = None
        self.n_Xs = None
        self.R = None
        self.userdict = None
        self.itemdict = None
        self.timedict = None
        self.n_times = None
        
    def fit(self, df, Xi = None):
        '''Perform stochastic gradient descent       
        Arguments:
        df: NumPy array with four columns [user, item, rating, time category]
        Xi: NumPy array with 1 row per item and 1 + n_Xs columns (= None if no regressors)
            First column of Xi is item ID
        '''
        
        # Begin by creating zero-indexed labels for user and item
        useru = pd.Series(df[:,0]).astype('category')
        itemui = pd.Series(df[:,1]).astype('category')
        timeui = pd.Series(df[:,3]).astype('category')
        newdf = np.column_stack((useru.cat.codes, itemui.cat.codes, df[:,2], timeui.cat.codes))
                                
        # Assign values from data
        self.n_users = len(np.unique(newdf[:,0]))   # Number of users
        self.R = newdf.shape[0]    # Total number of ratings
        self.n_items = len(np.unique(newdf[:,1]))   # Number of items
        self.n_times = len(np.unique(newdf[:,3]))   # Number of time periods
        
        # Create a user and item dictionary to recover values
        self.userdict = np.column_stack((useru.cat.categories, range(0,self.n_users)))
        self.itemdict = np.column_stack((itemui.cat.categories, range(0,self.n_items)))
        self.timedict = np.column_stack((timeui.cat.categories, range(0,self.n_times)))
        
        # Initialize the necessary parameter values
        self.intercept_ = sum(newdf[:,2])/self.R
        self.bu = np.zeros((self.n_users, 1))
        self.alpha_ = self.init_mean + self.init_std_dev*np.random.randn(self.n_times, self.n_users, self.n_factors)
        self.Z = self.init_mean + self.init_std_dev*np.random.randn(self.n_items, self.n_factors)
        
        if Xi is not None:
            self.n_Xs = Xi.shape[1] - 1
            self.B = self.init_mean + self.init_std_dev*np.random.randn(self.n_times, self.n_users, self.n_Xs)
        
        # Fit the model with observed regressors
        if Xi is not None:
            self.X = Xi[:,1:]
            for _ in range(self.n_epochs):
                for u, i, r_ui, t in newdf:
                    err = r_ui - self.intercept_ - self.bu[u] - np.dot(self.B[t, u, :],self.X[i]) - self.alpha_[t,u,:] @ np.transpose(self.Z[i])
                    # Update bu
                    self.bu[u] += self.lr*(err - self.reg*self.bu[u])
                    # Update B
                    self.B[t,u,:] = self.B[t,u,:] + self.lr*(err*np.transpose(self.X[i]) - self.reg*self.B[t,u,:])
                    # Update alpha
                    self.alpha_[t,u,:] += self.lr*(err*self.Z[i] - self.reg*self.alpha_[t,u,:])
                    # Update Z
                    self.Z[i] += self.lr*(err*self.alpha_[t,u,:] - self.reg*self.Z[i])
        else:
            for _ in range(self.n_epochs):
                for u, i, r_ui, t in newdf:
                    err = r_ui - self.intercept_ - self.bu[u] - self.alpha_[t,u,:] @ np.transpose(self.Z[i])
                    # Update bu
                    self.bu[u] += self.lr*(err - self.reg*self.bu[u])
                    # Update alpha
                    self.alpha_[t,u,:] += self.lr*(err*self.Z[i] - self.reg*self.alpha_[t,u,:])
                    # Update Z
                    self.Z[i] += self.lr*(err*self.alpha_[t,u,:] - self.reg*self.Z[i])
        
    def accuracy(self, df, Xi = None):
        '''Calculates the mean squared prediction error of RWR fit       
        Arguments:
        df: NumPy array with three columns [user, item, rating]
        Xi: NumPy array with 1 row per item and 1 + n_Xs columns (= None if no regressors)
        First column of Xi is item ID
        Inputs are meant to match the fit inputs so that the user can evaulate training model
        
        Can only be called after fit has been called
        '''
        # Begin by creating zero-indexed labels for user and item
        useru = pd.Series(df[:,0]).astype('category')
        itemui = pd.Series(df[:,1]).astype('category')
        timeui = pd.Series(df[:,3]).astype('category')
        newdf = np.column_stack((useru.cat.codes, itemui.cat.codes, df[:,2], timeui.cat.codes))
        
        # Assign values from data -- local storage so do not reassign to self
        R = newdf.shape[0]    # Total number of ratings
        
        # Parameter values already assigned from fit
        
        if Xi is not None:
            n_Xs = Xi.shape[1] - 1
        
        # Calculate MSPE when regressors are included
        if Xi is not None:
            X = Xi[:,1:]
            # Loop over all the rows in newdf
            sume2 = 0
            for u, i, r_ui, t in newdf:
                # Calculate prediction error
                err = r_ui - self.intercept_ - self.bu[u] - np.dot(self.B[t,u,:],X[i]) - self.alpha_[t,u,:] @ np.transpose(self.Z[i])
                err2 = err**2
                sume2 = sume2 + err2
        else:
            # Loop over all the rows in newdf
            sume2 = 0
            for u, i, r_ui, t in newdf:
                # Calculate prediction error
                err = r_ui - self.intercept_ - self.bu[u] - self.alpha_[t,u,:] @ np.transpose(self.Z[i])
                err2 = err**2
                sume2 = sume2 + err2
        
        return sume2/R
    
    def predict(self, u_p, i_p, tee):
        '''This function predicts the rating user u_p assigns to item i_p in time period tee
    
        u_p, i_p, and tee are individual values so if you wish to use this for multiple predictions,
        you should create a loop
    
        u_p, i_p, and tee must be of the same type as the original data
    
        Regressor information has already defined as self.Xi if regressors were originally used    
        '''
        # First, find the index value for u_p and i_p
        indxu = np.where(self.userdict[:,0] == u_p)[0]
        indxi = np.where(self.itemdict[:,0] == i_p)[0]
        indxt = np.where(self.timedict[:,0] == tee)[0]
    
        # Use index values to find u and i
        u = self.userdict[indxu[0],1]
        i = self.itemdict[indxi[0],1]
        t = self.timedict[indxt[0],1]
    
        if self.X is not None:
            rhat = self.intercept_ + self.bu[u] + np.dot(self.B[t,u,:],self.X[i]) + self.alpha_[t,u,:] @ np.transpose(self.Z[i])
        else:
            rhat = self.intercept_ + self.bu[u] + self.alpha_[t,u,:] @ np.transpose(self.Z[i])
    
        return rhat