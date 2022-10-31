# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/losses.pytorch.ipynb.

# %% auto 0
__all__ = ['MAE', 'MSE', 'RMSE', 'MAPE', 'SMAPE', 'MASE', 'QuantileLoss', 'MQLoss', 'wMQLoss', 'PMM', 'GMM']

# %% ../../nbs/losses.pytorch.ipynb 3
import math
import numpy as np
import torch

# %% ../../nbs/losses.pytorch.ipynb 5
def _divide_no_nan(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Auxiliary funtion to handle divide by 0
    """
    div = a / b
    div[div != div] = 0.0
    div[div == float('inf')] = 0.0
    return div

# %% ../../nbs/losses.pytorch.ipynb 8
class MAE(torch.nn.Module):
    
    def __init__(self):
        """Mean Absolute Error

        Calculates Mean Absolute Error between
        `y` and `y_hat`. MAE measures the relative prediction
        accuracy of a forecasting method by calculating the
        deviation of the prediction and the true
        value at a given time and averages these devations
        over the length of the series.
        
        $$ \mathrm{MAE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} |y_{\\tau} - \hat{y}_{\\tau}| $$
        """
        super(MAE, self).__init__()
        self.outputsize_multiplier = 1
        self.output_names = ['']
        
    def adapt_output(self, y_pred):
        return y_pred

    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>
        
        **Returns:**<br>
        `mae`: tensor (single value).
        """
        if mask is None:
            mask = torch.ones_like(y)

        mae = torch.abs(y - y_hat) * mask
        mae = torch.mean(mae)
        return mae

# %% ../../nbs/losses.pytorch.ipynb 13
class MSE(torch.nn.Module):
    
    def __init__(self):
        """  Mean Squared Error

        Calculates Mean Squared Error between
        `y` and `y_hat`. MSE measures the relative prediction
        accuracy of a forecasting method by calculating the 
        squared deviation of the prediction and the true
        value at a given time, and averages these devations
        over the length of the series.
        
        $$ \mathrm{MSE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} (y_{\\tau} - \hat{y}_{\\tau})^{2} $$
        """
        super(MSE, self).__init__()
        self.outputsize_multiplier = 1
        self.output_names = ['']
        
    def adapt_output(self, y_pred):
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mse`: tensor (single value).
        """
        if mask is None:
            mask = torch.ones_like(y_hat)

        mse = (y - y_hat)**2
        mse = mask * mse
        mse = torch.mean(mse)
        return mse

# %% ../../nbs/losses.pytorch.ipynb 18
class RMSE(torch.nn.Module):
    
    def __init__(self):
        """ Root Mean Squared Error

        Calculates Root Mean Squared Error between
        `y` and `y_hat`. RMSE measures the relative prediction
        accuracy of a forecasting method by calculating the squared deviation
        of the prediction and the observed value at a given time and
        averages these devations over the length of the series.
        Finally the RMSE will be in the same scale
        as the original time series so its comparison with other
        series is possible only if they share a common scale. 
        RMSE has a direct connection to the L2 norm.
        
        $$ \mathrm{RMSE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = \\sqrt{\\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} (y_{\\tau} - \hat{y}_{\\tau})^{2}} $$
        """
        super(RMSE, self).__init__()
        self.outputsize_multiplier = 1
        self.output_names = ['']
        
    def adapt_output(self, y_pred):
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `rmse`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        mse = (y - y_hat)**2
        mse = mask * mse
        mse = torch.mean(mse)
        mse = torch.sqrt(mse)
        return mse

# %% ../../nbs/losses.pytorch.ipynb 24
class MAPE(torch.nn.Module):
    
    def __init__(self):
        """ Mean Absolute Percentage Error

        Calculates Mean Absolute Percentage Error  between
        `y` and `y_hat`. MAPE measures the relative prediction
        accuracy of a forecasting method by calculating the percentual deviation
        of the prediction and the observed value at a given time and
        averages these devations over the length of the series.
        The closer to zero an observed value is, the higher penalty MAPE loss
        assigns to the corresponding error.
        
        $$ \mathrm{MAPE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{|y_{\\tau}|} $$
        """
        super(MAPE, self).__init__()
        self.outputsize_multiplier = 1
        self.output_names = ['']
        
    def adapt_output(self, y_pred):
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mape`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        mask = _divide_no_nan(mask, torch.abs(y))
        mape = torch.abs(y - y_hat) * mask
        mape = torch.mean(mape)
        return mape

# %% ../../nbs/losses.pytorch.ipynb 29
class SMAPE(torch.nn.Module):
    def __init__(self):
        """ Symmetric Mean Absolute Percentage Error
        
        Calculates Symmetric Mean Absolute Percentage Error between
        `y` and `y_hat`. SMAPE measures the relative prediction
        accuracy of a forecasting method by calculating the relative deviation
        of the prediction and the observed value scaled by the sum of the
        absolute values for the prediction and observed value at a
        given time, then averages these devations over the length
        of the series. This allows the SMAPE to have bounds between
        0% and 200% which is desireble compared to normal MAPE that
        may be undetermined when the target is zero.
        
        $$ \mathrm{sMAPE}_{2}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{|y_{\\tau}|+|\hat{y}_{\\tau}|} $$
        
        **References:**<br>
        [Makridakis S., "Accuracy measures: theoretical and practical concerns".](https://www.sciencedirect.com/science/article/pii/0169207093900793)
        """
        super(SMAPE, self).__init__()
        self.outputsize_multiplier = 1
        self.output_names = ['']
        
    def adapt_output(self, y_pred):
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `smape`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        delta_y = torch.abs((y - y_hat))
        scale = torch.abs(y) + torch.abs(y_hat)
        smape = _divide_no_nan(delta_y, scale)
        smape = smape * mask
        smape = 2 * torch.mean(smape)
        return smape

# %% ../../nbs/losses.pytorch.ipynb 34
class MASE(torch.nn.Module):

    def __init__(self, seasonality: int):
        """ Mean Absolute Scaled Error 
        Calculates the Mean Absolute Scaled Error between
        `y` and `y_hat`. MASE measures the relative prediction
        accuracy of a forecasting method by comparinng the mean absolute errors
        of the prediction and the observed value against the mean
        absolute errors of the seasonal naive model.
        The MASE partially composed the Overall Weighted Average (OWA), 
        used in the M4 Competition.
        
        $$ \mathrm{MASE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}, \\mathbf{\hat{y}}^{season}_{\\tau}) = \\frac{1}{H} \sum^{t+H}_{\\tau=t+1} \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{\mathrm{MAE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{season}_{\\tau})} $$

        **Parameters:**<br>
        `seasonality`: int. Main frequency of the time series; Hourly 24,  Daily 7, Weekly 52, Monthly 12, Quarterly 4, Yearly 1.
        
        **References:**<br>
        [Rob J. Hyndman, & Koehler, A. B. "Another look at measures of forecast accuracy".](https://www.sciencedirect.com/science/article/pii/S0169207006000239)<br>
        [Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, "The M4 Competition: 100,000 time series and 61 forecasting methods".](https://www.sciencedirect.com/science/article/pii/S0169207019301128)
        """
        super(MASE, self).__init__()
        self.seasonality = seasonality
        self.outputsize_multiplier = 1
        self.output_names = ['']
        
    def adapt_output(self, y_pred):
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor,  y_insample: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor (batch_size, output_size), Actual values.<br>
        `y_hat`: tensor (batch_size, output_size)), Predicted values.<br>
        `y_insample`: tensor (batch_size, input_size), Actual insample Seasonal Naive predictions.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mase`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        delta_y = torch.abs(y - y_hat)
        scale = torch.mean(torch.abs(y_insample[:, self.seasonality:] - \
                                     y_insample[:, :-self.seasonality]), axis=1)
        mase = _divide_no_nan(delta_y, scale[:, None])
        mase = mase * mask
        mase = torch.mean(mase)
        return mase

# %% ../../nbs/losses.pytorch.ipynb 40
class QuantileLoss(torch.nn.Module):
    
    def __init__(self, q):
        """ Quantile Loss

        Computes the quantile loss between `y` and `y_hat`.
        QL measures the deviation of a quantile forecast.
        By weighting the absolute deviation in a non symmetric way, the
        loss pays more attention to under or over estimation.
        A common value for q is 0.5 for the deviation from the median (Pinball loss).

        $$ \mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q)}_{\\tau}) = \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} \Big( (1-q)\,( \hat{y}^{(q)}_{\\tau} - y_{\\tau} )_{+} + q\,( y_{\\tau} - \hat{y}^{(q)}_{\\tau} )_{+} \Big) $$

        **Parameters:**<br>
        `q`: float, between 0 and 1. The slope of the quantile loss, in the context of quantile regression, the q determines the conditional quantile level.<br>

        **References:**<br>
        [Roger Koenker and Gilbert Bassett, Jr., "Regression Quantiles".](https://www.jstor.org/stable/1913643)
        """
        super(QuantileLoss, self).__init__()
        self.q = q
        self.outputsize_multiplier = 1
        self.output_names = [f'_ql{q}']
        
    def adapt_output(self, y_pred):
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `quantile_loss`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        delta_y = y - y_hat
        loss = torch.max(torch.mul(self.q, delta_y), torch.mul((self.q - 1), delta_y))
        loss = loss * mask
        quantile_loss = torch.mean(loss)
        return quantile_loss

# %% ../../nbs/losses.pytorch.ipynb 45
def level_to_outputs(level):
    qs = sum([[50-l/2, 50+l/2] for l in level], [])
    output_names = sum([[f'-lo-{l}', f'-hi-{l}'] for l in level], [])

    sort_idx = np.argsort(qs)
    quantiles = np.array(qs)[sort_idx]

    # Add default median
    quantiles = np.concatenate([np.array([50]), quantiles])
    quantiles = torch.Tensor(quantiles) / 100
    output_names = list(np.array(output_names)[sort_idx])
    output_names.insert(0, '-median')
    
    return quantiles, output_names

def quantiles_to_outputs(quantiles):
    output_names = []
    for q in quantiles:
        if q<.50:
            output_names.append(f'-lo-{np.round(100-200*q,2)}')
        elif q>.50:
            output_names.append(f'-hi-{np.round(100-200*(1-q),2)}')
        else:
            output_names.append('-median')
    return quantiles, output_names

# %% ../../nbs/losses.pytorch.ipynb 46
class MQLoss(torch.nn.Module):
    
    def __init__(self, level=[80, 90], quantiles=None):
        """  Multi-Quantile loss
    
        Calculates the Multi-Quantile loss (MQL) between `y` and `y_hat`.
        MQL calculates the average multi-quantile Loss for
        a given set of quantiles, based on the absolute 
        difference between predicted quantiles and observed values.
        
        $$ \mathrm{MQL}(\\mathbf{y}_{\\tau},[\\mathbf{\hat{y}}^{(q_{1})}_{\\tau}, ... ,\hat{y}^{(q_{n})}_{\\tau}]) = \\frac{1}{n} \\sum_{q_{i}} \mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q_{i})}_{\\tau}) $$
        
        The limit behavior of MQL allows to measure the accuracy 
        of a full predictive distribution $\mathbf{\hat{F}}_{\\tau}$ with 
        the continuous ranked probability score (CRPS). This can be achieved 
        through a numerical integration technique, that discretizes the quantiles 
        and treats the CRPS integral with a left Riemann approximation, averaging over 
        uniformly distanced quantiles.    
        
        $$ \mathrm{CRPS}(y_{\\tau}, \mathbf{\hat{F}}_{\\tau}) = \int^{1}_{0} \mathrm{QL}(y_{\\tau}, \hat{y}^{(q)}_{\\tau}) dq $$

        **Parameters:**<br>
        `level`: int list [0,100]. Probability levels for prediction intervals (Defaults median).
        `quantiles`: float list [0., 1.]. Alternative to level, quantiles to estimate from y distribution.

        **References:**<br>
        [Roger Koenker and Gilbert Bassett, Jr., "Regression Quantiles".](https://www.jstor.org/stable/1913643)<br>
        [James E. Matheson and Robert L. Winkler, "Scoring Rules for Continuous Probability Distributions".](https://www.jstor.org/stable/2629907)
        """
        super(MQLoss, self).__init__()
        # Transform level to MQLoss parameters
        if level:
            qs, self.output_names = level_to_outputs(level)
            quantiles = torch.Tensor(qs)

        # Transform quantiles to homogeneus output names
        if quantiles is not None:
            _, self.output_names = quantiles_to_outputs(quantiles)
            quantiles = torch.Tensor(quantiles)

        self.quantiles = torch.nn.Parameter(quantiles, requires_grad=False)
        self.outputsize_multiplier = len(self.output_names)

    def adapt_output(self, y_pred):
        # Model output is adapted to have quantiles in the last dim
        all_but_last_dims = y_pred.size()[:-1]
        last_dim = y_pred.size()[-1]
        y_pred = y_pred.view(*all_but_last_dims, 
                             last_dim//self.outputsize_multiplier,
                             self.outputsize_multiplier)
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mqloss`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        n_q = len(self.quantiles)
        
        error  = y_hat - y.unsqueeze(-1)
        sq     = torch.maximum(-error, torch.zeros_like(error))
        s1_q   = torch.maximum(error, torch.zeros_like(error))
        mqloss = (self.quantiles * sq + (1 - self.quantiles) * s1_q)
            
        # Match y/weights dimensions and compute weighted average
        mask = mask / torch.sum(mask)
        mask = mask.unsqueeze(-1)
        mqloss = (1/n_q) * mqloss * mask
        return torch.sum(mqloss)

# %% ../../nbs/losses.pytorch.ipynb 51
class wMQLoss(torch.nn.Module):
    
    def __init__(self, level=[80, 90], quantiles=None):
        """ Weighted Multi-Quantile loss
        
        Calculates the Weighted Multi-Quantile loss (WMQL) between `y` and `y_hat`.
        WMQL calculates the weighted average multi-quantile Loss for
        a given set of quantiles, based on the absolute 
        difference between predicted quantiles and observed values.  
            
        $$ \mathrm{wMQL}(\\mathbf{y}_{\\tau},[\\mathbf{\hat{y}}^{(q_{1})}_{\\tau}, ... ,\hat{y}^{(q_{n})}_{\\tau}]) = \\frac{1}{n} \\sum_{q_{i}} \\frac{\mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q_{i})}_{\\tau})}{\\sum^{t+H}_{\\tau=t+1} |y_{\\tau}|} $$
        
        **Parameters:**<br>
        `level`: int list [0,100]. Probability levels for prediction intervals (Defaults median).
        `quantiles`: float list [0., 1.]. Alternative to level, quantiles to estimate from y distribution.

        **References:**<br>
        [Roger Koenker and Gilbert Bassett, Jr., "Regression Quantiles".](https://www.jstor.org/stable/1913643)<br>
        [James E. Matheson and Robert L. Winkler, "Scoring Rules for Continuous Probability Distributions".](https://www.jstor.org/stable/2629907)
        """
        super(wMQLoss, self).__init__()
        # Transform level to MQLoss parameters
        if level:
            qs, self.output_names = level_to_outputs(level)
            quantiles = torch.Tensor(qs)

        # Transform quantiles to homogeneus output names
        if quantiles is not None:
            _, self.output_names = quantiles_to_outputs(quantiles)
            quantiles = torch.Tensor(quantiles)

        self.quantiles = torch.nn.Parameter(quantiles, requires_grad=False)
        self.outputsize_multiplier = len(self.output_names)

    def adapt_output(self, y_pred):
        # Model output is adapted to have quantiles in the last dim
        all_but_last_dims = y_pred.size()[:-1]
        last_dim = y_pred.size()[-1]
        y_pred = y_pred.view(*all_but_last_dims, 
                             last_dim//self.outputsize_multiplier,
                             self.outputsize_multiplier)
        return y_pred
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mqloss`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        error = y_hat - y.unsqueeze(-1)
        
        sq = torch.maximum(-error, torch.zeros_like(error))
        s1_q = torch.maximum(error, torch.zeros_like(error))
        loss = (self.quantiles * sq + (1 - self.quantiles) * s1_q)
        
        wmqloss = _divide_no_nan(torch.sum(loss * mask, axis=-2), 
                                 torch.sum(torch.abs(y.unsqueeze(-1)) * mask, axis=-2))
        return torch.mean(wmqloss)

# %% ../../nbs/losses.pytorch.ipynb 56
class PMM(torch.nn.Module):

    def __init__(self, level=[80, 90], quantiles=None):
        """ Poisson Mixture Mesh

        This Poisson Mixture statistical model assumes independence across groups of 
        data $\mathcal{G}=\{[g_{i}]\}$, and estimates relationships within the group.

        $$ P\\left(\mathbf{y}_{[b][t+1:t+H]}\\right) = 
        \prod_{ [g_{i}] \in \mathcal{G}} P \\left(\mathbf{y}_{[g_{i}][\\tau]} \\right) =
        \prod_{\\beta\in[g_{i}]} 
        \\left(\sum_{k=1}^{K} w_k \prod_{(\\beta,\\tau) \in [g_i][t+1:t+H]} \mathrm{Poisson}(y_{\\beta,\\tau}, \hat{\\lambda}_{\\beta,\\tau,k}) \\right)$$

        **References:**<br>
        [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan Reddy, Mengfei Cao, Lee Dicker. 
        Probabilistic Hierarchical Forecasting with Deep Poisson Mixtures. Submitted to the International 
        Journal Forecasting, Working paper available at arxiv.](https://arxiv.org/pdf/2110.13179.pdf)
        """
        super(PMM, self).__init__()
        # Transform level to MQLoss parameters
        if level:
            qs, self.output_names = level_to_outputs(level)
            quantiles = torch.Tensor(qs)

        # Transform quantiles to homogeneus output names
        if quantiles is not None:
            _, self.output_names = quantiles_to_outputs(quantiles)
            quantiles = torch.Tensor(quantiles)

        self.quantiles = torch.nn.Parameter(quantiles, requires_grad=False)
        self.outputsize_multiplier = len(self.output_names)

    def sample(self, weights, lambdas, num_samples=500):        
        B, H, K = lambdas.size()
        Q = len(self.quantiles)

        # Sample K ~ Mult(weights)
        # shared across B, H
        weights = torch.repeat_interleave(input=weights, repeats=H, dim=2)

        # Avoid loop, vectorize
        weights = weights.reshape(-1, K)
        lambdas = lambdas.flatten()        

        # Vectorization trick to recover row_idx
        sample_idxs = torch.multinomial(input=weights, 
                                        num_samples=num_samples,
                                        replacement=True)
        aux_col_idx = torch.unsqueeze(torch.arange(B*H),-1) * K

        # To device
        sample_idxs = sample_idxs.to(lambdas.device)
        aux_col_idx = aux_col_idx.to(lambdas.device)

        sample_idxs = sample_idxs + aux_col_idx
        sample_idxs = sample_idxs.flatten()

        sample_lambdas = lambdas[sample_idxs]

        # Sample y ~ Poisson(lambda) independently
        samples = torch.poisson(sample_lambdas).to(lambdas.device)
        samples = samples.view(B*H, num_samples)

        # Compute quantiles
        quantiles_device = self.quantiles.to(lambdas.device)
        quants = torch.quantile(input=samples, q=quantiles_device, dim=1)
        quants = quants.permute((1,0)) # Q, B*H

        # Final reshapes
        samples = samples.view(B, H, num_samples)
        quants  = quants.view(B, H, Q)

        return samples, quants        
    
    def neglog_likelihood(self,
                          y: torch.Tensor,
                          weights: torch.Tensor,
                          lambdas: torch.Tensor,
                          mask: torch.Tensor=None):

        if mask is None: 
            mask = torch.ones_like(y)

        B, H, K = lambdas.size()
        eps  = 1e-10
        
        log = y * torch.log(lambdas + eps) - lambdas\
              - ( (y) * torch.log(y + eps) - y )   # Stirling's Factorial

        #log  = torch.sum(log, dim=0, keepdim=True) # Joint within batch/group
        #log  = torch.sum(log, dim=1, keepdim=True) # Joint within horizon
        
        # Numerical stability mixture and loglik
        log_max = torch.amax(log, dim=2, keepdim=True) # [1,1,K] (collapsed joints)
        lik     = weights * torch.exp(log-log_max)     # Take max
        loglik  = torch.log(torch.sum(lik, dim=2, keepdim=True)) + log_max # Return max
        loglik  = loglik * mask #replace with mask
        
        loss = -torch.mean(loglik)
        return loss
    
    def __call__(self, y: torch.Tensor,
                 weights: torch.Tensor,
                 lambdas: torch.Tensor,
                 mask: torch.Tensor=None):
        
        return self.neglog_likelihood(y=y, weights=weights, lambdas=lambdas, mask=mask)


# %% ../../nbs/losses.pytorch.ipynb 60
class GMM(torch.nn.Module):

    def __init__(self, level=[80, 90], quantiles=None):
        """ Gaussian Mixture Mesh

        This Gaussian Mixture statistical model assumes independence across groups of 
        data $\mathcal{G}=\{[g_{i}]\}$, and estimates relationships within the group.

        $$ P\\left(\mathbf{y}_{[b][t+1:t+H]}\\right) = 
        \prod_{ [g_{i}] \in \mathcal{G}} P\left(\mathbf{y}_{[g_{i}][\\tau]}\\right)=
        \prod_{\\beta\in[g_{i}]}
        \\left(\sum_{k=1}^{K} w_k \prod_{(\\beta,\\tau) \in [g_i][t+1:t+H]} 
        \mathrm{Gaussian}(y_{\\beta,\\tau}, \hat{\mu}_{\\beta,\\tau,k}, \sigma_{\\beta,\\tau,k})\\right)$$

        **References:**<br>
        [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan Reddy, Mengfei Cao, Lee Dicker. 
        Probabilistic Hierarchical Forecasting with Deep Poisson Mixtures. Submitted to the International 
        Journal Forecasting, Working paper available at arxiv.](https://arxiv.org/pdf/2110.13179.pdf)
        """
        super(GMM, self).__init__()
        # Transform level to MQLoss parameters
        if level:
            qs, self.output_names = level_to_outputs(level)
            quantiles = torch.Tensor(qs)

        # Transform quantiles to homogeneus output names
        if quantiles is not None:
            _, self.output_names = quantiles_to_outputs(quantiles)
            quantiles = torch.Tensor(quantiles)

        self.quantiles = torch.nn.Parameter(quantiles, requires_grad=False)
        self.outputsize_multiplier = len(self.output_names)

    def sample(self, weights, means, stds, num_samples=500):
        B, H, K = means.size()
        Q = len(self.quantiles)
        assert means.shape == stds.shape

        # Sample K ~ Mult(weights)
        # shared across B, H
        # weights = torch.repeat_interleave(input=weights, repeats=H, dim=2)

        # Avoid loop, vectorize
        weights = weights.reshape(-1, K)
        means = means.flatten()
        stds = stds.flatten()

        # Vectorization trick to recover row_idx
        sample_idxs = torch.multinomial(input=weights, 
                                        num_samples=num_samples,
                                        replacement=True)
        aux_col_idx = torch.unsqueeze(torch.arange(B*H),-1) * K

        # To device
        sample_idxs = sample_idxs.to(means.device)
        aux_col_idx = aux_col_idx.to(means.device)

        sample_idxs = sample_idxs + aux_col_idx
        sample_idxs = sample_idxs.flatten()

        sample_means = means[sample_idxs]
        sample_stds  = stds[sample_idxs]

        # Sample y ~ Normal(mu, std) independently
        samples = torch.normal(sample_means, sample_stds).to(means.device)
        samples = samples.view(B*H, num_samples)

        # Compute quantiles
        quantiles_device = self.quantiles.to(means.device)
        quants = torch.quantile(input=samples, q=quantiles_device, dim=1)
        quants = quants.permute((1,0)) # Q, B*H

        # Final reshapes
        samples = samples.view(B, H, num_samples)
        quants  = quants.view(B, H, Q)

        return samples, quants        
    
    def neglog_likelihood(self,
                          y: torch.Tensor,
                          weights: torch.Tensor,
                          means: torch.Tensor,
                          stds: torch.Tensor,
                          mask: torch.Tensor=None):

        if mask is None: 
            mask = torch.ones_like(means)

        B, H, K = means.size()
        # eps  = 1e-10
        
        log  = -0.5 * ((1/stds)*(y - means))**2\
                - torch.log(((2*math.pi)**(0.5)) * stds)

        #log  = torch.sum(log, dim=0, keepdim=True) # Joint within batch/group
        #log  = torch.sum(log, dim=1, keepdim=True) # Joint within horizon

        # Numerical stability mixture and loglik
        log_max = torch.amax(log, dim=2, keepdim=True) # [1,1,K] (collapsed joints)
        lik     = weights * torch.exp(log-log_max)     # Take max
        loglik  = torch.log(torch.sum(lik, dim=2, keepdim=True)) + log_max # Return max
        
        loglik  = loglik * mask #replace with mask

        loss = -torch.mean(loglik)
        return loss
    
    def __call__(self, y: torch.Tensor,
                 weights: torch.Tensor,
                 means: torch.Tensor,
                 stds: torch.Tensor,
                 mask: torch.Tensor=None):

        return self.neglog_likelihood(y=y, weights=weights,
                                 means=means, stds=stds, mask=mask)
