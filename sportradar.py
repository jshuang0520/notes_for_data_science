import time
import re
import pymysql
import os
import requests
import json

from concurrent.futures import ThreadPoolExecutor, as_completed

from fuzzywuzzy import fuzz

from aws_xray_sdk.core import xray_recorder

import json, xmltodict
import boto3
from apollo_config import apollo_config
      
             
start_time = time.time()

s3 = boto3.resource('s3')
cluster = os.environ['ENV_STAGE']
bucket = os.environ['BUCKET_NAME']

content_object = s3.Object(bucket, 'lambda/' + cluster + '/job-config-apollo-' + cluster + '.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
config = json.loads(file_content)
app_id = config ['app_id']
config_server_url = config ['config_server']         
        
Dict = apollo_config (app_id = app_id, cluster = cluster, config_server_url = config_server_url)



def lambda_handler(event, context):

    foreign_languages = ['ZhCN', 'JaJP', 'KoKR']
    print("foreign_languages : ", foreign_languages)
    
    categoryName = event['categoryName'] # 在 cloudWatch 建 add Target :   
    print("categoryName : ", categoryName)
    lang = event['lang']
    print(lang)
     
    host = Dict['hostM'] # "tx-alpha.cluster-..."
    # user = Dict['DB_MYSQL_USERNAME'] # Dict['db_username']
    # password = Dict['DB_MYSQL_PASSWORD'] # Dict['db_password']

    def connection(host):
        return pymysql.connect(host=host,
                               user='', # 'collectionuser'
                               password='', # 'Collection000000user'
                               db='collection',
                               use_unicode=True,
                               charset="utf8")
        







    if categoryName == "Tennis" :
        category_id = [2]
        category_name = "Tennis"
    
    if categoryName == "Football" :
        category_id = [1]
        category_name = "Football"
    if categoryName == "Cricket" :
        category_id = [4]
        category_name = "Cricket"
    if categoryName == "Basketball" :
        category_id = [21] 
        category_name = "Basketball"
    if category_id == "eSport" :   # betMarathon 網頁呈現該項目的名稱大小寫
        category_id = [10] 
        category_name = "eSport"
    
    
    
    
    # Betradar_API
    if lang == 'EnUS'  :
        languageCode = 'EnUS'
        lang_url = 'en' # Betradar_API 網頁呈現該項目的名稱
        new_Events_table = 'sportBetfairTranslations' + languageCode # 取代原本要看 sportBetfairEvents 的中文欄位
    
    if lang == 'ZhCN'  :
        languageCode = 'ZhCN'
        lang_url = 'zh' # Betradar_API 網頁呈現該項目的名稱
        new_Events_table = 'sportBetfairTranslations' + languageCode # 取代原本要看 sportBetfairEvents 的中文欄位
        unicode_of_lang = r"[\u4e00-\u9fff]+"
    if lang == 'JaJP'  :
        languageCode = 'JaJP'
        lang_url = 'ja'
        new_Events_table = 'sportBetfairTranslations' + languageCode # 取代原本要看 sportBetfairEvents 的中文欄位
        unicode_of_lang = r"[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9fff\u3400-\u4dbf]+|[\u4e00-\u9fff]+"
    if lang == 'KoKR'  :
        languageCode = 'KoKR'
        lang_url = 'ko'  
        new_Events_table = 'sportBetfairTranslations' + languageCode # 取代原本要看 sportBetfairEvents 的中文欄位
        unicode_of_lang = r"[\uac00-\ud7a3]+|[\u4e00-\u9fff]+"
    
    def connection(host):
        return pymysql.connect(host=host,
                               user='',
                               password='',
                               db='collection',
                               use_unicode=True,
                               charset="utf8")
    
    # 從 SQL 選到 Python
    def read_sql_to_pyList(sql, x) :
        """
        x 要是 list 的形式喔，不然這裡參數的位置就要放 [x] 而不是 x
        """
                          #"snk-prod.cluster..."
        conn = connection(host)
        cur = conn.cursor()
    #   df = pd.read_sql(sql, conn).rename(columns = {"nameRe" : "NameRe"})
        cur.execute(sql, x)
        resultSet = list(cur.fetchall())
        conn.close()
        return resultSet
    
    
    # 從 SQL 選到 Python
    def read_sql_to_pyList_noVar(sql) : # df = pd.read_sql(sql, conn).rename(columns = {"nameRe" : "NameRe"})
        conn = connection(host)
        cur = conn.cursor()  
        cur.execute(sql)
        resultSet = list(cur.fetchall())
        conn.close()
        return resultSet
    
    
    # 從 Python 寫到 SQL
    def execute_sql(sql) :
                          #"snk-prod.cluster..."
        conn = connection(host)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()  
        conn.close()
    
    
    # 從 Python 寫到 SQL withPyVar
    def execute_sql_withPyVar(sql, x) :
        """
        x 要是 list 的形式喔，不然這裡參數的位置就要放 [x] 而不是 x
        """
                          #"snk-prod.cluster..."
        conn = connection(host)
        cur = conn.cursor()
        cur.execute(sql, x)
        conn.commit()  
        conn.close()
        
         
    def prettify_name_abbre(word) :
        if (category_name == 'Tennis') and (lang == "ZhCN") :
            word = re.sub("·[A-Z]+|[A-Z]+·|·\s+[A-Z]+|[A-Z]+\s+·|-[A-Z]+|[A-Z]+-|\.[A-Z]+|[A-Z]+\.", "", word)
            word = re.sub("-", "·", word)
            word = word.strip()
        return word
    def prettify_name_order(word) : 
        if category_name == 'Tennis' and (lang == "ZhCN") :
            if (len(word.split(",")) > 1)  or  (len(word.split("，")) > 1):
                seperators = [",", "，"]
                for seperator in seperators :
                    if len(word.split(seperator)) > 1 :
                        #print("seperator: ", seperator)
                        
                        # sportradar 原本的格式是： 姓lastname，名firstname
                        last_name = word.split(seperator)[0].strip()   # 姓 － Last Name、Surname、Family Name 
                        first_name = word.split(seperator)[-1].strip() # 名 － First Name、Forename、Given Name
                        name = first_name + "·" + last_name
                        #print("first_name: ", first_name)
                        #print("last_name: ", last_name)
                        return name
                        break
                    else :
                        pass
            else :
                return word
        else :
            return word
            
            
    # # 20190926 加
    # def abbre_competition(competition_2) : 

    #     #U23 -> U[0-9][0-9]
    #     competition_2 = re.sub("[A-Z][0-9]+", "", competition_2)
    #     #U-23 -> U-[0-9][0-9]
    #     competition_2 = re.sub("[A-Z]-[0-9]+", "", competition_2)
    #     #19/20 -> [0-9]/[0-9]
    #     competition_2 = re.sub("[0-9][0-9]/[0-9][0-9]", "", competition_2)
    #     #2019 -> [0-9][0-9][0-9][0-9]
    #     competition_2 = re.sub("[0-9][0-9][0-9][0-9]", "", competition_2)
    
    #     competition_2 = competition_2.strip() # 去除字串開頭和結尾的空白符 # competition_2 = [word.strip() for word in competition_2]
    #     competition_2 = re.sub(r' +', ' ', competition_2) # 只去除重複的空白符 # competition_2 = [" ".join(word.split()) for word in competition_2]
    
    
    
    #     if "单打" or "双打" in competition_2 :
    #         competition_2 = re.split('单打|双打', competition_2)[0]
    #         competition_2 = competition_2.strip()
    
    #     if "站" in competition_2 :
    #         if "单打" or "双打" in competition_2 :
    #             competition_2 = re.split('单打|双打', competition_2)[0]
    #             competition_2 = competition_2.strip() + "站"
    #         else :
    #             competition_2 = re.split('单打|双打', competition_2)[0]
    #             competition_2 = competition_2.strip()
    
    
    
    #     if "联赛杯" in competition_2 :
    #         competition_2 = re.split('联赛杯', competition_2)[0]
    #         competition_2 = competition_2.strip() + "联赛杯"
    
    #     if "杯赛" or "联赛" or "联杯" in competition_2 :
    #         if "杯赛" in competition_2 :
    #             competition_2 = re.split('杯赛', competition_2)[0]
    #             competition_2 = competition_2.strip() + "杯赛"
    #         if "联赛" in competition_2 :
    #             competition_2 = re.split('联赛', competition_2)[0]
    #             competition_2 = competition_2.strip() + "联赛"
    #         if "联杯" in competition_2 :
    #             competition_2 = re.split('联杯', competition_2)[0]
    #             competition_2 = competition_2.strip() + "联杯"
    
    
    #     if "杯" in competition_2 :
    #         competition_2 = re.split('杯', competition_2)[0]
    #         competition_2 = competition_2.strip() + "杯"
    
    #     if "赛" in competition_2 :
    #         competition_2 = re.split('赛', competition_2)[0]
    #         competition_2 = competition_2.strip() + "赛"
    
    #     competition_2 = competition_2.replace(". ", " ").replace(".杯", "杯").replace(".", " ")
    #     competition_2 = competition_2.replace("站站", "站").replace("杯杯", "杯").replace("赛赛", "赛")
    #     competition_2 = competition_2.replace("站 站", "站")
    #     competition_2 = re.sub(r' +', ' ', competition_2)
    #     competition_2 = competition_2.strip()
    
    #     return competition_2
    
    
    
    
    
    
    # 20190926 加 ; 20191001 改
    def abbre_competition(competition_2, lang) : 
    
        #U23 -> U[0-9][0-9]
        competition_2 = re.sub("[A-Z][0-9]+", "", competition_2)
        #U-23 -> U-[0-9][0-9]
        competition_2 = re.sub("[A-Z]-[0-9]+", "", competition_2)
        #19/20 -> [0-9]/[0-9]
        competition_2 = re.sub("[0-9][0-9]/[0-9][0-9]", "", competition_2)
        #2019 -> [0-9][0-9][0-9][0-9]
        competition_2 = re.sub("[0-9][0-9][0-9][0-9]", "", competition_2)
    
        competition_2 = competition_2.strip() # 去除字串開頭和結尾的空白符 # competition_2 = [word.strip() for word in competition_2]
        competition_2 = re.sub(r' +', ' ', competition_2) # 只去除重複的空白符 # competition_2 = [" ".join(word.split()) for word in competition_2]
    
        if lang == 'ZhCN' :
            單打 = "单打"
            雙打 = "双打"
            站 = "站"
    
            聯賽杯 = "联赛杯"
    
            杯賽 = "杯赛"
            聯賽 = "联赛"
            聯杯 = "联杯"
    
            杯 = "杯"
            賽 = "赛"
            
        if lang == 'JaJP' :
            單打 = "シングルス"
            雙打 = "ダブルス"
            站 = "          "
    
            聯賽杯 = "リーグカップ"
    
            杯賽 = "カップ"
            聯賽 = "リーグ"
            聯杯 = "カップ"
    
            杯 = "カップ"
            賽 = "          "
            
            
        if lang == 'KoKR' :
            單打 = "싱글"
            雙打 = "복식"
            站 = "역"
    
            聯賽杯 = "리그 컵"
    
            杯賽 = "          "
            聯賽 = "리그"
            聯杯 = "          "
    
            杯 = "컵"
            賽 = "경기"
            
    
        if 單打 or 雙打 in competition_2 :
            competition_2 = re.split(str(單打)+"|"+str(雙打), competition_2)[0]
            competition_2 = competition_2.strip()
    
        if 站 in competition_2 :
            if 單打 or 雙打 in competition_2 :
                competition_2 = re.split(str(單打)+"|"+str(雙打), competition_2)[0]
                competition_2 = competition_2.strip() + 站
            else :
                competition_2 = re.split(str(單打)+"|"+str(雙打), competition_2)[0]
                competition_2 = competition_2.strip()
    
    
    
        if 聯賽杯 in competition_2 :
            competition_2 = re.split(聯賽杯, competition_2)[0]
            competition_2 = competition_2.strip() + 聯賽杯
    
        if (杯賽 or 聯賽 or 聯杯) in competition_2 :
            if 杯賽 in competition_2 :
                competition_2 = re.split(杯賽, competition_2)[0]
                competition_2 = competition_2.strip() + 杯賽
            if 聯賽 in competition_2 :
                competition_2 = re.split(聯賽, competition_2)[0]
                competition_2 = competition_2.strip() + 聯賽
            if 聯杯 in competition_2 :
                competition_2 = re.split(聯杯, competition_2)[0]
                competition_2 = competition_2.strip() + 聯杯
    
        elif (杯賽 or 聯賽 or 聯杯) not in competition_2 :
            if 杯 in competition_2 :
                competition_2 = re.split(杯, competition_2)[0]
                competition_2 = competition_2.strip() + 杯
    
            if 賽 in competition_2 :
                competition_2 = re.split(賽, competition_2)[0]
                competition_2 = competition_2.strip() + 賽
    
        competition_2 = competition_2.replace(". ", " ").replace(str(".")+"|"+str(杯), 杯).replace(".", " ")
        competition_2 = competition_2.replace(str(站)+str(站), 站).replace(str(杯)+str(杯), 杯).replace(str(賽)+str(賽), 賽)
        competition_2 = competition_2.replace(str(站)+" "+str(站), 站)
        competition_2 = re.sub(r' +', ' ', competition_2)
        competition_2 = competition_2.strip()
    
        print("abbre_competition done!")
        return competition_2
    
    
    
    # DB
    # matchList_history
    # 2019.08.07 18:16 變更 : 把 ("Utd", "United") 改成 ("Utd", "")
    sql = """
    SELECT DISTINCT SBMS.betradarMatchId,
    
    
                    SBMS.betfairEventId,
                    C.name AS categoryName,
                    SBC.competitionName AS competitionName,
                    SBE.name AS eventName,
                    GROUP_CONCAT(DISTINCT SBSA.runnerName ORDER BY SBSA.sortPriority ASC SEPARATOR ' v ') AS selectionNames
    
    
    FROM collection.sportBetfairEvents SBE
    
    
    INNER JOIN collection.sportBetradarMatchSources SBMS
    ON SBE.eventId = SBMS.betfairEventId
    
    
    INNER JOIN marketMgmt.categories C
    ON C.id = SBE.categoryId
    
    
    
    INNER JOIN collection.sportBetfairMarketAlls SBMA
    ON SBE.categoryId = SBMA.categoryId
    AND SBE.eventId = SBMA.eventId
    AND SBMA.categoryId IN (%s)      /* SBMA.categoryId     是球種 - {1:Football, 2:Tennis, 4:Cricket, 21:Basketball} */
    AND SBMA.marketTypeId = 1         /* SBMA.marketTypeId 1 是主盤 */
    
    
    INNER JOIN collection.sportBetfairCompetitions SBC
    ON SBMA.competitionId = SBC.competitionId
    
    
    INNER JOIN collection.sportBetfairSelectionAlls SBSA
    ON SBSA.marketId = SBMA.marketId
    AND (SBSA.sortPriority = 1 OR SBSA.sortPriority = 2) # 20191001 加
    AND SBSA.runnerName != "The Draw" # NOT IN (58805, 60443)     /* SBSA.selectionId 58805, 60443 是平手 */
    
    INNER JOIN (SELECT DISTINCT eventId, """ + 'name'+languageCode + """, nameEnUS, isEventTranslateSucceed, isCompetitionTranslateSucceed FROM """ + new_Events_table + """) SBT
    ON SBE.eventId = SBT.eventId
    AND (SBT.isEventTranslateSucceed = 0 OR SBT.isEventTranslateSucceed = 2 OR SBT.isCompetitionTranslateSucceed = 0) /* isEventTranslateSucceed = 0 ; 舊的寫法: SBT.name''' + languageCode + ''' IS NULL --> 可能要把單引號改雙引號吧*/
    /* AND SBE.nameZhCN IS NULL */
    
    AND NOT EXISTS (SELECT tTRSR.categoryNameEnUS FROM tempTranslationSportradars tTRSR WHERE SBT.nameEnUS = tTRSR.eventNameEnUS AND tTRSR.isTranslateSucceed = 0 AND languageCode = %s)
    GROUP BY SBSA.marketId
    """  # WHERE nameCn IS NULL
    
    
    
    
    
    
    # INNER JOIN collection.sportBetfairSelectionAlls SBSA
    # ON SBSA.marketId = SBMA.marketId
    # AND SBSA.runnerName != "The Draw" # NOT IN (58805, 60443)     /* SBSA.selectionId 58805, 60443 是平手 */
    
    
    # GROUP BY SBSA.marketId
    
    
    
    
    sql_var_1 = []
    sql_var_1 = sql_var_1 + category_id # merge python list
    sql_var_1.append(languageCode)      # append element
    
    
    
    # # matchList_historyRe = read_sql_to_pyList(sql)["NameRe"]
    dbSummary = [i for i in read_sql_to_pyList(sql, sql_var_1)]
    # dbSummary = [i for i in read_sql_to_pyList(sql, category_id)]
    
    
    
    
    betradarMatchId_history = [i[0] for i in dbSummary]
    betfairEventId_history  = [i[1] for i in dbSummary]
    
    categoryName_history = [i[2] for i in dbSummary]
    competitionName_history = [i[3] for i in dbSummary]
    
    matchList_history = [i[4] for i in dbSummary]
    
    player_1_NamesEn_history = [i[5].split(' v ')[0] for i in dbSummary]
    player_2_NamesEn_history = [i[5].split(' v ')[1] for i in dbSummary]
    
    
    
    print("len(dbSummary): ", len(dbSummary))
    print("dbSummary: \n", dbSummary)
    
    dbSummary
    
    
    
    # from tqdm import tnrange, tqdm_notebook
    
    
    # start = datetime.datetime.now()
    # print(start)
    
    
    
    
    def get_data(lang) :
        
    
        
        eventIdName = []
        
        languageCode_list = []
        
        categoryName_dbEnUS = []
        competitionName_dbEnUS = []
        eventName_dbEnUS = []
        player_1Name_dbEnUS = []
        player_2Name_dbEnUS = []
        
        
        categoryName = []
        competitionName = []
        eventName = []
        team_homeName = []
        team_awayName = []
        
        
    #     # tx system
    #     host = "tx-alpha.cluster..."
        host = Dict['hostM']
        
        # 從 SQL 選到 Python
        def tx_read_sql_to_pyList(sql, x) :
            conn = connection(host)
            cur = conn.cursor()  
            cur.execute(sql, x)
            resultSet = list(cur.fetchall())
            conn.close()
            return resultSet
        sql = """
        SELECT DISTINCT eventNameEnUS
        FROM tempTranslationSportradars
        WHERE languageCode = %s
        """
        x = [languageCode]
        events_insert_already = [i[0] for i in tx_read_sql_to_pyList(sql, x)]
        
        cnt = 0
                    # 測試區
        #for i in tqdm_notebook(range(0, len(dbSummary))) : # len(dbSummary)
        for i in range(0, len(dbSummary)) : # len(dbSummary)
            
            
            matchId = betradarMatchId_history[i]
            eventId = betfairEventId_history[i]
            
            category_dbEnUS = categoryName_history[i]
            competition_dbEnUS = competitionName_history[i]
            event_dbEnUS = matchList_history[i]
            player_1_dbEnUS = player_1_NamesEn_history[i]
            player_2_dbEnUS = player_2_NamesEn_history[i]
            
            print("matchId: ", matchId, " eventId: ", eventId, " category_dbEnUS: ", category_dbEnUS, " competition_dbEnUS: ", competition_dbEnUS, " event_dbEnUS: ", event_dbEnUS, " player_1_dbEnUS: ", player_1_dbEnUS, " player_2_dbEnUS: ", player_2_dbEnUS)
            
            
            if event_dbEnUS not in events_insert_already :
    
                
                
                try :
                    # import requests

                    # https://www.bbb.games/exchange/{category}/{competitionId}/{eventId}

                    # 網址1 : {lang_url} {matchId}
                    url_1 = "https://lmt.fn.sportradar.com/common/" + lang_url + "/Etc:UTC/gismo/match_timelinedelta/" + str(matchId)
                    # 偽瀏覽器資訊
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
                                            #'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                    response = requests.get(url_1, headers = headers)
                    response.encoding = 'utf8'
                    json_text_1 = json.loads(response.text)


                    seasonid = json_text_1['doc'][0]['data']['match']['_seasonid']
                    sportid  = json_text_1['doc'][0]['data']['match']['_sid']

                    team_home = prettify_name_order(prettify_name_abbre(json_text_1['doc'][0]['data']['match']['teams']['home']['name'].encode('utf-8').decode('utf-8'))) #['mediumname']
                    team_away = prettify_name_order(prettify_name_abbre(json_text_1['doc'][0]['data']['match']['teams']['away']['name'].encode('utf-8').decode('utf-8'))) #['mediumname']

                    #------------------------------------------------------------------------
                    # url EnUS info - for the order the teams
                    url_1_urlEnUS = "https://lmt.fn.sportradar.com/common/" + 'en' + "/Etc:UTC/gismo/match_timelinedelta/" + str(matchId)
                    response = requests.get(url_1_urlEnUS, headers = headers)
                    response.encoding = 'utf8'
                    json_text_1_urlEnUS = json.loads(response.text)
                    team_home_urlEnUS = prettify_name_order(prettify_name_abbre(json_text_1_urlEnUS['doc'][0]['data']['match']['teams']['home']['mediumname'].encode('utf-8').decode('utf-8'))) #['name']
                    team_away_urlEnUS = prettify_name_order(prettify_name_abbre(json_text_1_urlEnUS['doc'][0]['data']['match']['teams']['away']['mediumname'].encode('utf-8').decode('utf-8'))) #['name']
                    #------------------------------------------------------------------------

                    # 網址2 : {lang_url} {matchId}
                    url_2 = "https://lmt.fn.sportradar.com/common/" + lang_url + "/Etc:UTC/gismo/match_info/" + str(matchId)

                    response = requests.get(url_2, headers = headers)
                    response.encoding = 'utf8'
                    json_text_2 = json.loads(response.text)


                    if json_text_2['doc'][0]['data']['season']['_id'] == str(seasonid) : # seasonid 為 string
                        competition = json_text_2['doc'][0]['data']['season']['name']
                        # competition = abbre_competition(competition)
                        competition = abbre_competition(competition, lang)
                    else :
                        competition = None
                    if (len(re.findall(unicode_of_lang, competition)) == 0) :
                        print("competition 抓到英文字")
                        competition = None



                    if json_text_2['doc'][0]['data']['sport']['_id'] == sportid :        # sportid  為 int
                        category = json_text_2['doc'][0]['data']['sport']['name']
                    else :
                        category = None






                    # For Tennis Doubles
                    if (category_dbEnUS == 'Tennis')  and  ("/" in event_dbEnUS) : 
                        # 這邊名稱比較完整，優先序 1
                        home = json_text_1['doc'][0]['data']['match']['teams']['home']['children']
                        away = json_text_1['doc'][0]['data']['match']['teams']['away']['children']
                        team_home = prettify_name_order(prettify_name_abbre(home[0]['name'].encode('utf-8').decode('utf-8'))) + "/" + prettify_name_order(prettify_name_abbre(home[1]['name'].encode('utf-8').decode('utf-8')))
                        team_away = prettify_name_order(prettify_name_abbre(away[0]['name'].encode('utf-8').decode('utf-8'))) + "/" + prettify_name_order(prettify_name_abbre(away[1]['name'].encode('utf-8').decode('utf-8')))

#                         # 如果優先序 1 的 4組姓名 任一個翻譯失敗了
#                         if (len(re.findall(unicode_of_lang, team_home.split("/")[0])) == 0 or len(re.findall(unicode_of_lang, team_home.split("/")[1])) == 0)  or  (len(re.findall(unicode_of_lang, team_away.split("/")[0])) == 0 or len(re.findall(unicode_of_lang, team_away.split("/")[1])) == 0) :
#                             # 這邊名稱比較差一點，優先序 2
#                             team_home = json_text_1['doc'][0]['data']['match']['teams']['home']['name'].encode('utf-8').decode('utf-8') #['mediumname']
#                             team_away = json_text_1['doc'][0]['data']['match']['teams']['away']['name'].encode('utf-8').decode('utf-8') #['mediumname']

#                             team_home = prettify_name_order(prettify_name_abbre(team_home.split("/")[0])) + "/" + prettify_name_order(prettify_name_abbre(team_home.split("/")[1]))
#                             team_away = prettify_name_order(prettify_name_abbre(team_away.split("/")[0])) + "/" + prettify_name_order(prettify_name_abbre(team_away.split("/")[1]))

                        # 2019.09.20 改
                        # 如果優先序 1 的 4組姓名 任一個翻譯失敗了
                        # 這邊名稱比較差一點，優先序 2
                        if (len(re.findall(unicode_of_lang, team_home.split("/")[0])) == 0 or len(re.findall(unicode_of_lang, team_home.split("/")[1])) == 0) :
                            team_home_2_info = json_text_1['doc'][0]['data']['match']['teams']['home']['name'].encode('utf-8').decode('utf-8') #['mediumname']
                            team_home = prettify_name_order(prettify_name_abbre(team_home_2_info.split("/")[0])) + "/" + prettify_name_order(prettify_name_abbre(team_home_2_info.split("/")[1]))
                        if (len(re.findall(unicode_of_lang, team_away.split("/")[0])) == 0 or len(re.findall(unicode_of_lang, team_away.split("/")[1])) == 0) :
                            team_away_2_info = json_text_1['doc'][0]['data']['match']['teams']['away']['name'].encode('utf-8').decode('utf-8') #['mediumname']
                            team_away = prettify_name_order(prettify_name_abbre(team_away_2_info.split("/")[0])) + "/" + prettify_name_order(prettify_name_abbre(team_away_2_info.split("/")[1]))

                    print("\n")
                    print("team_home: ", team_home)
                    print("team_away: ", team_away)
                    # 所有 events 都來檢查是不是翻譯不完全
#                     if (len(re.findall(unicode_of_lang, team_home)) == 0 or len(re.findall(unicode_of_lang, team_away)) == 0) :
#                         print("eventId: '%s', matchId: '%s'; eventName : '%s' - 翻譯不完全！" % (eventId, matchId, event_dbEnUS))
#                         cnt += 1


                    if (len(re.findall(unicode_of_lang, team_home)) == 0 or len(re.findall(unicode_of_lang, team_away)) == 0) :
                        print("eventId: '%s', matchId: '%s'; eventName : '%s' - 翻譯不完全！" % (eventId, matchId, event_dbEnUS))
                        cnt += 1
                        # 2019.09.20 加
                        if len(re.findall(unicode_of_lang, team_home)) == 0 :
                            team_home = None
                        if len(re.findall(unicode_of_lang, team_away)) == 0 :
                            team_away = None
                        if (len(re.findall(unicode_of_lang, team_home)) == 0 and len(re.findall(unicode_of_lang, team_away)) == 0) :
                            None
                        else :
                            eventIdName.append(eventId) # NOT dbSummary[i][0]
                            languageCode_list.append(languageCode) 
                            categoryName_dbEnUS.append(category_dbEnUS) 
                            competitionName_dbEnUS.append(competition_dbEnUS)
                            eventName_dbEnUS.append(event_dbEnUS)
                            player_1Name_dbEnUS.append(player_1_dbEnUS)
                            player_2Name_dbEnUS.append(player_2_dbEnUS)
                            #------------------------------------------------------------------------
                            categoryName.append(category)
                            competitionName.append(competition)
                            if float(fuzz.token_sort_ratio(team_home_urlEnUS, player_1_dbEnUS)) >= float(fuzz.token_sort_ratio(team_away_urlEnUS, player_1_dbEnUS)) :
                                eventName.append(None)
                                team_homeName.append(team_home)
                                team_awayName.append(team_away)
                            else :
                                print("inverse! eventId: %s, matchId: %s, event: %s" % (eventId, matchId, event_dbEnUS))
                                eventName.append(None)
                                team_homeName.append(team_away)
                                team_awayName.append(team_home)
                            #------------------------------------------------------------------------
                            
                        

                    else :

                        eventIdName.append(eventId) # NOT dbSummary[i][0]

                        languageCode_list.append(languageCode) 


                        categoryName_dbEnUS.append(category_dbEnUS) 
                        competitionName_dbEnUS.append(competition_dbEnUS)
                        eventName_dbEnUS.append(event_dbEnUS)
                        player_1Name_dbEnUS.append(player_1_dbEnUS)
                        player_2Name_dbEnUS.append(player_2_dbEnUS)


                        #------------------------------------------------------------------------
                        categoryName.append(category)
                        competitionName.append(competition)

                        if float(fuzz.token_sort_ratio(team_home_urlEnUS, player_1_dbEnUS)) >= float(fuzz.token_sort_ratio(team_away_urlEnUS, player_1_dbEnUS)) :
                            eventName.append(team_home + " v " + team_away)
                            team_homeName.append(team_home)
                            team_awayName.append(team_away)

                        else :
                            print("inverse! eventId: %s, matchId: %s, event: %s" % (eventId, matchId, event_dbEnUS))
                            eventName.append(team_away + " v " + team_home)
                            team_homeName.append(team_away)
                            team_awayName.append(team_home)
                        #------------------------------------------------------------------------


                except Exception as e :
                    print(e)
                    continue
            
            
            
    # #     df = pd.DataFrame({"eventId": eventIdName, "competition": competitionName, "event": eventName, "play1Name": team_homeName, "play2Name": team_awayName})    
    
    # # ---------------------------------------------------------    
    #     df = pd.DataFrame({"eventId": eventIdName, "categoryNameEnUS": category_dbEnUS, "categoryName": categoryName, "competitionNameEnUS": competitionName_dbEnUS, "competitionName": competitionName, "eventNameEnUS": eventName_dbEnUS, "event": eventName, "play1NameEnUS": player_1Name_dbEnUS, "play1Name": team_homeName, "play2NameEnUS": player_2Name_dbEnUS, "play2Name": team_awayName})
    # # ---------------------------------------------------------   
    
    # #     df.columns = df.columns.map(lambda x: str(x) + '_' + languageCode)
    # #     df = df.rename(columns = {'eventId' + '_' + languageCode: 'eventId'})
        
        
        
        
        
        
        
    #     for a,b,c,d,e, f,g,h,i,j in categoryName_dbEnUS, categoryName, competitionName_dbEnUS, competitionName, eventName_dbEnUS, eventName, player_1Name_dbEnUS, team_homeName, player_2Name_dbEnUS, team_awayName :
    #         x = zip(a,b,c,d,e,f,g,h,i,j)    
        
        return categoryName_dbEnUS, categoryName, competitionName_dbEnUS, competitionName, eventName_dbEnUS, eventName, player_1Name_dbEnUS, team_homeName, player_2Name_dbEnUS, team_awayName#, df
            
    
    
    
    
    
    """
    若 dbSummary = [] 
    就會遇到 UnboundLocalError: local variable 'category_dbEnUS' referenced before assignment
    """
    
    data = get_data(languageCode)
    
    categoryName_dbEnUS = data[0]
    categoryName = data[1]
    
    competitionName_dbEnUS = data[2]
    competitionName = data[3]
    
    eventName_dbEnUS = data[4]
    eventName = data[5]
    
    player_1Name_dbEnUS = data[6]
    team_homeName = data[7]
    
    player_2Name_dbEnUS = data[8]
    team_awayName = data[9]
    
    # df = data[10]
    
    print("len(categoryName_dbEnUS): ", len(categoryName_dbEnUS))
    
    
    
    
    
    # start = datetime.datetime.now()
    
    # from concurrent.futures import ThreadPoolExecutor, as_completed
    
    
    languageCode_list = [languageCode] * len(categoryName_dbEnUS)
    
    # print(1)
    def INSERT(languageCode_list, categoryName_dbEnUS, categoryName, competitionName_dbEnUS, competitionName, eventName_dbEnUS, eventName, player_1Name_dbEnUS, team_homeName, player_2Name_dbEnUS, team_awayName) :
        
        """
        https://stackoverflow.com/questions/48245853/threadpoolexecutor-with-all-params-from-two-lists
        """
        
        # # tx system
        # host = "tx-alpha.cluster..."
        host = Dict['hostM']
    
        def connection(host):
            return pymysql.connect(host=host,
                                   user='',
                                   password='',
                                   db='collection',
                                   use_unicode=True,
                                   charset="utf8")
        # 從 Python 寫到 SQL withPyVar
        def tx_execute_sql_withPyVar(sql, x) :
            """
            x 要是 list 的形式喔，不然這裡參數的位置就要放 [x] 而不是 x
            """
                              #"snk-prod.cluster..."
            conn = connection(host)
            cur = conn.cursor()
            cur.execute(sql, x)
            conn.commit()  
            conn.close()
        
    
        # tx system
        
    #     for i in range(0, len(categoryName_dbEnUS)) :
    #         x = [categoryName_dbEnUS[i], categoryName[i]]
    
    
        x = [languageCode_list, categoryName_dbEnUS, categoryName, competitionName_dbEnUS, competitionName, eventName_dbEnUS, eventName, player_1Name_dbEnUS, team_homeName, player_2Name_dbEnUS, team_awayName, 1]
        
        try :
            a = x[7] # player_1Name_dbEnUS
            b = x[9] # player_2Name_dbEnUS
            if a == b :
                print("db_selection_1 == db_selection_2 ! Didn't INSERT !, x: ", x)
            else:
                # if not in Re, then insert
                sql = """INSERT INTO tempTranslationSportradars (languageCode, categoryNameEnUS, categoryName, competitionNameEnUS, competitionName, eventNameEnUS, eventName, play1NameEnUS, play1Name, play2NameEnUS, play2Name, isTranslateSucceed)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                      """
                tx_execute_sql_withPyVar(sql, x)
                print("INSERT EnUS:", x)
        except :
            print("INSERT INTO temp fail", x)
    
            
    
    
    def main(languageCode_list, categoryName_dbEnUS, categoryName, competitionName_dbEnUS, competitionName, eventName_dbEnUS, eventName, player_1Name_dbEnUS, team_homeName, player_2Name_dbEnUS, team_awayName):
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(INSERT, languageCode_list, categoryName_dbEnUS, categoryName, competitionName_dbEnUS, competitionName, eventName_dbEnUS, eventName, player_1Name_dbEnUS, team_homeName, player_2Name_dbEnUS, team_awayName)
            for result in results:
                print(result)
        return results
    
    __name__ = "__main__"
    if __name__ == '__main__':
        
        try :
            # print(2)
            main(languageCode_list, categoryName_dbEnUS, categoryName, competitionName_dbEnUS, competitionName, eventName_dbEnUS, eventName, player_1Name_dbEnUS, team_homeName, player_2Name_dbEnUS, team_awayName)
            
            # 20191004加 call sp
            con = connection(host = Dict['hostM'])
            cursor = con.cursor(cursor = pymysql.cursors.DictCursor)
            cursor.execute("call uspJobUpdateTranslationFromSportradars")
            con.commit()
            con.close()
            #print("successfully execute sp")
            
        except Exception as e :
            # print(3)
            print(e)
    # else :
    #     print(4)
    
    # end = datetime.datetime.now()
    # print(end - start)
