url1#Libraries used: tm, RCurl, 
#tm vignette: http://cran.r-project.org/web/packages/tm/vignettes/tm.pdf

url1 <- "http://en.wikipedia.org/wiki/Agamemnon"
url2 <- "http://en.wikipedia.org/wiki/Ancient_Greece"

#Given a URL, this function returns a single string with all relevant text
getText <- function(url) {
  htmlData <- readLines(url)
  text <- htmlData[grep("<p>", htmlData)]
  text <- gsub("<.*?>", " ", text) # " "; "" will create false words (e.g. "war.although")
  paste(text, collapse = '') # collapse to return one only 1 character per page
}

#Given a body of text, this function returns it's DocumentTermMatrix
getDocumentTermMatrix <- function(corpora) {
  corpus <- VCorpus(VectorSource(corpora))
  DocumentTermMatrix(corpus, control = list(removePunctuation=TRUE))
}

#Given a DTM, this function returns the actual counts
getCounts <- function(documentTermMatrix) {
  documentTermMatrix$v
}

#for quicker testing
getCountsFromUrl <- function(url) {
    getCounts(getDocumentTermMatrix(getText(url)))  
}

#returns magnitude of vector
magnitude <- function(v) { (sqrt(sum(v ^ 2))) }

#Given two vectors, this function returns the cosine similarity
cosineSimilarity <- function(v1, v2){
  sum(v1 * v2) / (magnitude(v1) * magnitude(v2))
}

findSimilarity <- function(url1, url2){
  m1 <- getDocumentTermMatrix(getText(url1))
  m2 <- getDocumentTermMatrix(getText(url2))
  v1 <- unlist(m1$dimnames)
  v2 <- unlist(m2$dimnames)
  
  i <- is.na(match(v2, v1))
  m2uniqueterms <- v2[i]
  nextid <- length(v1) + 1
  print(sum(i))
  print(length(m2uniqueterms))
  m3 <- rbind(nextid : (nextid + sum(i) - 1), m2uniqueterms, rep(0, sum(i)))
  
  i2 <- is.na(match(v1, v2))
  m1uniqueterms <- v1[i]
  nextid2 <- length(v2) + 1
  print(sum(i2))
  print(length(m1uniqueterms))
  m4 <- rbind(nextid2 : (nextid2 + sum(i2) - 1), m1uniqueterms, rep(0, sum(i2)))
  
  s <- cosineSimilarity(m3[,3], m4[,3])
  #TOFIX: m3[,3] and m4[,3] consist of CHARACTERS, m3 & m4 need to be data.frames instead
  #so that count values are expressed as integers instead of characters
  s
}
