library(dplyr)

recode_exp_name <- function(frame) {
  exp_name_levels <- c("LSS_v1", "LSS_v2")
  exp_name_labels <- c("one-sided", "masked")

  exp_name_map <- dplyr::data_frame(
    exp_name = exp_name_levels,
    exp_c = c(-0.5, 0.5),
    exp_factor = factor(exp_name_levels, levels = exp_name_levels, labels = exp_name_labels)
  )
  
  frame %>% left_join(exp_name_map)
}