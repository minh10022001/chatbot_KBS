import pickle
import re 
import string


class Input():
    def __init__(self):
        self.dict_keyword = {
    'Q1':['cứng','nhỏ','bình thường','lỏng'],
    'Q2':['đen','tối','máu','phân','bình thường'],
    'Q3':['trên','thượng vị','trái','phải','gần rốn','đau','đau bụng','dưới rốn','không'],
    'Q4':['Có','Không','bụng','đầy'],
    'Q5':["Có",'Không','chán ăn','ăn'],
    'Q6':['Có','Không','buồn nôn','nôn'],
    'Q7':['Có','Không','ợ','ợ chua','ợ hơi','ợ nóng'],
    'Q8':['Có','Không','sốt'],
    'Q9':['Có','không','sút','sụt','cân'],
    'Q10':['nhiều','ít','lần','tuần','không'],
    'Q11':['da','bỏng','loét','ngứa','vàng','bong'],
    'Q12':['Có','Không','hậu môn','nóng','rát'],
    'Q13':['Có','Không','nhiều','ít','nước bọt','bình thường'],
    'Q14':['Có','Không','thừa','lòi','thịt'],
    'Q15':['Có','Không','hơi thở','hôi','bình thường'],
    'Q16':['Có','không','sưng','bình thường','phình'],
        }
        self.dict_question = dict_question = {
    'Q1':'Trạng trái phân của bạn ?',
    'Q2':"Màu phân của bạn?",
    'Q3':"Vị trí mà bạn cảm thấy đau bụng?",
    'Q4':"Bạn có cảm thấy bị đầy bụng không?",
    'Q5':"Bạn có cảm thấy chán ăn không?",
    'Q6':"Bạn có cảm thấy buồn nôn không?",
    'Q7':"Bạn có ợ hơi, ợ nóng hay ợ chua không?",
    'Q8':"Bạn có sốt không?",
    'Q9':"Bạn có thấy cân nặng của mình bị sụt nhanh không?",
    'Q10':"Tần suất đi đại tiện của bạn lúc này?",
    'Q11':"Tình trạng da của bạn?",
    'Q12':"Bạn có cảm thấy hậu môn nóng rát không ?",
    'Q13':"Miệng có tiết nhiều nước bọt không?",
    'Q14':"Hậu môn có xuất hiện mô thừa không?",
    'Q15':"Hơi thở của bạn có mùi hôi không?",
    'Q16':"Bụng bạn có bị sưng không?"
}
    def no_accent_vietnamese(self,s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s
    def remove_punctuation(self,word):
        result = word.translate(str.maketrans(dict.fromkeys(string.punctuation)))
        return result
    def clean_up_pipeline(self,sentence):
            # cleaning_utils = [remove_punctuation]
            # for o in cleaning_utils:
            #     sentence = o(sentence)
            # return sentence
        return self.remove_punctuation(sentence)
  
    def predict(self, id_question,input_user):
        flat = False
        question = self.dict_question[id_question]
        keywords = self.dict_keyword[id_question] 
        for keyword in keywords:
            if keyword.lower() in input_user.lower():
                flat = True
                break
        if flat == False:
            return None
          #load model naive_bayes.GaussianNB
        filename = 'C:/Users/Admin/Downloads/kbs_chatbot-main/kbs_chatbot-main/backend/kbs.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        #load svd - giảm chiều 
        filename = 'C:/Users/Admin/Downloads/kbs_chatbot-main/kbs_chatbot-main/backend/svd.sav'
        svd = pickle.load(open(filename, 'rb'))
        #load tfidf 
        filename = 'C:/Users/Admin/Downloads/kbs_chatbot-main/kbs_chatbot-main/backend/tfidf.sav'
        tfidf = pickle.load(open(filename, 'rb'))
        #load labelencoder
        filename = 'C:/Users/Admin/Downloads/kbs_chatbot-main/kbs_chatbot-main/backend/label.sav'
        labelencoder = pickle.load(open(filename, 'rb'))
        label = labelencoder.classes_
        input_model = question + " " + input_user
        input_model = self.no_accent_vietnamese(input_model.lower())
        input_model = self.clean_up_pipeline(input_model)
        input_model = tfidf.transform([input_model])
        input_model = svd.transform(input_model)
        output = loaded_model.predict(input_model)
        return label[output][0]
