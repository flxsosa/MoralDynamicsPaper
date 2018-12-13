# Load packages -------------------------------------------------------------------------------
library(RSQLite)
library(tidyverse)

# Handle input --------------------------------------------------------------------------------
args = commandArgs(T)

filename = args[1]
tablename = args[2]

# Anonymize table -----------------------------------------------------------------------------
con = dbConnect(SQLite(),dbname = paste0(filename));
df.table = dbReadTable(con,tablename)
dbDisconnect(con)

df.table = df.table %>%
  filter(!str_detect(uniqueid,'debug')) %>%
  mutate(datastring = str_replace_all(datastring,uniqueid,as.character(row_number())),
         datastring = str_replace_all(datastring,workerid,as.character(row_number()))) %>%
  select(-uniqueid,-workerid,-ipaddress)

con = dbConnect(SQLite(), paste0(str_remove(filename,".db"),"_anonymized.db"))
dbWriteTable(con,tablename,df.table)
dbDisconnect(con)