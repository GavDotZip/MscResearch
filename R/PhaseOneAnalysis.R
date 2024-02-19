# Load in libraries
library(readxl)
library(tidyverse)
library(tidytext)
library(ggplot2)

# Load in data
p1TradFixed <- "C:/Users/gavin/MscResearch/src/ph1/results/PhaseOneTraditionalFixed.xlsx"

# Print data structure
ph1TFdata <- read_excel(p1TradFixed)