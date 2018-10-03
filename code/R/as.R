# Load packages  ------------------------------------------------------------------------------
library(scales)
library(Hmisc)
library(tidyjson)
library(magrittr)
library(corrr)
library(boot)
library(stringr)
library(svglite)
library(RSQLite)
library(ggrepel)
library(tidyverse)
rm(list = ls())

# Helper functions and variables ----------------------------------------------------------------------------
# Set ggplot theme 
theme_set(
  theme_bw()+
    theme(text = element_text(size = 30),
          panel.grid = element_blank()
    )
)

# Root mean squared error
rmse = function(x,y){
  return(sqrt(mean((x-y)^2)))
}

# Luce's choice axiom
lca = function(x,y){
  if (x+y == 0){
    return(0.5)
  }
  else{
    return(x/(x+y))
  }
}

# Clips we can reconstruct from Moral Kinematics using our physics engine (see paper)
clips_we_can_reconstruct <- c(1,3,4,7,8,9,10,11,12,20,21,22,23,24,25,26,27,28)
clips_in_experiment_2 <- c(1,3,4,7,8,9,10,11,12)

# Experiment 1 clip number to name mapping
clip_number_name_map_mk = c(3,7,12,4,1,9,10,11,8)
clip_number_name_map_counter = c(20:28)

# ~~~~~~~~~~~~~ -------------------------------------------------------------------------------
# EXP1: Read in and Structure Data ------------------------------------------------------------------
# Connect to database file and collect data
con = dbConnect(SQLite(),dbname = "../../data/empirical/experiment1.db");
df.data = dbReadTable(con,"moral_dynamics")
dbDisconnect(con)

# Filter out incomplete trials by users
df.data = df.data %>% 
  filter(status %in% 3:5) %>% 
  filter(!str_detect(uniqueid,'debug')) %>%
  filter(codeversion == 'experiment_3')

# Grab demographic data 
df.demographics = df.data$datastring %>% 
  spread_values(condition = jstring('condition'),
                age = jstring('questiondata','age'),
                gender = jstring('questiondata','sex'),
                feedback = jstring('questiondata','feedback')) %>% 
  rename(participant = document.id) %>% 
  mutate(time = difftime(df.data$endhit,df.data$beginhit,units = 'mins'))

# Create structured trial dataframe 
df.long = df.data$datastring %>% 
  as.tbl_json() %>% # Format datastring as json
  spread_values(participant = jstring('workerId')) %>%
  enter_object('data') %>% # Enter the data sub-object
  gather_array('order') %>% # Gather order into column
  enter_object('trialdata') %>% # Enter the tiral data responses
  spread_values(clip = jstring('clip'),
                display = jstring('order'),
                rating = jstring('rating')) %>%
  as.data.frame() %>% 
  separate(clip, into = c('1', '2')) %>%
  mutate(`1` = str_replace_all(`1`,"video","")) %>% # Leave only numbers
  mutate(`2` = str_replace_all(`2`,"video","")) %>% # Leave only numbers
  filter(`1` %in% clips_we_can_reconstruct) %>% # Filter out only clips we can reconstruct
  filter(`2` %in% clips_we_can_reconstruct) %>% # Filter out only clips we can reconstruct
  mutate(clips = paste(`1`,`2`,sep="_")) %>% # Create clip pair labels
  mutate(rating = as.numeric(rating),
         rating = ifelse(display == 'flipped', 7-rating, rating)) %>% 
  select(-c(display,`1`,`2`)) %>% 
  mutate(participant = factor(participant,labels = 1:length(unique(participant))))

# Create dataframe containing empirical results from "Moral Kinematics"
df.kinematics = read.csv("../../data/empirical/moral_kinematics.csv") %>%
  # Only grab scenarios we can reconstruct (see paper)
  filter(left %in% clips_we_can_reconstruct) %>% # Should be clips_in_experiment_1
  filter(right %in% clips_we_can_reconstruct) # Should be clips_in_experiment_1

# EXP1: Model Predictions  --------------------------------------------------------------------

# Dataframe containing ground-truth effort values for each scenario
df.exp1_eff_val = read.csv("../../data/model/experiment1.csv") %>%
  set_names(c("clip","effort")) %>%
  mutate(clip = c(clip_number_name_map_mk)) %>%
  filter(clip != 'scenario') %>% # Filter out headers from csv file
  filter(clip %in% clips_in_experiment_2) # Should be clips_in_experiment_1

# Dataframe containing LCA predictions of moral judgment
df.predictions = df.long %>% 
  mutate(clip_pairs = clips) %>%
  group_by(clips) %>% 
  summarise(rating = mean(rating)) %>% 
  ungroup() %>% 
  separate(clips,into = c('clip1','clip2'),sep="_") %>%
  mutate_at(vars(contains('clip')),funs(as.numeric(.))) %>% 
  left_join(df.exp1_eff_val %>% 
              select(clip,effort), by = c("clip1" = "clip")) %>%
  left_join(df.exp1_eff_val %>% 
              select(clip,effort), by = c("clip2" = "clip")) %>%
  rename(effort.1 = effort.x) %>%
  rename(effort.2 = effort.y) %>%
  mutate(lca = lca(effort.1,effort.2),
         fit = lm(rating~lca,data=.)$fitted.values,
         clips = paste(clip1,clip2,sep="_"),
         index = 'Model',
         rating.low = lca,
         rating.high = lca,
         rating = lca) %>%
  select('clips','rating','rating.low','rating.high','index')

# EXP1: Plot Results - Mean Judgment Comparison (Bar Graph) -----------------------------------------------------

# Dataframe for bar graph of mean moral judgments across videos
df.plot = df.long %>% 
  mutate(rating = ifelse(rating <= 3,1,0)) %>% 
  group_by(clips) %>% 
  summarise(rating.mean = mean(rating),
            rating.high = smean.cl.boot(rating)[2],
            rating.low = smean.cl.boot(rating)[3]
  ) %>% 
  ungroup() %>% 
  left_join(df.kinematics %>% select(clips,kinematics = rating)) %>%
  gather("index","rating",c(rating.mean,kinematics)) %>% 
  mutate_at(vars(rating.high,rating.low),funs(ifelse(index == 'kinematics',rating,.))) %>% 
  mutate(index = factor(index,levels = c('rating.mean','kinematics'), labels = c('Experiment 1', 'Moral Kinematics'))) %>%
  mutate(clips = as.factor(clips)) %>%
  select('clips', 'index','rating','rating.low','rating.high') %>%
  rbind(df.predictions)

# Generate bar graph
ggplot(df.plot,aes(x=index,y=rating,fill=index))+
  geom_bar(stat = 'identity',color = 'black', position = position_dodge(0.8), width = 0.8)+
  geom_linerange(data=df.plot,aes(ymin=rating.low,ymax=rating.high), position = position_dodge(0.8), width = 0.8)+
  facet_wrap(~clips,ncol=6)+
  labs(y = 'Percent Particpants Judging\nLeft Video as Worse')+
  scale_y_continuous(breaks=c(1.0,0.5,0),labels=c('100%','50%','0%'))+
  theme_bw()+
  theme(legend.position = 'right',
        axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_text(size=18),
        legend.title = element_blank()
  )

# EXP1: Plot Results - Paper Figure (Bar Graph)  -----------------------------------------------------

# Generate bar graphs used in paper
for(i in c(1:9)){
  df.tmp = df.plot %>%
    filter(clips %in% c(toString(df.plot[i,]$clips))) %>%
    mutate(clips = str_replace_all(clips,"_"," vs "))
  
  ggplot(df.tmp,aes(x=index,y=rating,fill=index))+
    geom_bar(stat = 'identity',color = 'black', position = position_dodge(0.8), width = 0.8)+
    geom_hline(yintercept = 0.5, linetype = 2, color = 'black')+
    geom_linerange(data=df.tmp,aes(ymin=rating.low,ymax=rating.high), position = position_dodge(0.8), width = 0.8)+
    labs(y = '')+
    scale_y_continuous(limits=c(0, 1.0),breaks=c(1.0,0.5,0),labels=c('100%','50%','0%'))+
    scale_fill_grey(start = 0.5, end = .9)+
    theme_bw()+
    theme(legend.position = 'none',
          axis.title.x = element_blank(),
          axis.text.x = element_blank(),
          axis.text.y = element_text(size=30,face='bold'),
          legend.title = element_blank()
    )
  # ggsave(paste("../../figures/plots/experiment_1/collapsed_mean_",toString(toString(df.plot[i,]$clips)),".pdf"),width=8,height=4)
}

# ~~~~~~~~~~~~~ -------------------------------------------------------------------------------
# EXP2: Read in and Structure Data ------------------------------------------------------------------
# Connect to database file and collect data
con = dbConnect(SQLite(),dbname = "../../data/empirical/experiment2.db");
df.data = dbReadTable(con,"moral_dynamics")
dbDisconnect(con)

# Filter out incomplete trials by users
df.data = df.data %>% 
  filter(status %in% 3:5) %>% 
  filter(!str_detect(uniqueid,'debug')) %>%
  filter(codeversion %in% c('experiment_7'))

# Grab demographic data 
df.demographics = df.data$datastring %>% 
  spread_values(condition = jstring('condition'),
                age = jstring('questiondata','age'),
                gender = jstring('questiondata','sex'),
                feedback = jstring('questiondata','feedback')
  ) %>%
  mutate(time = difftime(df.data$endhit,df.data$beginhit,units = 'mins'),
         condition = factor(condition,levels = 0:1, labels = c('effort','moral'))) %>% 
  rename(participant = document.id)

# Structure the trial data 
df.long = df.data$datastring %>% # Grab datastring
  as.tbl_json() %>% # Structure it as a json
  enter_object('data') %>% # Access the recorded data sub-object
  gather_array('order') %>% 
  enter_object('trialdata') %>% # Access the recorded responses from the trials 
  gather_object('index') %>% 
  append_values_string('values') %>% 
  as.data.frame() %>% # Compile everything into a dataframe
  spread(index,values) %>% # Tidy up key:value pairs
  rename(participant = document.id) %>% 
  select(-condition) %>% 
  left_join(df.demographics %>% select(participant,condition), by = 'participant') %>% 
  rename(rating = response) %>% 
  mutate(rating = as.numeric(rating),
         rating = rescale(rating, to=c(0,1))) %>% 
  arrange(participant)

# EXP2: Model Predictions ------------------------------------------------------------------

# Effort predictions from Moral Dyanmics model 
df.exp2_eff_val = read.csv("../../data/model/experiment2.csv")

# Datafrane for model prediction
df.predictions = df.long %>% 
  # filter(clip %in% !c('video4', 'video12')) %>%
  group_by(condition,clip) %>% 
  summarise(mean = mean(rating),
            low = smean.cl.boot(rating)[2],
            high = smean.cl.boot(rating)[3]
  ) %>% 
  ungroup() %>% 
  gather(index,value,-c(condition,clip)) %>% 
  unite(condition_index,condition,index) %>% 
  spread(condition_index,value) %>% 
  left_join(df.exp2_eff_val, by = c('clip'='names')) %>% 
  mutate(effort = rescale(effort, to=c(0,1))) %>%
  #filter(!(clip %in% c('video4', 'video12'))) %>% # Test
  mutate(effort_model_prediction = glm(effort_mean~effort,family=binomial(),data=.)$fitted.values, # Model prediction of effort judgments
         moral_empirical_prediction = glm(moral_mean~effort_mean,family=binomial(),data=.)$fitted.values, # Prediction of moral judgments using effort judgments
         moral_model_prediction = glm(moral_mean~effort,family=binomial(),data=.)$fitted.values) # Model prediction of moral judgments

# EXP2: Regression ------------------------------------------------------------------

# Statistical summaries 
moral_model_fit = lm(moral_mean~moral_model_prediction,data=df.predictions) 
moral_model_fit %>% summary()
cor(df.predictions$effort_model_prediction, df.predictions$moral_mean) # Correlate model predictions with moral judgments

effort_model_fit = lm(effort_mean~effort_model_prediction,data=df.predictions) 
effort_model_fit %>% summary()
cor(df.predictions$effort_model_prediction, df.predictions$effort_mean) # Correlate model effort with effort judgments

moral_model_fit = lm(moral_mean~moral_empirical_prediction,data=df.predictions) 
moral_model_fit %>% summary()
cor(df.predictions$moral_empirical_prediction, df.predictions$moral_mean) # Correlate effort judgment with moral judgments

# EXP2: Within Participant Correlation ------------------------------------------------------------------

# Initialize regression sum to 0
regression_sum = 0
# Iterate through all participants and leave one out and correlate with others
for (i in c(1:length(unique(df.long$participant)))) {
  # Temporary dataframe 
  df.tmp = df.predictions %>%
    select('clip','effort')
  # Participant dataframe
  df.participant = df.long %>%
    filter(participant %in% c(i)) %>%
    select('clip', 'rating')
  # Add to the regression sum
  regression_sum = regression_sum + abs(cor(df.tmp$effort, df.participant$rating))
}
regression_sum = regression_sum/length(unique(df.long$participant))

# EXP2: Cross Validation ------------------------------------------------------------------

# Initialize square error to 0
square_error = 0
for (i in c(1:length(df.predictions$clip))) {
  # Filter out clips
  df.tmp = df.predictions %>%
    filter(clip != df.predictions$clip[i])
  # Fit glm to remaining clips
  moral_model_fit = glm(moral_mean~effort,family=binomial(),data=df.tmp) 
  # Actual value
  y = df.predictions$moral_mean[i]
  # Predicted value
  y_hat = predict(moral_model_fit,data.frame(effort=df.predictions$effort[i]),type='response')
  # Sum square error
  square_error = square_error + (y - y_hat)^2
}
print(square_error/length(df.predictions$clip))

# EXP2: Bootstrapped Confidence Intervals ------------------------------------------------------------------

# Statistic function
estimation_func <- function(original_dataset, d) {
  # Gather sampled_dataset
  sampled_dataset = original_dataset %>% 
    filter(participant %in% d) %>% # Gather sample from original dataset
    group_by(condition,clip) %>% 
    summarise(mean = mean(rating)) %>% # Compute mean for responses across videos
    ungroup() %>% 
    gather(index,value,-c(condition,clip)) %>% 
    unite(condition_index,condition,index) %>% 
    spread(condition_index,value) %>% 
    left_join(df.exp2_eff_val, by = c('clip'='names')) %>% 
    mutate(effort = rescale(effort, to=c(0,1))) # Rescale effort values from physics engine to [0,1]
  # Fit a glm to the sampled dataset and gather fitted values
  fitted_values = glm(moral_mean~effort, family = binomial(), data=sampled_dataset)$fitted.values
  # Measure correaltion between fitted values and sampled_dataset
  corr = cor(sampled_dataset$moral_mean, fitted_values)
  # Return correlation
  return(corr)
}

# Gather moral condition only
moral_dataset = df.long %>%
  filter(condition == 'moral') 

# Renumber participant IDs (this is important because we use participant IDs as indices!)
moral_dataset$participant <- moral_dataset %>% 
  group_indices(moral_dataset$participant)

# Make boot object
b = boot(moral_dataset, estimation_func, R=1000)
summary(b)
# Gather ci for correlations
ci = boot.ci(b,conf=.95)
# Print out summary of ci
summary(ci)

# EXP2: Plot Results - Mean Judgments (Scatterplot) --------------------------------------------------------------------

# Dataframe for scatterplot of mean moral judgments by mean effort judgments
df.plot = df.long %>% 
  mutate(rating = as.numeric(rating)) %>% 
  group_by(clip,condition) %>% 
  summarise(mean = mean(rating)) %>% 
  spread(condition,mean) %>% 
  ungroup() %>% 
  select(clip,effort,moral) %>% 
  mutate(index = 1:nrow(.))

# Generate scatterplot
ggplot(df.plot,aes(x=effort,y=moral))+
  geom_abline(intercept = 0, slope = 1, linetype = 2)+
  geom_smooth(method=lm,color='black')+
  # geom_errorbar(aes(ymin = effort_low, ymax = effort_high),width=0)+
  geom_point(size=6)+
  geom_text_repel(aes(label = index),size=10)+
  # coord_cartesian(xlim=c(25,100),ylim=c(25,100))+
  coord_cartesian(xlim=c(0,100),ylim=c(0,100))+
  scale_x_continuous(breaks = seq(0,100,25),labels = seq(0,100,25))+
  scale_y_continuous(breaks = seq(0,100,25),labels = seq(0,100,25))+
  labs(y = 'Mean Moral Judgments', x = 'Mean Effort Judgments')
ggsave("../../figures/plots/experiment_2_scatter.png",width=18,height=15)

# EXP2: Plot Results - Paper Figure (Bar Graph) --------------------------------------------------------------------

df.plot = df.long %>%
  left_join(df.predictions) %>%
  mutate(clip = as.factor(clip))

ggplot(df.plot,aes(x=condition,y=rating,fill=condition))+
  stat_summary(fun.y = mean, geom = 'bar', color = 'black')+
  geom_point(aes(x=c('moral'),y=moral_model_prediction),color='black',fill='light grey',shape=21,size=6)+ # Model effort prediction
  geom_point(aes(x=c('effort'),y=effort_model_prediction),color='black',shape=21,size=6)+
  # geom_text(aes(label = clip),size=2)+
  stat_summary(fun.data = mean_cl_boot, geom = 'errorbar', width = 0, color = 'black')+
  facet_wrap(~(-1*moral_mean),ncol=6)+
  scale_y_continuous(limits=c(0, 105),breaks=c(100,50,0),labels=c('100','50','0'))+
  scale_fill_grey(start = 0.5, end = .9)+
  labs(y = ' ')+
  theme(legend.position = 'none',
        axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        strip.text.x = element_blank(),
        legend.title = element_blank(),
        panel.spacing.y = unit(13, "lines")
  )
ggsave("../../figures/plots/experiment_2_paper.pdf",width=14,height=16)

# ~~~~~~~~~~~~~ -------------------------------------------------------------------------------
