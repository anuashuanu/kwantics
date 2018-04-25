# -*- coding: utf-8 -*-

def Decimal_Word(Number):
    Word=["शून्य", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ"]
    print('Number is decimal')
    Number=Number-int(Number)
    Number='%.3f' % Number
    Number=str(Number).split('.')[1]
    float_word=''
    lst = [int(i) for i in str(Number)]
    for i in lst:
        float_word=float_word+' '+Word[i]
    return float_word

def Integer_Word(Number):
    Number=int(Number)
    LowDigit = ["", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ", "दस", "ग्यारह", "बारह", "तेरह", "चौदह",
                "पन्द्रह", "सोलह", "सत्रह", "अठारह", "उन्नीस", "बीस", "इक्कीस", "बाईस", "तेईस", "चौबीस", "पच्चीस",
                "छब्बीस", "सत्ताईस", "अट्ठाईस", "उनतीस", "तीस", "इकतीस", "बत्तीस", "तैंतीस", "चौंतीस", "पैंतीस",
                "छत्तीस", "सैंतीस", "अड़तीस", "उनतालीस", "चालीस", "इकतालीस", "बयालीस", "तैंतालीस", "चौवालीस",
                "पैंतालीस", "छियालीस", "सैंतालीस", "अड़तालीस", "उनचास", "पचास", "इक्यावन", "बावन", "तिरेपन", "चौवन",
                "पचपन", "छप्पन", "सत्तावन", "अट्ठावन", "उनसठ", "साठ", "इकसठ", "बासठ", "तिरेसठ", "चौंसठ", "पैंसठ",
                "छियासठ", "सड़सठ", "अड़सठ", "उनहत्तर", "सत्तर", "इकहत्तर", "बहत्तर", "तिहत्तर", "चौहत्तर", "पचहत्तर",
                "छिहत्तर", "सतहत्तर", "अठहत्तर", "उनासी", "अस्सी", "इक्यासी", "बयासी", "तिरासी", "चौरासी", "पचासी",
                "छियासी", "सत्तासी", "अट्ठासी", "नवासी", "नब्बे", "इक्यानबे", "बानबे", "तिरानबे", "चौरानबे", "पंचानबे",
                "छियानबे", "सत्तानबे", "अट्ठानबे", "निन्यानबे"]

    HigherDigit = ["सौ", "हजार", "लाख", "करोड़", ]

    Tenth=Number%100
    if Tenth>0:
        TenthWord=LowDigit[Tenth]
    else:
        TenthWord=LowDigit[0]

    Hundred=int((Number%1000-Number%100)/100)
    if Hundred>0:
        HundredWord= LowDigit[Hundred] +' '+HigherDigit[0]
    else:
        HundredWord=LowDigit[0]

    Thousand=int((Number%100000-Number%1000)/1000)
    if Thousand>0:
        ThousandWord= LowDigit[Thousand] +' '+ HigherDigit[1]
    else:
        ThousandWord=LowDigit[0]

    Lakh=int((Number%10000000-Number%100000)/100000)
    if Lakh>0:
        LakhWord= LowDigit[Lakh] +' '+ HigherDigit[2]
    else:
        LakhWord=LowDigit[0]

    Crore=int((Number%1000000000-Number%10000000)/10000000)
    if Crore>0:
        CroreWord= LowDigit[Crore] +' '+ HigherDigit[3]
    else:
        CroreWord=LowDigit[0]

    Word=CroreWord+' '+LakhWord+' '+ThousandWord+' '+HundredWord+' '+TenthWord
    return Word

if __name__ == "__main__":
    Number=12345.00
    Integer=Integer_Word(Number)
    if Number!=int(Number):
        Decimal = Decimal_Word(Number)
        NumWord=Integer+str('दशमलव')+Decimal
    else:
        NumWord = Integer
    print(NumWord)

