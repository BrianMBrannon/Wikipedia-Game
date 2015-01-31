#Libraries used: tm, RCurl, 
#tm vignette: http://cran.r-project.org/web/packages/tm/vignettes/tm.pdf

url <- "http://en.wikipedia.org/wiki/Agamemnon"

getText <- function(url) {
  htmlData <- readLines(url)
  text <- htmlData[grep("<p>", htmlData)]
  text <- gsub("<.*?>", "", text)
  text
}

getDocumentMatrix <- function(corporaVector) {
  corpus <- VCorpus(VectorSource(corporaVector))
  DocumentTermMatrix(corpus)
}