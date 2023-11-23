ScanRecords <- read.csv("~/Downloads/ScanRecords.csv")

library(boot)

type_2 <- ScanRecords$Duration

# Calculating the statistics
f <- function(data, indices) {
  sample_data <- data[indices]
  return(mean(sample_data))
}

# Number of bootstrap samples
num <- 1000

# Perform bootstrap resampling
boot_1 <- boot(data = type_2, statistic = f, R = num)

# Plot the histogram of the bootstrap samples
hist(boot_1$t, main = "Bootstrap",
     xlab = "Duration", col = "lightblue", border = "black")

abline(v = f(type_2, 1:length(type_2)), col = "red", lty = 2)

print(boot_1)
