##
# A small library of functions that wrap the rugarch package
# this lib exposes functions on rugarch::ugarchfit and rugarch::ugarchsim
#

# fit an ARMA-GARCH model
#
# Args:
#   series: the target time series to fit
#   spec: a rugarch::ugarchspec
fit_model <- function(series, spec)
{
    model <- rugarch::ugarchfit(spec=spec, data=series, solver = 'hybrid')
    converged <- !(is.null(model) || model@fit$solver$sol$convergence != 0)
    return(c(model, converged))
}


# simulate paths from the ARMA-GARCH model
#
# Args:
#   model: a handle to the rugarch::ugarchfit
#   len_sim: the number of days in one simulation
#   num_sims: the number of simulations
#   extregsims: a dataframe with simulations of the external
#               regressors (should be same length as len_sim)
simulate_model <- function(model, len_sim, num_sims, extregsims)
{
    if (!is.null(extregsims)) {
        extregsims  <- as.matrix(extregsims)
        reg_list <- list()
        for (i in 1:num_sims) {
            reg_list[[i]] <- extregsims
        }
        sims <- rugarch::ugarchsim(
          model, n.sim=len_sim, m.sim=num_sims, mexsimdata=reg_list
        )
    }
    else {
        sims <- rugarch::ugarchsim(model, n.sim=len_sim, m.sim=num_sims)
    }
    sims <- as.data.frame(fitted(sims))
    names(sims) <- paste0('V', seq_len(num_sims))
    return(sims)
}


# compute the Akaike Information Criteria
#
# Args:
#   model: a handle to a rugarch::ugarchfit
calc_aic <- function(model, series)
{
    return(rugarch::infocriteria(model)[1] * length(series))
}


# return summary of model fit
#
# Args:
#   model: a handle to the rugarch::ugarchfit
get_model_summary <- function(model)
{
    tryCatch({
        return(capture.output(show(model)))
    }, error = function(e) {
        return('ARMA-GARCH fit with too few data points for summary statistics')
    })
}


# return residuals of the model fit
#
# Args:
#   model: a handle to the rugarch::ugarchfit
get_residuals <- function(model)
{
    return(residuals(model))
}


# return the fitted values
#
# Args:
#   model: a handle to the rugarch::ugarchfit
get_fitted_values <- function(model)
{
    return(fitted(model))
}


# return the fitted GARCH volatilities
#
# Args:
#   model: a handle to the rugarch::ugarchfit
get_volatilities <- function(model)
{
    return(sigma(model))
}
