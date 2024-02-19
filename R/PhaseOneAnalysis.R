# Load in libraries
library(readxl)
library(tidyverse)
library(tidytext)
library(ggplot2)

# Load in data
p1TradFixed <- "C:/Users/gavin/MscResearch/src/ph1/results/PhaseOneTraditionalFixed.xlsx"

# Print data structure
ph1TFdata <- read_excel(p1TradFixed)

if (!is.null(ph1TFdata)) {
  
  # Display summary of traditional data
  cat("\nSummary of Phase One Traditional Data:\n")
  print(summary(ph1TFdata))
  
} else {
  cat("Error: Failed to load data from one or more files.\n")
}


# Print basic numeric calculations
mean_dataTF <- sapply(ph1TFdata[, -1], mean) 
median_dataTF <- sapply(ph1TFdata[, -1], median)
sd_dataTF <- sapply(ph1TFdata[, -1], sd)

# Round the results to 2 decimals
mean_dataTF <- round(mean_dataTF, 2)
median_dataTF <- round(median_dataTF, 2)
sd_dataTF <- round(sd_dataTF, 2)

# Combine results into a data frame
analysis_results <- data.frame(
  Mean = mean_dataTF,
  Median = median_dataTF,
  SD = sd_dataTF
)

# View the analysis results
print(analysis_results)
