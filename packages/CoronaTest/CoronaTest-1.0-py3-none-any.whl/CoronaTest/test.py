from pathlib import Path

script_location = Path(__file__).absolute().parent
ques_loc = script_location / "ques_pickle"
sugg_loc = script_location / "sugg_pickle"

from ConvertVal import converter
import pickle
with open(ques_loc, "rb") as p:
    data_list = pickle.load(p)

with open(sugg_loc, "rb") as p:
    suggestions = pickle.load(p)

def pick_ques(index):
    import random
    q = data_list[index].split("&&")
    return q[random.randint(0,len(q)-1)]

yn_ques_map = {
    "yes": ["হ্যাঁ","হ্যা","জ্বী", "খেয়েছি", "খাইছি", "খেয়েছিলাম","আচ্ছা", "আছে", "আছেতো", "অনেক আছে", "অনেক", "আছে", "অল্প আছে", "ইয়েস", "হুম", "হ", "হু", "hm", "hum", "hu", "yes", "চাই", "চাচ্ছি", "সিউর", "sure"],
    "no" : ["না", "নাই", "একদম নাই", "নাইতো", "ছিলো", "ছিল" ,"এখন নাই", "নেই", "নেইতো", "ছিলোত", "নো", "ন", "নানা", "no", "na", "never", "নেভার", "নেবার", "খাইনি ", "চাইনা"],
    "male" : ["পুরুষ", "মেইল", "মেল", "মরদ ফুয়া", "ছেলে", "পুলা", "পোয়া", "পোলা", "মদ্দা", "নর", "বাবা", "মামা", "চাচা", "ছাত্র", "পুত", "male" ],
    "female" : ["ফিমেল", "মহিলা", "মাইয়া", "মেয়ে", "লেরকি", "নারী", "ছাত্রী", "আন্টি", "মামি", "মা", "ভাবী", "বোদি", "বেটী", "বেটি", "অন্যান্য", "other", "আদারস", "female"]
    }

bangla_number = ['০', '১','২', '৩','৪',
                 '৫','৬', '৭', '৮', '৯']

english_number = ['0', '1', '2', '3', '4',
                  '5', '6', '7', '8', '9']
def BTE(original):
    converted = ""
    for character in str(original):
        if character in bangla_number:
            converted+=english_number[bangla_number.index(character)]
        else:
            converted+=character
    return converted

def get_prob(data):
    
    Fever103 = 25   #>103
    Fever100 = 20   #>100
    Fever99 = 15    #>=99

    body_hot = 15
    Dry_Cough = 10
    Fatigue   = 7
    Sputum_Production = 7
    Shortness_Breath = 15
    Shortness_Breath_Disease = 7
    Pain = 10
    Smoking = 6
    Sore_throat = 15
    Headache = 7
    Chills = 7
    Vomiting = 6
    Nasal_Congestion = 6
    Diarrhoea = 12
    Past_Disease = 10
    TRAVEL = 5
    day = 20

    sums = 0
    fever_flag=0


    if data[2] > 103:
        sums+=Fever103
        fever_flag=1
    elif data[2]>100:
        sums+=Fever100
        fever_flag=1
    elif data[2]>=99:
        sums+=Fever99
        fever_flag=1
    else:
        sums+=0

    if fever_flag==1 and data[3]==1 and data[4]==0:
        sums+=15
    if fever_flag==1 and data[3]==1 and data[4]==1:
        sums -= 10
    if fever_flag==0 and data[5]==1:
        sums+=body_hot
        
        
        
        
    sums+= \
    data[6]*Dry_Cough+     \
    data[7]*Fatigue+  \
    data[8]*Sputum_Production+    \
    data[9]*Shortness_Breath+ \
    data[10]*Shortness_Breath_Disease+    \
    data[11]*Pain+     \
    data[12]*Smoking+ \
    data[13]*Sore_throat+     \
    data[14]*Headache+    \
    data[15]*Chills+    \
    data[16]*Vomiting+    \
    data[17]*Nasal_Congestion+    \
    data[18]*Diarrhoea+     \
    data[19]*Past_Disease+     \
    data[20]*TRAVEL+    \
    data[21]*day
        
    return sums


def StartTest(i, data,status, flag, sugg_index, lst, check):
    if check=="fdk":
        answer = 0
    if check=="tdk":
        answer = 1
	if check=="sdk":
		answer = 0
	

    
    if check == 'sdk':
        check = converter.convert(6, data)
    else: check = converter.convert(i-1, data)

    if status == True and check != 'sdk':
        if check == "fdk":
            output = pick_ques(24)
            i=50
            status = False
            return 50, output,status, flag, sugg_index,lst, check
        else:
            output = pick_ques(i)
            status = False
        
    elif check == 'sdk':
        output = pick_ques(23)
        i = i - 2
        status = True
        
    elif i == 3:
        if check == "fdk":
            i = i + 3
            output = pick_ques(i)
            lst[i] = answer
        else:
            output = pick_ques(i)
            lst[i] = answer
            flag = True
    elif i == 5:
        if check == "fdk":
            i = i + 2
        output = pick_ques(i)
        lst[i] = answer
    elif i==23:
        corona_mat = lst[:2]+lst[3:]
        result = get_prob(corona_mat)
        if 0<result<=10:
            sugg_index = 0
        elif 10<result<=40:
            sugg_index = 2
        elif 40<result<=90:
            sugg_index = 4
        elif 90<result<=130:
            sugg_index = 6
        else:
            sugg_index = 8
        output = suggestions[sugg_index]
        sugg_index+=1
        
    elif i==24:
        if check == "tdk":
            output = suggestions[sugg_index]
        else:
            output = "ধন্যবাদ"
        
        
        
    else:
        output = pick_ques(i)
        lst[i] = answer


    if flag == True and i == 5:
        i += 1
        flag = False

    i = i + 1
    return i, output,status, flag, sugg_index,lst, check