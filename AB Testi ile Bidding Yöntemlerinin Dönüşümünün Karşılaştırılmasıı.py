# AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması

# İş Problemi

"""
Facebook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne alternatif olarak yeni bir teklif türü olan "average bidding"’i tanıttı.
Müşterilerimizden biri olan bombabomba.com, bu yeni özelliği test etmeye karar verdi ve average bidding'in maximum bidding'den daha
fazla dönüşüm getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.
A/B testi 1 aydır devam ediyor ve bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.
Bombabomba.com için nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.

"""
# Veri Seti Hikayesi

"""
Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları reklam sayıları gibi bilgilerin
yanı sıra buradan gelen kazanç bilgileri yer almaktadır. Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır.
Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer almaktadır.
******Kontrol grubuna Maximum Bidding, test grubuna Average Bidding uygulanmıştır.******

"""
# Proje Görevleri

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Görev 1
# Veriyi Hazırlama ve Analiz Etme

# Adım 1
# ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

# Adım 2
# Kontrol ve test grubu verilerini analiz ediniz.

# Adım 3
# Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.


df_control_group = pd.read_excel("dsmlbc_9_abdulkadir/Homeworks/hakan_erdem/3_Olcumleme_Problemleri/AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması/ab_testing.xlsx", sheet_name=0)
df_control_group.head()
df_control_group.shape

df_control_group.describe().T

df_test_group = pd.read_excel("dsmlbc_9_abdulkadir/Homeworks/hakan_erdem/3_Olcumleme_Problemleri/AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması/ab_testing.xlsx", sheet_name=1)
df_test_group.head()
df_test_group.shape
test_group.describe().T

df = pd.concat([df_control_group, df_test_group],keys=['df_control_group', 'df_test_group']).reset_index(0)
df.rename(columns={"level_0":"Groups"}, inplace=True)
df.head()

# Görev 2
# A/B Testinin Hipotezinin Tanımlanması

# Adım 1
# Hipotezi tanımlayınız.

# H0 : M1 = M2
# average bidding'in maximum bidding'den daha fazla dönüşüm getirip getirmemesi  Arasında İst. Ol. Anlamlı Farklılık Yoktur.
# H1 : M1!= M2
# average bidding'in maximum bidding'den daha fazla dönüşüm getirip getirmemesi  Arasında İst. Ol. Anlamlı Farklılık vardır.

# Adım 2
# Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.

df.groupby("Groups").agg({"Purchase": "mean"})

# Görev 3
# Hipotez Testinin Gerçekleştirilmesi

# Adım 1
# Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.

"""
Bunlar Normallik Varsayımı ve Varyans Homojenliğidir. Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.
Normallik Varsayımı :
H0: Normal dağılım varsayımı sağlanmaktadır. H1: Normal dağılım varsayımı sağlanmamaktadır.
p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ? Elde edilen p-value değerlerini yorumlayınız.
Varyans Homojenliği :
H0: Varyanslar homojendir.
H1: Varyanslar homojen Değildir.
p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını Purchase değişkeni üzerinden test ediniz. Test sonucuna göre normallik varsayımı sağlanıyor mu? Elde edilen p-value değerlerini yorumlayınız.

"""

# Varsayım Kontrolü

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df.loc[df["Groups"] == "df_control_group", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["Groups"] == "df_test_group", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# Sonuç: p-value <  0.05 olduğu  için H0 REDDEDILEMEZ. Dağılım normaldir.

# Varyans Homojenliği Varsayımı

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df.loc[df["Groups"] == "df_control_group", "Purchase"],
                           df.loc[df["Groups"] == "df_test_group", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# Sonuç: p-value <  0.05 olduğu  için H0 REDDEDILEMEZ. Varyanslar Homojendir.

#Adım 2
# Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

test_stat, pvalue = ttest_ind(df.loc[df["Groups"] == "df_control_group", "Purchase"],
                              df.loc[df["Groups"] == "df_test_group", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


# Adım 3
# Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

Sonuç: H0 hipotezi reddedilir.average bidding'in maximum bidding'den daha fazla dönüşüm getirip getirmemesi  Arasında İst. Ol. Anlamlı Farklılık vardır.

# Görev 4
# Sonuçların Analizi

# Adım 1
# Hangi testi kullandınız, sebeplerini belirtiniz.
ttest_ind kullanılmıştır. Çünkü varsayımlar sağlanmaktadır.

# Adım 2
# Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

Ortalamalara baktığımızda average bidding yönteminin daha kazançlı bir işlem olduğu ortaya  çıkmıştır.

df.groupby("Groups").agg({"Purchase": "mean"})
