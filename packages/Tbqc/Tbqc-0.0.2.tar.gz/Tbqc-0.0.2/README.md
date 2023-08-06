![Github](https://img.shields.io/github/license/dapingtai/Tw-Bartender-Quizdata-crawler?style=for-the-badge)
![pypi](https://img.shields.io/pypi/v/Tbqc?style=for-the-badge)
# Tw-Bartender-Quizdata-crawler
The crawler of Taiwan bartender make you get newest quiz data
# Qucik Start
```
pip install Tbqc
import Tbqc
```
# Usage
- Step1: Crawler Taiwan Bartender Quiz Table with `pdfextrat()`
```
table_df = Tbqc.pdfextrat(url="http://www.fsvs.ks.edu.tw/ezfiles/0/1001/img/58/206002.pdf", page=34)
```
- Step2: Transform Clean Table with `table_transform()`
```
new_table_df = Tbqc.table_transform(table_df)
```
- Bonus: Crawler & Transform Mutiplepage Data with `multiplepage()`

**Choose usage**

page_start/page_end=47: Crawler PDF page start to end
```
all_table_df = Tbqc.multiplepage(page_start=34, page_end=47, url="http://www.fsvs.ks.edu.tw/ezfiles/0/1001/img/58/206002.pdf")
```
![image](https://github.com/dapingtai/Tw-Bartender-Quizdata-crawler/blob/master/coding_record/CleanTable.jpg)
- Step3: Putting in postgreSQL with `to_postgresql()`

 Inputdata: Your transform data making by step2
 
 User: Your postgreSQL username
 
 Password: Your postgreSQL password
 
 Host/Port: Your postgreSQL IP/Port
 
 DB: Your DB name
```
Tbqc.to_postgresql(inputdata=new_table_df, user, password, host, port, db)
```
![image](https://github.com/dapingtai/Tw-Bartender-Quizdata-crawler/blob/master/coding_record/Result.jpg)
