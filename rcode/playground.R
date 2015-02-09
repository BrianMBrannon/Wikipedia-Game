#Libraries used: tm, RCurl, 
#tm vignette: http://cran.r-project.org/web/packages/tm/vignettes/tm.pdf

library(tm)
library(RCurl)

url1 <- "http://en.wikipedia.org/wiki/Agamemnon"
url2 <- "http://en.wikipedia.org/wiki/Achilles"
url3 <- "http://en.wikipedia.org/wiki/Ancient_Greece"
url4 <- "http://en.wikipedia.org/wiki/Tomato"

#Given a URL, this function returns a single string with all relevant text
getText <- function(url) {
  htmlData <- readLines(url)
  text <- htmlData[grep("<p>", htmlData)]
  text <- gsub("<.*?>", " ", text) # " "; "" will create false words (e.g. "war.although")
  text <- paste(text, collapse = '') # collapse to return one only 1 character per page
  text
}

#Given a body of text, this function returns it's DocumentTermMatrix
getDocumentTermMatrix <- function(corpora) {
  corpus <- VCorpus(VectorSource(corpora))
  DocumentTermMatrix(corpus, control = list(removePunctuation=TRUE, removeNumbers=TRUE, stopwords=stopwords("en")))
}

#Remove common occurances of English words
#Ignore; learned about stop words.
removeCommonWords <- function(text){
  words <- c("the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go")
  
  removeWords(text, words)
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
#This function can take a long time to compute
cosineSimilarity <- function(v1, v2){
  sum(v1 * v2) / (magnitude(v1) * magnitude(v2))
}

tanimotoSimilarity <- function(v1, v2){
  dp <- sum(v1 * v2)
  dp / (magnitude(v1)^2 + magnitude(v2)^2 - dp)
}

findSimilarity <- function(url1, url2, func){
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
  
  s <- func(df1[,3], df2[,3])
  #TOFIX: m3[,3] and m4[,3] consist of CHARACTERS, m3 & m4 need to be data.frames instead
  #so that count values are expressed as integers instead of characters
  s
}

#Gets the average similarity between any two random Wikipedia pages.
averageSimilarity <- function(n, func){
  random <- "http://en.wikipedia.org/wiki/Special:Random"
  i <- 0
  sum <- 0
  while (i < n){
    sim <- findSimilarity(random, random, func)
    sum <- sum + sim
    i <- i + 1
    print(sim)
  }
  
  sum / n
  #About 0.40 for cosineSimilarity
}