import numpy as np
from datetime import datetime
import pandas as pd


def bookrecommend(user_id, gender) :
    Library = pd.read_csv('C:/Users/Master/.spyder-py3/book_data_fin_3.csv', encoding='cp949') #전체 책 데이터
    Library_book_borrow = pd.read_csv('C:/Users/Master/.spyder-py3/회원대출0411.csv') #전체 대출 내역
    book_borrow_user_sort = Library_book_borrow.sort_values(by = ['member_id']) #사용자이름으로 정렬
    book_borrow_user_birth_sort = book_borrow_user_sort.sort_values(by = ['birthday']) #생일로 정렬 
    book_borrow_user_birth_sort['year'] = book_borrow_user_birth_sort['birthday'].str.split('-').str[0].astype(int) #년도 추출 (나이 구분)
    book_borrow_user_birth_year = book_borrow_user_birth_sort.sort_values(by='year') #년도 추가 


    def categories(file) :
        categories = np.zeros((len(file),10))
        for n in range(len(file)) : #카테고리 데이터에 대한 One-Hot Encoding
            if file[n] == '총류' :
                categories[n,0] = 1
            elif file[n] == '자연과학' :
                categories[n,1] = 1
            elif file[n] == '사회과학' :
                categories[n,2] = 1
            elif file[n] == '기술과학' :
                categories[n,3] = 1
            elif file[n] == '종교' :
                categories[n,4] = 1
            elif file[n] == '역사' :
                categories[n,5] = 1
            elif file[n] == '철학' :
                categories[n,6] = 1
            elif file[n] == '문학' :
                categories[n,7] = 1
            elif file[n] == '예술' :
                categories[n,8] = 1
            elif file[n] == '언어' :
                categories[n,9] = 1

        return categories   

    def gender(file) :
        gender = np.zeros((len(file),3))
        for n in range(len(file)) : #성별 데이터에 대한 One-Hot Encoding
            if file[n] == 'M' :
                gender[n,0] = 1
            elif file[n] == 'F' :
                gender[n,1] = 1
            else : #성별정보 없음
                gender[n,2] = 1
            return gender   

    def borrow(file) :
        borrow = np.zeros((len(file),2))
        for n in range(len(file)) : #대출 데이터에 대한 One-Hot Encoding
            if file[n] == 'F' :
                borrow[n,0] = 1
            elif file[n] == 'T' :
                borrow[n,1] = 1
            return borrow  

    def age(file) :
        age = np.zeros((len(file),9))
        corrent_year = datetime.now().year
        for n in range (len(file)) : #나이 데이터에 대한 One-Hot Encoding
            age_s = corrent_year - file[n] #나이 계산    
            if (0 < age_s <= 9) : # 0 ~ 9세
                age[n,0] = 1
            elif (9 < age_s <= 19): # 10 ~ 19세
                age[n,1] = 1
            elif (19 < age_s <= 29): # 20 ~ 29세
                age[n,2] = 1
            elif (29 < age_s <= 39): # 30 ~ 39세
                age[n,3] = 1
            elif (39 < age_s <= 49): # 40 ~ 49세
                age[n,4] = 1
            elif (49 < age_s <= 59): # 50 ~ 59세
                age[n,5] = 1
            elif (59 < age_s <= 69): # 60 ~ 69세
                age[n,6] = 1
            elif (69 < age_s ): # 70세 이상
                age[n,7] = 1
            else : #나이 정보 없음
                age[n,8] = 1

        return age   

   
    delete = book_borrow_user_birth_year.drop_duplicates('isbn')
    delete.reset_index(drop = False, inplace = True)

    duplicates = pd.merge(Library, delete['isbn'], on ='isbn')

    def delete_(data) :
        result = Library[~Library['isbn'].isin(data['isbn'])].dropna(axis = 'index', how = 'any', subset =['isbn'])
        return result 
    
    result = delete_(duplicates)
    result.reset_index(drop = False, inplace = True)



    Library_book_gender_year_add = pd.merge(Library, book_borrow_user_birth_year[['isbn','gender','year']], on ='isbn',how = 'left')
    Library_book_gender_year_add.reset_index(drop = False, inplace = True)

    Library_book_borrow_add = pd.merge(Library, book_borrow_user_birth_year[['isbn','lend_status']], on ='isbn',how = 'left')
    Library_book_borrow_add['lend_status']  = Library_book_borrow_add['lend_status'].fillna('F')
    Library_book_borrow_add = Library_book_borrow_add.drop_duplicates('isbn')
    Library_book_borrow_add.reset_index(drop = False, inplace = True)


#member_id => key 로 한것 
    grouped_dict = dict(tuple(book_borrow_user_birth_year.groupby('member_id')))
    keys = [group for group in grouped_dict]
    for i in range(len(keys)) :
        grouped_dict[keys[i]].reset_index(drop = False, inplace = True)

    us1 = user_id
    if us1 in grouped_dict :
        user_info = grouped_dict[us1]
        if(user_info['gender'][0] == 'M') :
            recommendations =pd.read_csv('C:/Users/Master/.spyder-py3/cos_2_100.csv', encoding='cp949') #전체 책 데이터
        else :
            recommendations =pd.read_csv('C:/Users/Master/.spyder-py3/cos_1_010.csv', encoding='cp949') #전체 책 데이터
    else : 
        
        if(gender == 'M') :
            recommendations =pd.read_csv('C:/Users/Master/.spyder-py3/cos_2_100.csv', encoding='cp949') #전체 책 데이터
        else :
            recommendations =pd.read_csv('C:/Users/Master/.spyder-py3/cos_1_010.csv', encoding='cp949') #전체 책 데이터






#isbn을 기준으로 중복된 책 제거 
    delete1 = recommendations.drop_duplicates('isbn')
    
#유저의 대출기록에서 중복된 정보 제거 
    delete2 = book_borrow_user_birth_year.drop_duplicates('isbn')

#isbn을 기준으로 현재 대출 상태 정보를 추가 
    delete1 = pd.merge(delete1, delete2[['isbn','lend_status']], on ='isbn',how = 'left')
    delete1['lend_status']  = delete1['lend_status'].fillna('F')

#유저의 대출기록에서 상태를 가져옴으로 대출기록이 존재하지 않는 경우 lend_state를 부여 
    if us1 in grouped_dict :
        result = delete1[~delete1['isbn'].isin(user_info['isbn'])].dropna(axis = 'index', how = 'any', subset =['isbn'])
    else :
        result = delete1

    sorted_result = result.sort_values(by='similarity', ascending = False)


    max_value = sorted_result.iloc[0]['similarity']
    max_columns = sorted_result[sorted_result['similarity'] == max_value]       

    if(len(max_columns) < 3) :
        random_column = max_columns
    else :                
        random_column = max_columns.sample(3)         
  
    return random_column
qwert123 = bookrecommend(10000,'F')
print(qwert123)

