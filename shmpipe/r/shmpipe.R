# ShmPipe R helper (requires the arrow package in R).
# NOTE: This R code is included for the polyglot story, but it was
# NOT tested in this VM because R is not installed here.
# In R with arrow installed:
#
#   library(arrow)
#   source("r/shmpipe.R")
#   df <- shmpipe_read("demo")   # data.frame from shared memory
#
# It reads the same .arrow file that Python wrote to /dev/shm.

shmpipe_read <- function(name, shm_dir = "/dev/shm") {
  path <- file.path(shm_dir, paste0("shmpipe-", name, ".arrow"))
  if (!file.exists(path)) stop(paste("No ShmPipe named", name))
  # arrow reads IPC stream files directly
  tab <- arrow::read_ipc_stream(path)
  as.data.frame(tab)
}

shmpipe_write <- function(df, name, shm_dir = "/dev/shm") {
  path <- file.path(shm_dir, paste0("shmpipe-", name, ".arrow"))
  arrow::write_ipc_stream(df, path)
  invisible(path)
}
