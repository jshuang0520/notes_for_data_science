# python 整理資料的使用技巧


### 簡介

這是[黃聖翔](https://www.facebook.com/profile.php?id=100001348802783)在用 Python 清理資料常用的方法，[網頁版](https://jshuang0520.github.io/notes_for_data_science/)


### Compilor Online

[repl.it](https://repl.it/languages)

#### [repl.it - python 3](https://repl.it/repls/TragicCulturedOutcome)

---

### 大綱

 - [Dataframe - 指定匯入EXCEL的特定表單_選取特定欄位_變更欄位名稱_排列欄位順序](http://nbviewer.jupyter.org/github/jshuang0520/notes_for_data_science/blob/master/python_指定匯入EXCEL的特定表單_選取特定欄位_變更欄位名稱_排列欄位順序.ipynb)

 - [Jupyter Notebook Sublime指令 安裝流程](http://nbviewer.jupyter.org/github/jshuang0520/notes_for_data_science/blob/master/Sublime指令安裝法.ipynb)
 
 - [Sublime Text 基礎熱鍵表 1](https://www.camdemy.com/media/6211)
 
 - [Sublime Text 基礎熱鍵表 2](http://resuly.me/2017/11/03/jupyter-config-for-windows/)


#### Python - MySQL

 - [Python connect to MySQL with XAMPP](http://nbviewer.jupyter.org/github/jshuang0520/notes_for_data_science/blob/master/2018.06.20_Python_connect_to_MySQL_with_XAMPP.ipynb)

 - [Python connect to MySQL : SQL DDL + web crawler (104 & Google Map)](http://nbviewer.jupyter.org/github/jshuang0520/notes_for_data_science/blob/master/web_crawler_for_104_job_2018.12.16_ver_2.ipynb)

 - [Python connect to MySQL : SQL statement + web crawler (overstock.com)](http://nbviewer.jupyter.org/github/jshuang0520/notes_for_data_science/blob/master/topline_2019.01.09_demo.ipynb)


#### Python - Flask - MySQL

- [Using Flask on Python 3 with MySQL](https://sweetcode.io/flask-python-3-mysql/)
- [上面的HTML語法有誤 參考這篇GitHub](https://github.com/devopper/python3-mysql-example)




---
## 機器學習評估指標

### [如何辨別機器學習模型的好壞？ 秒懂 Confusion Matrix](https://www.ycc.idv.tw/confusion-matrix.html)

### [Evaluation Metric : 分類模型](https://medium.com/ai%E5%8F%8D%E6%96%97%E5%9F%8E/evaluation-metrics-%E5%88%86%E9%A1%9E%E6%A8%A1%E5%9E%8B-ba17ad826599)

![img_confusion_matrix](https://www.ycc.idv.tw/media/mechine_learning_measure/mechine_learning_measure.001.jpeg)

![img_Type_I_II_error](https://www.ycc.idv.tw/media/mechine_learning_measure/mechine_learning_measure.002.jpeg)

![img_indicators](https://www.ycc.idv.tw/media/mechine_learning_measure/mechine_learning_measure.003.jpeg)


![img_precision_recall](https://pic3.zhimg.com/80/v2-76b9176719868e9b85bedf5192e722d3_720w.jpg)
> [Precision Recall](https://www.zhihu.com/question/30643044)


![img_timimg](https://www.ycc.idv.tw/media/mechine_learning_measure/mechine_learning_measure.004.jpeg)

![img_evaluate](https://www.ycc.idv.tw/media/mechine_learning_measure/mechine_learning_measure.006.jpeg)

---
## 演算法

## 分類

### SVM 

1. [SVM1](https://www.itread01.com/content/1544347819.html) 2. [SVM2](https://www.zhihu.com/question/21094489)

### xgboost

1. [XGBoost – A Scalable Tree Boosting System：Kaggle 競賽最常被使用的演算法之一](https://medium.com/@cyeninesky3/xgboost-a-scalable-tree-boosting-system-%E8%AB%96%E6%96%87%E7%AD%86%E8%A8%98%E8%88%87%E5%AF%A6%E4%BD%9C-2b3291e0d1fe)
2. [作者 Youngmi huang : Participate in data science field, fascinated by something new in FinTech. (Current: investment decision making, risk and fraud field with ML, Past: NLP)](https://medium.com/@cyeninesky3)


### catboost

- CatBoostClassifier : 

1. [原理介紹](http://datacruiser.io/2019/08/19/DataWhale-Workout-No-8-CatBoost-Summary/) 2. [fit](https://catboost.ai/docs/concepts/python-reference_catboostclassifier_fit.html) 3. [Usage examples1](https://catboost.ai/docs/concepts/python-usages-examples.html), [Usage examples2](https://stackoverflow.com/questions/54437646/catboost-precision-imbalanced-classes)

---

## 回歸

---

## 分群

---

## 降維


### LDA (Linear Discriminant Analysis - 線性 ; 監督式學習)

- 用途 : 

1. 分類(Classification)

2. 降維(dimension reduction)，此方法LDA會有個別稱區別分析特徵萃取(Discriminant Analysis Feature Extraction, DAFE)

3. [機器學習: 降維(Dimension Reduction)- 線性區別分析(Linear Discriminant Analysis)](https://medium.com/@chih.sheng.huang821/%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E9%99%8D%E7%B6%AD-dimension-reduction-%E7%B7%9A%E6%80%A7%E5%8D%80%E5%88%A5%E5%88%86%E6%9E%90-linear-discriminant-analysis-d4c40c4cf937)

此LDA(Linear Discriminant Analysis)並非主題模型的LDA(Latent Dirichlet Allocation)

### PCA (非線性 ; 非監督式學習)

1. [機器/統計學習:主成分分析(Principal Component Analysis, PCA) - medium](https://medium.com/@chih.sheng.huang821/%E6%A9%9F%E5%99%A8-%E7%B5%B1%E8%A8%88%E5%AD%B8%E7%BF%92-%E4%B8%BB%E6%88%90%E5%88%86%E5%88%86%E6%9E%90-principle-component-analysis-pca-58229cd26e71)

2. [作者 Tommy Huang : 怕老了忘記這些吃飯的知識，開始寫文章記錄機器/深度學習相關內容](https://medium.com/@chih.sheng.huang821)




---

#### Python - Recommendation System 筆記

- [協同過濾 - User-Based, Item-Based](http://nbviewer.jupyter.org/github/jshuang0520/notes_for_data_science/blob/master/recommendation_system.ipynb)

---

## 文字分析

1. [以 jieba 與 gensim 探索文本主題：五月天人生無限公司歌詞分析 (II) - Youngmi huang](https://medium.com/pyladies-taiwan/%E4%BB%A5-jieba-%E8%88%87-gensim-%E6%8E%A2%E7%B4%A2%E6%96%87%E6%9C%AC%E4%B8%BB%E9%A1%8C-%E4%BA%94%E6%9C%88%E5%A4%A9%E4%BA%BA%E7%94%9F%E7%84%A1%E9%99%90%E5%85%AC%E5%8F%B8%E6%AD%8C%E8%A9%9E%E5%88%86%E6%9E%90-ii-fdf5d3708662)

### LDA (Latent Dirichlet Allocation)

1. [通俗的說LDA ----Latent Dirichlet Allocation](https://blog.csdn.net/qq_25439417/article/details/82217333)

2. [用scikit-learn學習LDA主題模型](https://blog.csdn.net/weixin_33811961/article/details/90126968)

3. [生成模型與文字探勘：利用 LDA 建立文件主題模型 - 大鼻觀點](https://taweihuang.hpd.io/2019/01/10/topic-modeling-lda/)

---
## 演算法程式實踐

- [基本程式實踐](https://www.itread01.com/content/1543203132.html)

---

## IT邦幫忙 鐵人競賽好文

### 資料分析相關

- [R 語言使用者的Python 學習筆記](https://ithelp.ithome.com.tw/users/20103511/ironman/1077)

### 爬蟲

- [爬蟲始終來自於墮性](https://ithelp.ithome.com.tw/users/20107159/ironman/1325)

- 591 出租網爬蟲
1. [591 出租網爬蟲](https://ithelp.ithome.com.tw/articles/10191506)
2. [Python 中讓 urllib 使用 cookie 的方法](https://blog.m157q.tw/posts/2018/01/06/use-cookie-with-urllib-in-python/)

關鍵點1:
j.setCookie(request.cookie('urlJumpIp=23'), url);
參考: https://ithelp.ithome.com.tw/articles/10191506

關鍵點2:
cookies = dict(urlJumpIp='3') 
resp = res.get(url_1,headers=headers1, cookies=cookies)
參考: https://blog.m157q.tw/posts/2018/01/06/use-cookie-with-urllib-in-python/


### ELK
- [ELK - Elasticsearch, Logstash, Kibana](https://ithelp.ithome.com.tw/users/20103420/ironman/1046?page=1)


---

## 參考公開 kernel

- [Kaggle_Titanic_Top3%_Medium -  YLTsai0609](https://gist.github.com/YLTsai0609/617ef7bd66b140089f9c314ce0db4bc5#file-kaggle_titanic_top3-_medium-ipynb)

