from fuzzywuzzy import fuzz
#str_a='市委党校经管教研部'
#str_b='奥康德石油贸易集团公司企业管理部'
str_a='中山市公安局人事处干部调配科副科长'
str_b='中山市环境保护局人事处干部调配科科长'
print(fuzz.ratio(str_a,str_b))