  
  library("warbleR")
  
  
  working.path <- "C:/Voice-Analysis/Audio"
  setwd(working.path)
  # manualoc(flim = c(0,28))
  getwd()
  
  input_csv <- data.frame("sound.files" = "demo.wav", "selec" = 1, "start" = 0, "end" = 5)
  
  dat <- specan(input_csv, bp = c(0,0.28), path = working.path, fast = TRUE)
  filtered_dat <- dat[,-which(names(dat) %in% c("sound.files", "selec", "duration", "time.median", "time.Q25", "time.Q75", "time.IQR", "time.ent", "entropy", "startdom", "enddom", "dfslope", "meanpeakf", "peakf"))]
  write.csv(filtered_dat, "C:/Voice-Analysis/Audio/Features.csv", row.names = FALSE)
