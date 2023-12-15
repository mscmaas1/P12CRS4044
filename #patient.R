ScanRecords <- read.csv("~/Downloads/ScanRecords.csv")

type1 <- ScanRecords[ScanRecords$PatientType == "Type 1", ]
type2 <- ScanRecords[ScanRecords$PatientType == "Type 2", ]

library(dplyr)

Numtype1 <- type1 %>%
  group_by(Date) %>%
  summarise(NumRows = n())


Numtype2 <- type2 %>%
  group_by(Date) %>%
  summarise(NumRows = n())


library(boot)
set.seed(6411)

# Define a function for bootstrapping (calculating mean)
f <- function(data, indices) {
  sample_data <- data[indices]
  return(mean(sample_data))
}

boot_2 <- boot(data = Numtype2$NumRows, statistic = f, R = 1000)

hist(boot_2$t, main = "Number of patients per day",
     xlab = "Type 2", col = "lightblue", border = "black")
abline(v = f(Numtype2$NumRows, 1:length(Numtype2$NumRows)), col = "red", lty = 2)

mean(boot_2$t)

qqnorm(boot_2$t, main = "Number of patients per day")
qqline(boot_2$t)
shapiro.test(boot_2$t)


# Function for bootstrap estimation (used in the loop)
boot_0 <- function(data) {
  boot_result <- boot(data, statistic = f, R = 1000)
  return(boot_result$t0)
}


bootstrap_results_2 <- numeric(1000)

for (i in 1:1000) {
  simulated_data_2 <- sample(Numtype2$NumRows, replace = TRUE)
  bootstrap_result_2 <- boot_0(simulated_data_2)
  bootstrap_results_2[i] <- bootstrap_result_2
}

bias_2 <- mean(bootstrap_results_2) - mean(Numtype2$NumRows)
mse_2 <- mean((bootstrap_results_2 - mean(Numtype2$NumRows))^2)

cat("Bias:", bias_2, "\n")
cat("MSE:", mse_2, "\n")






