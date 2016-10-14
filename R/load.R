library(dplyr)

load_LSS <- function(pattern = "LSS", header = "header_LSS.txt") {
  header <- read.delim(header) %>% colnames
  list.files("data", pattern = pattern, full.names = TRUE) %>%
    lapply(read.delim, col.names = header, stringsAsFactors = FALSE) %>%
    bind_rows()
}