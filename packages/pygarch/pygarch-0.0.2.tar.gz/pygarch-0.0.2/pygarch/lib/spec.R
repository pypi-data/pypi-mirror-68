##
# A small library of functions that wrap the rugarch package
# this lib exposes functions on rugarch::ugarchspec
#

library(rugarch)


# return a rugarch::ugarchspec
#
# Args:
#   arma_order: a vector of length 2
#   garch_order: a vector of length 2
#   extregdata: a dataframe of external regressors
#   dist: distribution of errors ("norm" or "std")
#   dof: the degrees of freedom in the (Student-t) error model. If
#        left NULL the model selects the best dof
#   fixed_ar: fixed (AR) parameters from the ARMA component
#   fixed_ma: fixed (MA) parameters from the ARMA component
#   model_mean: whether of not the model the mean in the ARCH model
#               (like the intercept on a linear regression)
create_spec <- function(arma_order, garch_order, extregdata,
                        dist, dof, fixed_ar, fixed_ma, model_mean)
{
    if (!is.null(extregdata)) {
        extregdata <- as.matrix(extregdata)
    }
    spec <- rugarch::ugarchspec(
        mean.model=list(armaOrder=arma_order,
                        external.regressors=extregdata,
                        include.mean=model_mean),
        variance.model=list(model="sGARCH",
                            garchOrder=garch_order),
        distribution.model=dist
    )

    bounds <- list()
    if (!is.null(extregdata)) {
        for (ix in seq_len(ncol(extregdata))) {
            bounds[[paste0('mxreg', ix)]] <- c(-5, 5)  # sensible bounds
        }
    }
    if (length(bounds) != 0) {
        rugarch::setbounds(spec) <- bounds
    }

    fixed <- list()
    if (!is.null(fixed_ar)) {
        for (ix in seq_along(fixed_ar)) {
            bounds[[paste0('ar', ix)]] <- fixed_ar[ix]
        }
    }
    if (!is.null(fixed_ma)) {
        for (ix in seq_along(fixed_ma)) {
            bounds[[paste0('ma', ix)]] <- fixed_ma[ix]
        }
    }
    if (!is.null(dof)) {
        fixed[['shape']] <- dof
    }
    if (length(fixed) != 0) {
        rugarch::setfixed(spec) <- fixed
    }

    return(spec)
}
