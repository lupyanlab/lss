library(dplyr)
library(ggplot2)
library(lme4)
library(broom)
library(AICcmodavg)

source("R/load.R")
source("R/tidy.R")
source("R/recoders.R")

LSS <- load_LSS_all() %>%
  tidy_LSS %>%
  recode_exp_name

mod <- lmer(rt ~ valid_cue * exp_c + (valid_cue|subjCode), data = LSS)
tidy(mod, effects = "fixed")

preds <- expand.grid(valid_cue = 0:1, exp_c = c(-0.5, 0.5)) %>%
  recode_exp_name %>%
  cbind(., predictSE(mod, ., se = TRUE)) %>%
  rename(rt = fit, se = se.fit)

ggplot(LSS, aes(valid_cue, rt)) +
  geom_bar(stat = "summary", fun.y = "mean") +
  geom_pointrange(aes(ymin = rt - se, ymax = rt + se),
                  data = preds) +
  coord_cartesian(ylim = c(300, 450)) +
  facet_wrap("exp_factor")
