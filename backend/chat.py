import db
from cbr_tieuhoa import TuVan

class Chat():
    # tv = TuVan()
    def __init__(self):
        #để t add code lên git
        self.list_question = {"type":"","benh":"","question":[]}
        self.list_option= ["Mô tả","Triệu chứng", "Nguyên nhân", "Cách phòng ngừa"]
        self.pick = 0
        self.tv = TuVan()
    
    def reset(self):
        self.list_question = {"type":"","benh":"","question":[]}
        self.list_option= ["Mô tả","Triệu chứng", "Nguyên nhân", "Cách phòng ngừa"]
        self.pick = 0
        self.tv = TuVan()
    def hello(self):
        ops =[]
        ops.append("Xem thông tin các bệnh")
        ops.append("Tư vấn bệnh")
        return ops
    
    def xu_li_xem_thong_tin(self, msg):
        if self.list_question["benh"] == "" :
            self.list_question["benh"] = msg
            print("benh: ", self.list_question["benh"])
        else:                     
            pass
        return self.list_option            
            
        
    def xu_li_tu_van(self, msg):
        list_answer = []
        if msg == "Tư vấn bệnh":
            self.tv.get_cauHoi()
            # self.list_question["benh"] = msg
            self.tv.get_list_answer()
            list_answer = self.tv.list_option
        elif msg =='Dừng':
            list_answer = []
            
        else:
            self.tv.get_cauHoi()
            print('jshdjkshdkshdkhsdkshds',self.tv.cauHoi)
            self.tv.get_list_answer()
            list_answer = self.tv.list_option   
            # self.list_question["benh"] = msg         
            if self.tv.id_question!='Q_error' and self.tv.id_question!='Q1' and msg !='Tiếp tục' :
                self.tv.list_id_question.append(self.tv.id_question)        
        return list_answer  
    
    
    
    def get_list_disease(self):
        df = db.get_danh_sach_benh()
        return df
    
    def get_trieu_chung_by_benh(self, benhid):
        trieu_chung = db.get_trieu_chung_by_benh(benhid)
        result = self.handle_list_return(trieu_chung)
        return result
    
    def handle_list_return(self, list_return:list):
        result = ""
        for item in list_return:
            result += "\n"+"- "+item 
        return result
    
    def split_text(self, text):
        ls_split = text.split("|")
        # print(text)
        result = self.handle_list_return(ls_split)
        return result
    
    def get_option(self, msg):
        #truyen vao input la cau tra loi
        ops = []
        df_disease = self.get_list_disease()
        list_disease = df_disease['ten'].values

        # if msg == 'Xem thông tin các bệnh' and self.pick == 0:
        if msg == 'Xem thông tin các bệnh' and self.tv.new_turn ==True :
            self.list_question['type'] = msg
            ops= list(self.get_list_disease()['ten'])
            # self.pick = 1
            return ops
        elif msg == 'Tư vấn bệnh':
            # print("tuvan")
            # self.tv = TuVan()
            self.list_question['type'] = msg
            self.pick = 1
            self.tv.start_turn()
            ops = self.xu_li_tu_van(msg)
            print(ops)
            return ops
        elif  msg in list_disease and self.list_question['type'] == 'Xem thông tin các bệnh':
            ops = self.xu_li_xem_thong_tin(msg)
            return ops
        elif msg in self.list_option and self.list_question['type'] == 'Xem thông tin các bệnh':
            return self.list_option
        elif msg != 'Xem thông tin các bệnh' and msg != "Tư vấn bệnh" and self.tv.new_turn ==True and msg!='Dừng':
            ops = self.hello()
            return ops
         
        if self.list_question["type"] == "Xem thông tin các bệnh":
            ops = self.xu_li_xem_thong_tin(msg)
        elif self.list_question["type"] == "Tư vấn bệnh":
            if self.tv.new_turn ==False:
                ops = self.xu_li_tu_van(msg)
        
        print(ops)
        return ops
    
    
    def get_response(self, msg):
        #truyen vao input la cau tra loi
        df_disease = self.get_list_disease()
        list_disease = df_disease['ten'].values
        if  msg in list_disease  and self.list_question['type'] == 'Xem thông tin các bệnh':
            if msg in list_disease:
                self.list_question['benh'] =msg
                return "Hãy chọn các lựa chon sau về "+msg
            
       
        elif msg == 'Xem thông tin các bệnh' and self.pick==0 and self.tv.new_turn ==True: 
            self.pick=1
            self.list_question['benh'] =[]
            self.list_question['type'] = msg
            return "Xem thông tin các bệnh sau"
        elif msg == "Tư vấn bệnh":
            self.pick =1
            self.list_question['type'] = msg
            self.tv.finish_turn()
            self.tv.start_turn()
            self.tv.get_cauHoi()
            cauhoi = self.tv.cauHoi 
            return cauhoi
        elif self.list_question["type"] == 'Xem thông tin các bệnh' and self.list_question["benh"] != "" and msg in self.list_option:
            df = self.get_list_disease()
            df = df[df['ten'] == self.list_question["benh"]]
            if msg == "Mô tả":
                return df['moTa'].values[0]
            elif msg == "Triệu chứng":
                return self.get_trieu_chung_by_benh(df['id'].values[0])
            elif msg == "Nguyên nhân":
                return self.split_text(df['nguyenNhan'].values[0])
            elif msg == "Cách phòng ngừa":
                return self.split_text(df['nganNgua'].values[0])            
        elif msg != 'Xem thông tin các bệnh' and msg != "Tư vấn bệnh" and self.tv.new_turn ==True and msg!='Dừng':
            self.reset()
            return "Chào bạn, mình là Sam - chuyên gia tiêu hóa của bạn. Hãy lựa chọn các hỗ trợ sau"
        # elif  self.list_question["type"] == 'Tư vấn bệnh' and self.list_question["benh"] != "":
        elif  self.list_question["type"] == 'Tư vấn bệnh' :
            chuanDoan = self.tv.process(msg)
            print (chuanDoan)
            # if self.tv.id_question!='Q_error' :
            #     self.tv.list_id_question.append(self.tv.id_question) 
            print(self.list_question)
           
            print(self.tv.id_question)
            print(self.tv.dict_cbr)
            dict_allCBR = self.tv.get_diemCBR_AllTrieuChung_daXet()
            max_cbr = max(list(dict_allCBR.values()))
            print("-----HHIHIHIHI  ",max_cbr)
            print("Message: ", msg)
            print(self.tv.list_id_question)
            self.tv.get_cauHoi()
            self.tv.get_list_answer()
            list_answer = self.tv.list_option
            cauhoi = self.tv.cauHoi       
          
            print("cauhoi: ", cauhoi)
            print("Phương án", list_answer)     
            if chuanDoan!= "Error" and chuanDoan!= None:
                self.pick = 0
                return (chuanDoan)
            elif self.tv.new_turn ==False:
                return cauhoi   
            # elif chuanDoan ==None:
            #     print(self.tv.)

            # else:   
            #     return cauhoi
        self.pick =0
        return None
    
