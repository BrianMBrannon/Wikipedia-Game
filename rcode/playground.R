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
  
  i <- is.na(match(v2, v1)) #logical vector
  m2uniqueterms <- v2[i] #terms in m2 that are not in m1
  i2 <- is.na(match(v1, v2))
  m1uniqueterms <- v1[i2] 
  
  nextid <- length(v1) + 1
  df2 <- as.data.frame(c(m2$j, (nextid : (nextid + sum(i2))))) #start data frame off with ids
  df2 <- cbind(df2, c(v2, m1uniqueterms))
  df2 <- cbind(df2, c(m2$v, rep(0, sum(i2) + 1)))

  nextid2 <- length(v2) + 1
  df1 <- as.data.frame(c(m1$j, (nextid2 : (nextid2 + sum(i))))) 
  df1 <- cbind(df1, c(v1, m2uniqueterms))
  df1 <- cbind(df1, c(m1$v, rep(0, sum(i) + 1)))
  
  s <- cosineSimilarity(df1[,3], df2[,3])
  #TOFIX: m3[,3] and m4[,3] consist of CHARACTERS, m3 & m4 need to be data.frames instead
  #so that count values are expressed as integers instead of characters
  s
}
