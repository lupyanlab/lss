library(readr)
library(dplyr)
library(stringr)

v1_seeds <- 101:104

read_and_label_trials_csv <- function(trials_csv) {
  seed <- str_extract(trials_csv, "[[:digit:]]+") %>% as.numeric
  version <- ifelse(seed %in% v1_seeds, "v1", "v2")
  read_csv(trials_csv) %>% mutate(seed = seed, version = version)
}

trials_csvs <- dir("trials", "*.csv", full.names = TRUE)
trials <- lapply(trials_csvs, read_and_label_trials_csv) %>% bind_rows

grouping_vars <- c("pic_category", "pic_version", "cue_version")

unique(subset(trials, select = grouping_vars, version == "v1")) %>%
  arrange_(grouping_vars)

# Right now pic_version A is always appearing with cue_version A.
# For version 2, we want pic_version A to appear with both cue_versions A and B.

unique(subset(trials, select = grouping_vars, version == "v2")) %>%
  arrange_(grouping_vars)
