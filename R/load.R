library(dplyr)
library(readr)

load_LSS_participant <- function(name, col_names) {
  read_tsv(name, col_names = col_names)
}

load_LSS_version <- function(pattern = "LSS", header = "header_LSS.txt", ...) {
  col_names <- read_tsv(header) %>% colnames
  list.files("data", pattern = pattern, full.names = TRUE, ...) %>%
    lapply(load_LSS_participant, col_names = col_names) %>%
    bind_rows()
}

load_LSS_v1 <- function() {
  load_LSS(pattern = "LSS1") %>%
    mutate(exp_name = "LSS_v1")
}

load_LSS_v2 <- function() {
  load_LSS(pattern = "lss_v2", header = "header_LSS_v2.txt", ignore.case = TRUE)
}

load_LSS_all <- function() {
  v1 <- load_LSS_v1()
  v2 <- load_LSS_v2()
  bind_rows(v1, v2)
}