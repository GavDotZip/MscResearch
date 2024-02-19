# Load in libraries
library(readxl)
library(tidyverse)
library(tidytext)
library(ggplot2)
library(forecast)


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

# Calculate means, medians, and standard deviations for each column
summary_stats <- ph1TFdata %>%
  summarise(across(everything(), list(mean = mean, median = median, sd = sd)))

# Reshape the data for plotting
summary_stats_long <- summary_stats %>%
  pivot_longer(cols = everything(),
               names_to = c(".value", "stat"),
               names_sep = "_")

# Plot means, medians, and standard deviations as a bar chart
ggplot(summary_stats_long, aes(x = stat, y = value, fill = stat)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9)) +
  facet_wrap(~name, scales = "free") +
  labs(title = "Summary Statistics of Columns",
       x = "Statistic",
       y = "Value") +
  theme_minimal()


# Calculate totals of each column over the runtime
totals <- apply(ph1TFdata[, -1], 2, cumsum)  # Calculate cumulative sum of each column

# Create a dataframe for plotting
totals_df <- data.frame(
  Step = ph1TFdata$step,
  totals
)

# Reshape the dataframe for plotting
totals_df <- tidyr::pivot_longer(totals_df, -Step, names_to = "Variable", values_to = "Total")

# Plot the totals of each column over the runtime
ggplot(totals_df, aes(x = Step, y = Total, color = Variable)) +
  geom_line() +
  labs(title = "Total of Each Column Over Runtime", x = "Step", y = "Total") +
  theme_minimal()

############################
# Forecast Total Emissions #
############################

# Create a time series object for system_total_emissions column
emissions_ts <- ts(ph1TFdata$system_total_emissions)

# Forecast future figures for system_total_emissions
emissions_forecast <- forecast(auto.arima(emissions_ts), h = 100)  # Forecast next 100 steps

# Plot the forecasted figures for system_total_emissions
plot(emissions_forecast, main = "Forecasted System Total Emissions")

# Alternatively, plot using autoplot
autoplot(emissions_forecast) +
  labs(title = "Forecasted System Total Emissions",
       x = "Step", y = "Total") +
  theme_minimal()
