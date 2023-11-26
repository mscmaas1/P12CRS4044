ScanRecords <- read.csv("~/Downloads/ScanRecords.csv")

# Separate data for Type 1 and Type 2 patients
type1 <- ScanRecords[ScanRecords$PatientType == "Type 1", ]
type2 <- ScanRecords[ScanRecords$PatientType == "Type 2", ]

# Extract duration information for Type 1 and Type 2
type1_duration <- type1$Duration
type2_duration <- type2$Duration

# Calculate mean and standard deviation for Type 1
mean_1 <- mean(type1_duration)
sd_1 <- sd(type1_duration)
cat("Type1 mean:", mean_1, "\n")
cat("Type1 standard deviation:", sd_1, "\n")

# Perform t-test for Type 1 duration
t_test_1 <- t.test(type1_duration)
cat("95% Confidence Interval:", t_test_1$conf.int, "\n")

library(boot)
set.seed(6411)

# Define a function for bootstrapping (calculating mean)
f <- function(data, indices) {
  sample_data <- data[indices]
  return(mean(sample_data))
}

# Bootstrap estimation for Type 2 duration
boot_1 <- boot(data = type2_duration, statistic = f, R = length(type2_duration))

# Plot histogram of bootstrap means
hist(boot_1$t, main = "Bootstrap",
     xlab = "Duration", col = "lightblue", border = "black")
abline(v = f(type2_duration, 1:length(type2_duration)), col = "red", lty = 2)

# Print bootstrap results
print(boot_1)

# Calculate and print a 95% confidence interval for the bootstrap mean
CI <- boot.ci(boot_1, type = "basic", conf = 0.95)
CI

# Function for bootstrap estimation (used in the loop)
boot_2 <- function(data) {
  boot_result <- boot(data, statistic = f, R = length(type2_duration))
  return(boot_result$t0)
}

# Monte Carlo simulation for bias and MSE
bootstrap_results <- numeric(1000)

for (i in 1:1000) {
  simulated_data <- sample(type2_duration, replace = TRUE)
  bootstrap_result <- boot_2(simulated_data)
  bootstrap_results[i] <- bootstrap_result
}

# Calculating bias and MSE
bias <- mean(bootstrap_results) - mean(type2_duration)
mse <- mean((bootstrap_results - mean(type2_duration))^2)
cat("Bias:", bias, "\n")
cat("MSE:", mse, "\n")



