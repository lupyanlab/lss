library(dplyr)
library(ggplot2)
library(lme4)
library(broom)
library(AICcmodavg)

source("R/load.R")
source("R/tidy.R")

LSS <- load_LSS() %>% tidy_LSS

mod <- lmer(rt ~ valid_cue + (valid_cue|subjCode), data = LSS)
tidy(mod, effects = "fixed")

preds <- data.frame(valid_cue = 0:1) %>%
  cbind(., predictSE(mod, ., se = TRUE))

ggplot(LSS, aes(valid_cue, rt)) +
  geom_bar(stat = "summary", fun.y = "mean") +
  geom_linerange(aes(y = fit, ymin = fit-se.fit, ymax=fit+se.fit),
                 data = preds)

