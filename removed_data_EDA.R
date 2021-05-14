# 簡單迴歸之探索性資料分析
library(readr)

removed_data <- read_csv("C:/Users/frank/OneDrive/桌面/remove_outliers_data.csv")
View(removed_data)

library(funModeling)
library(tidyverse) 
library(Hmisc)

basic_eda_removed <- function(removed_data)
{glimpse(removed_data)
  print(removed_data)
  print(profiling_num(removed_data))
  plot_num(removed_data)
  describe(removed_data)}

basic_eda_removed(removed_data)

#-------------------------------------------
#統計圖表

library(ggplot2)
#[盒形圖 box plot] 
#<法一>
boxplot(removed_data$X_TSM, #指定資料
        col = "steelblue", #指定圖表顏色
        outline = TRUE, #開啟outline
        main = "台積電ADR股價報酬率盒形圖", #圖表主標題
        xlab = "Quantiles",
        ylab = "", #y軸標題
        oulier.tagging = TRUE, #開啟極端值標示
        outlier.label =TRUE, 
        pars = list(boxwex = 0.8, staplewex = 0.5, outwex = 0.5), #調整單一表大小
        horizontal = TRUE,
        range = 1.5,  #指定「鬍鬚」（也就是虛線）的延伸程度，公式：range*從盒子延伸出的四分位距
        plot = TRUE)
boxplot(removed_data$Y_2330, #指定資料
        col = "steelblue", #指定圖表顏色
        outline = TRUE, #開啟outline
        main = "台灣台積電股價報酬率盒形圖", #圖表主標題
        xlab = "Quantiles",
        ylab = "", #y軸標題
        oulier.tagging = TRUE, #開啟極端值標示
        outlier.label =TRUE, 
        pars = list(boxwex = 0.8, staplewex = 0.5, outwex = 0.5), #調整單一表大小
        horizontal = TRUE,
        range = 1.5,  #指定「鬍鬚」（也就是虛線）的延伸程度，公式：range*從盒子延伸出的四分位距
        plot = TRUE)
#<法二> 
ggplot(removed_data, aes(x = X_TSM, y = 1)) +
  geom_boxplot()

ggplot(removed_data, aes(x = 1, y = Y_2330)) +
  geom_boxplot()+
  coord_flip() #反轉

#待修正
#boxplot(removed_data$X_TSM, range = 1.5, width = NULL, varwidth = FALSE, notch = FALSE, 
        #outline = TRUE, names, plot = TRUE, border = par("fg"), col = NULL, 
        #log = "", pars = list(boxwex = 0.8, staplewex = 0.5, outwex = 0.5), 
        #horizontal = TURE, add = FALSE, at = NULL)

#[直方圖 histogram] 

#<法一>
ggplot(removed_data, aes(X_TSM)) +
  geom_histogram(bins=10)

#<法二>
hist(removed_data$X_TSM , #指定繪圖對象
     main = "台積電ADR股價報酬率 次數直方圖", #圖表名稱
     col= "steelblue",
     axes = TRUE, 
     freq = FALSE, #freq若為FALSE，則y軸為密度(density)
     plot = TRUE,  #顯示圖表
     label = FALSE) #標示資料
#rug(jitter(Reg_XY_data$X_TSM))  #繪製x軸的頻率圖，對應區間內數值出現頻率
#lines(density(Reg_XY_data$X_TSM), col = "red", lwd = 2) #繪製核密度曲線

hist(removed_data$Y_2330,
     main = "台灣台積電股價報酬率 次數直方圖",
     col= "steelblue",
     axes = TRUE,
     freq = FALSE, #freq為TRUE，y軸為頻率(frequency)
     plot = TRUE, 
     label = FALSE)

# [莖葉圖 stem-and-leaf plot]
stem(x, scale = 莖葉圖長度, width = 莖葉圖寬度, atom = 1e-08(容忍值))
stem(removed_data$X_TSM)

# [折線圖 line plot]
line_plot_X <- ggplot(removed_data, aes(x = Date, y = X_TSM)) +
  geom_line()
line_plot_X

line_plot_Y <- ggplot(removed_data, aes(x = Date, y = Y_2330)) +
  geom_line()
line_plot_Y
#=========================沒成功================================
# [雙y軸折線圖]
# define mts with distinct y-axis scales
X_TSM <- ts(frequency = 12, start = c(2011, 1))
Y_2330 <- ts(frequency = 12, start = c(2011, 1))
returns <- cbind(X_TSM, Y_2330)
# assign the "rainfall" series to the y2 axis
library(dygraphs)
dygraph(returns) %>%
  dyAxis("y", label = "X_TSM") %>%
  dyAxis("y2", label = "Y_2330", independentTicks = TRUE) %>%
  dySeries("Y_2330",axis = 'y2')
dySeries(drawPoints = TRUE, pointShape = "square", color = "blue")
#.....
dygraph(Reg_XY_data, main = "Regression")%>%
  dyAxis("y", label = "X_TSM", independentTicks = TRUE)%>%
  dyAxis("y2", label = "Y_2330 " , independentTicks = TRUE) %>%
  dySeries("Y_2330", axis=('y2'))
#=========================沒成功================================
#[散佈圖 scatter plot]
#<法一>
scatter_plot <- ggplot(removed_data, aes(x = X_TSM, y = Y_2330)) +
  geom_point()
scatter_plot

#<法二>
ggplot(removed_data, aes(x = X_TSM, y = Y_2330)) +
  geom_point(color = "red", shape = 8)+

#[pp-plot] 略

#[qq-plot]
#<法一>
p <- ggplot(removed_data , aes(sample=X_TSM))+
  geom_qq() + geom_qq_line()
ggplotly(p)

#<法二>
qqnorm(removed_data$X_TSM, main = "台積電ADR股價報酬率 Q-Q Plot",
       xlab = "Theoretical Quantiles", ylab = "Sample Quantiles",
       plot.it = TRUE, datax = FALSE)
qqline(removed_data$X_TSM)

qqnorm(removed_data$Y_2330, main = "台灣台積電股價報酬率 Q-Q Plot",
       xlab = "Theoretical Quantiles", ylab = "Sample Quantiles",
       plot.it = TRUE, datax = FALSE)
qqline(removed_data$Y_2330)

#qqline(y, datax = FALSE, distribution = qnorm,
#probs = c(0.25, 0.75), qtype = 7, ...)
#qqplot(x, y, plot.it = TRUE,
#xlab = deparse1(substitute(x)),
#ylab = deparse1(substitute(y)), ...)

#------------------------------------------
#補充:
switched.lm <- lm(X_TSM~Y_2330, data = removed_data)
summary(switched.lm)

#殘差獨立性檢定
library(car)
durbinWatsonTest(switched.lm)

#殘差變異數同質性檢定
library(lmtest)
library(zoo)
ncvTest(switched.lm)
bptest(switched.lm)
