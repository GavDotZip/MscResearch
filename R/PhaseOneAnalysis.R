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
emissions_forecast <- forecast(auto.arima(emissions_ts), h = 100)  # Forecast next 10 steps

# Plot the forecasted figures for system_total_emissions
plot(emissions_forecast, main = "Forecasted System Total Emissions")

# Alternatively, plot using autoplot
autoplot(emissions_forecast) +
  labs(title = "Forecasted System Total Emissions",
       x = "Step", y = "Total") +
  theme_minimal()


# Aggregate data for every 100 steps
ph1TFdata_aggregated <- ph1TFdata %>%
  group_by(Group = ceiling(step / 100)) %>%
  summarise(Avg_Emissions = mean(system_total_emissions))

# Plot system_total_emissions as a bar chart for every 100 steps
ggplot(ph1TFdata_aggregated, aes(x = Group, y = Avg_Emissions)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(title = "Average System Total Emissions for Every 100 Steps",
       x = "Step Group",
       y = "Average System Total Emissions") +
  theme_minimal()



# Create the proportions of noise caused and fuel consumption relative to QoLDataTF
ph1TFdata <- ph1TFdata %>%
  mutate(Noise_Proportion = system_total_noise_caused / QoLDataTF,
         Fuel_Consumption_Proportion = system_total_fuel_consumption / QoLDataTF)

# Plot noise caused and fuel consumption as a pie chart
ggplot(ph1TFdata) +
  geom_bar(aes(x = "", y = Noise_Proportion, fill = "Noise Caused"), stat = "identity", width = 1) +
  geom_bar(aes(x = "", y = Fuel_Consumption_Proportion, fill = "Fuel Consumption"), stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  scale_fill_manual(values = c("Noise Caused" = "skyblue", "Fuel Consumption" = "orange")) +
  labs(title = "Proportion of Noise Caused and Fuel Consumption",
       fill = "Category") +
  theme_void() +
  theme(legend.position = "bottom")
 

# Perform two-tailed t-tests
t_test_resultSTE <- t.test(ph1TFdata$system_total_emissions)
t_test_resultFC <- t.test(ph1TFdata$system_total_fuel_consumption)

# Print the t-test result
print(t_test_resultSTE)
print(t_test_resultFC)
