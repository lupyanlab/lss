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

recode_cue_pic_mapping <- function(frame) {
  # Recode cuePicMapping variable in terms of the consistency
  # of the mapping, e.g., cuePicMapping: fixed == reversed
  # in that both are constant mappings (as opposed to random).
  cue_pic_mapping_levels <- c("random", "fixed", "reversed")
  cue_pic_mapping_map <- dplyr::data_frame(
    cuePicMapping = cue_pic_mapping_levels,
    mapping_consistency = c("random", "constant", "constant")
  )
  
  mapping_consistency_levels <- c("random", "constant")
  mapping_consistency_map <- dplyr::data_frame(
    mapping_consistency = mapping_consistency_levels,
    mapping_consistency_c = c(-0.5, 0.5),
    mapping_consistency_label = factor(mapping_consistency_levels, levels = mapping_consistency_levels)
  )
  
  left_join(cue_pic_mapping_map, mapping_consistency_map) %>%
    left_join(frame, .)
}