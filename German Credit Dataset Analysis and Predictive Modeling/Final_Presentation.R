### all variables


library(dplyr)
library(tidyr)
library(ggplot2)
library(survival)
library(corrplot)
library(tidyverse)


german_credit <- read.csv("german_credit.csv")

german_credit[sapply(german_credit, is.integer)] <- lapply(german_credit[sapply(german_credit, is.integer)],
                                                           as.factor)


creditDatabaseFull <- german_credit
convertToFactor <- c(1,2,4,5,7,8,10,11,12,13,15,16,18,20,21)
creditDatabaseFull[convertToFactor] <- lapply(creditDatabaseFull[convertToFactor], factor)




set.seed(123)
ind <- sample(c("Yes","No"), size = 500 , replace = TRUE, prob = c(0.7,0.3)  ) 
train <- german_credit[ind=="Yes",]
test <- german_credit[ind=="No",]


prop.table(table(train$Creditability))
prop.table(table(test$Creditability))


library(rpart)
fit <- rpart(Creditability~., data = train, method = 'class')
library(RColorBrewer)
library(rattle)
fancyRpartPlot(fit, sub = "All variables")


new_prediction <- predict(fit, train, type = 'class')


table_mat <- table(train$Creditability, new_prediction )
table_mat

accuracy_Test <- sum(diag(table_mat)) / sum(table_mat)
print(paste('Accuracy for test', accuracy_Test))

Recall_test <- table_mat[2,2] / (table_mat[2,2] + table_mat[2,1])
Recall_test

Precision_test <- table_mat[2,2] / (table_mat[2,2] + table_mat[1,2])
Precision_test

true_positive <- table_mat[2,2] / sum(table_mat)
true_positive

false_positive <- table_mat[1,2] / sum(table_mat)
false_positive







### selected variables 


library(dplyr)
library(tidyr)
library(ggplot2)
library(survival)
library(corrplot)
library(tidyverse)


german_credit <- read.csv("german_credit.csv")

german_credit$Age <- cut(german_credit$Age..years., breaks = c(0,18,30,70,120), 
                                   labels = c("Underage","Young Adult","Adult","Elder"))
german_credit$duration_credit <- cut(german_credit$Duration.of.Credit..month., breaks = c(0,12,36,80), 
                         labels = c("Short","Medium","Long"))

german_credit <- german_credit %>% 
  rename(
   payment_status =  Payment.Status.of.Previous.Credit,
   assets = Most.valuable.available.asset,
   stocks = Value.Savings.Stocks,
   instalment = Instalment.per.cent
  )
german_credit2 <-  german_credit %>% select( Creditability , 
                                             Account.Balance , duration_credit, 
                                             payment_status , 
                                             assets
                                             ,stocks ,instalment   ,  
                                             Purpose  , Age
                                             )

german_credit2[sapply(german_credit2, is.integer)] <- lapply(german_credit2[sapply(german_credit2, is.integer)],
                                                             as.factor)

set.seed(123)
ind <- sample(c("Yes","No"), size = 500 , replace = TRUE, prob = c(0.7,0.3)  ) 
train <- german_credit2[ind=="Yes",]
test <- german_credit2[ind=="No",]


prop.table(table(train$Creditability))
prop.table(table(test$Creditability))


library(rpart)# rpart() use gini impurity measure to split the notes.
fit <- rpart(Creditability~., data = train, method = 'class' )
library(RColorBrewer)
library(rattle)
fancyRpartPlot(fit, sub = "Selected variables")   

new_prediction <- predict(fit, train, type = 'class')


table_mat <- table(train$Creditability, new_prediction )
table_mat

accuracy_Test <- sum(diag(table_mat)) / sum(table_mat)
print(paste('Accuracy for test', accuracy_Test))

Recall_test <- table_mat[2,2] / (table_mat[2,2] + table_mat[2,1])
Recall_test

Precision_test <- table_mat[2,2] / (table_mat[2,2] + table_mat[1,2])
Precision_test

true_positive <- table_mat[2,2] / sum(table_mat)
true_positive

false_positive <- table_mat[1,2] / sum(table_mat)
false_positive

print(paste('Accuracy for test', accuracy_Test))

