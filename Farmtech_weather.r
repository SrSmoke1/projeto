# FarmTech Solutions - Clima (Ir além, simplificado)

# Precisamos apenas de httr e jsonlite
if (!requireNamespace("httr", quietly = TRUE)) install.packages("httr", repos = "https://cloud.r-project.org")
if (!requireNamespace("jsonlite", quietly = TRUE)) install.packages("jsonlite", repos = "https://cloud.r-project.org")

library(httr)
library(jsonlite)

# ---- Argumentos ----
# Lat e Long Bauru-SP
args <- c("-22.3145", "-49.0587")

lat <- as.numeric(args[1])
lon <- as.numeric(args[2])

# ---- Consulta simples na API Open-Meteo ----
url <- paste0(
  "https://api.open-meteo.com/v1/forecast?",
  "latitude=", lat,
  "&longitude=", lon,
  "&current=temperature_2m,relative_humidity_2m,wind_speed_10m",
  "&hourly=temperature_2m,relative_humidity_2m,precipitation",
  "&timezone=auto"
)

resp <- GET(url)
if (status_code(resp) != 200) {
  stop(paste("Erro na API:", status_code(resp)))
}
data <- fromJSON(content(resp, as = "text", encoding = "UTF-8"))

# ---- Clima atual ----
cat("=== Clima atual ===\n")
cur <- data$current
cat("Temperatura:", cur$temperature_2m, "°C\n")
cat("Umidade:", cur$relative_humidity_2m, "%\n")
cat("Vento:", cur$wind_speed_10m, "km/h\n")

# ---- Estatísticas horárias (média e desvio) ----
temp <- as.numeric(data$hourly$temperature_2m)
umid <- as.numeric(data$hourly$relative_humidity_2m)
prec <- as.numeric(data$hourly$precipitation)

cat("\n=== Estatísticas do dia ===\n")
cat("Temperatura média:", round(mean(temp, na.rm = TRUE), 2), "°C | desvio:", round(sd(temp, na.rm = TRUE), 2), "\n")
cat("Umidade média:", round(mean(umid, na.rm = TRUE), 2), "% | desvio:", round(sd(umid, na.rm = TRUE), 2), "\n")
cat("Precipitação média:", round(mean(prec, na.rm = TRUE), 2), "mm | desvio:", round(sd(prec, na.rm = TRUE), 2), "\n")