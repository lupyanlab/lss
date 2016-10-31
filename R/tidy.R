library(dplyr)

tidy_LSS <- function(LSS) {
  LSS %>%
    filter(whichPart != "practice") %>%
    mutate(rt = ifelse(isRight==1, rt, NaN),
           is_error = 1-isRight)
}