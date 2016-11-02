# ---- setup
library(dplyr)
library(tidyr)
library(ggplot2)
library(lme4)
library(broom)
library(AICcmodavg)

source("R/load.R")
source("R/tidy.R")
source("R/recoders.R")

LSS <- load_LSS_all() %>%
  tidy_LSS() %>%
  recode_exp_name() %>%
  recode_cue_pic_mapping()

# ---- subjects
subjects <- LSS %>%
  group_by(subjCode) %>%
  summarize(
    rt = mean(rt, na.rm = TRUE),
    error = mean(is_error, na.rm = TRUE)
  ) %>%
  mutate(
    rt_rank = rank(rt, ties.method = "random"),
    error_rank = rank(error, ties.method = "random")
  )

subj_id_size <- 2.2

rt_ylim_padding <- 200
ggplot(subjects, aes(x = rt_rank, y = rt, label = subjCode)) +
  geom_point(size = 1.0) +
  geom_text(angle = 90, hjust = -0.1, size = subj_id_size) +
  coord_cartesian(ylim = c(min(subjects$rt), max(subjects$rt) + rt_ylim_padding))

error_ylim_padding <- 0.15
ggplot(subjects, aes(x = error_rank, y = error, label = subjCode)) +
  geom_point(size = 1.0) +
  geom_text(angle = 90, hjust = -0.1, size = subj_id_size) +
  coord_cartesian(ylim = c(min(subjects$error), max(subjects$error) + error_ylim_padding))

# ---- drop-outliers
outliers <- c("LSS115")
LSS <- filter(LSS, !(subjCode %in% outliers))

# ---- rt-mod
rt_mod <- lmer(rt ~ valid_cue * exp_c + (valid_cue|subjCode), data = LSS)

rt_preds <- expand.grid(valid_cue = 0:1, exp_c = c(-0.5, 0.5)) %>%
  recode_exp_name %>%
  cbind(., predictSE(rt_mod, ., se = TRUE)) %>%
  rename(rt = fit, se = se.fit)

# ---- rt-plot
ggplot(LSS, aes(valid_cue, rt)) +
  geom_bar(stat = "summary", fun.y = "mean") +
  geom_pointrange(aes(ymin = rt - se, ymax = rt + se),
                  data = rt_preds, shape = 1) +
  coord_cartesian(ylim = c(300, 450)) +
  facet_wrap("exp_factor")

# ---- error-mod
error_mod <- glmer(is_error ~ valid_cue * exp_c + (valid_cue|subjCode),
                   family = binomial, data = LSS)

error_preds <- expand.grid(valid_cue = 0:1, exp_c = c(-0.5, 0.5)) %>%
  recode_exp_name %>%
  cbind(., predictSE(error_mod, ., se = TRUE)) %>%
  rename(is_error = fit, se = se.fit)

# ---- error-plot
ggplot(LSS, aes(valid_cue, is_error)) +
  geom_bar(stat = "summary", fun.y = "mean") +
  geom_pointrange(aes(ymin = is_error - se, ymax = is_error + se),
                  data = error_preds, shape = 1) +
  scale_y_continuous(labels = scales::percent) +
  facet_wrap("exp_factor")

# ---- soa-plot
ggplot(LSS, aes(factor(soa), rt, group = valid_cue)) +
  geom_point(aes(color = factor(valid_cue)),
             stat = "summary", fun.y = "mean") +
  geom_smooth(aes(color = factor(valid_cue)), method = "lm") +
  facet_wrap("exp_factor") +
  theme(legend.position = "top")

# ---- mapping-rt-mod
mapping_rt_mod <- lmer(rt ~ mapping_consistency_c * valid_cue + (valid_cue|subjCode),
                       data = LSS)

mapping_rt_preds <- expand.grid(
    mapping_consistency_c = c(-0.5, 0.5),
    valid_cue = c(0, 1),
    stringsAsFactors = FALSE
  ) %>%
  cbind(., predictSE(mapping_rt_mod, ., se = TRUE)) %>%
  rename(rt = fit, se = se.fit) %>%
  recode_cue_pic_mapping()

# ---- mapping-rt-plot
dodge_width <- position_dodge(width = 0.9)
base_plot <- ggplot(LSS, aes(mapping_consistency, rt, group = valid_cue)) +
  geom_bar(aes(fill = factor(valid_cue)),
           stat = "summary", fun.y = "mean",
           position = dodge_width) +
  coord_cartesian(ylim = c(240, 460)) +
  theme(legend.position = "top")

base_plot +
  facet_wrap("exp_factor")

base_plot +
  geom_pointrange(aes(ymin = rt - se, ymax = rt + se),
                  data = mapping_rt_preds,
                  position = dodge_width,
                  shape = 1)

