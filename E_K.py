
import matplotlib.pyplot as plt

# Исходные данные
data = """
# 7K
# Матожидание частоты: 30.607614
# Дисперсия: 0.004127
# Матожидание частоты: 30.607983
# Дисперсия: 0.004228
# 9K
# # # # # # # # # Матожидание частоты: 30.606864
# # # # # # # # # Дисперсия: 0.004208
# # # # # # # # # Матожидание частоты: 30.607296
# # # # # # # # # Дисперсия: 0.004289
# 12K
# # # # # # # # Матожидание частоты: 30.605051
# # # # # # # # Дисперсия: 0.003709
# # # # # # # # Матожидание частоты: 30.604961
# # # # # # # # Дисперсия: 0.003751
# 15K
# # # # # # # Матожидание частоты: 30.609952
# # # # # # # Дисперсия: 0.003478
# # # # # # # Матожидание частоты: 30.611041
# # # # # # # Дисперсия: 0.003743
# 17K
# # # # # # # Матожидание частоты: 30.620543
# # # # # # # Дисперсия: 0.003096
# # # # # # # Матожидание частоты: 30.620750
# # # # # # # Дисперсия: 0.003148
# 19K
# # # # # # Матожидание частоты: 30.639667
# # # # # # Дисперсия: 0.002549
# # # # # # Матожидание частоты: 30.640036
# # # # # # Дисперсия: 0.002633
# 20.5K
# # # # # # Матожидание частоты: 30.653570
# # # # # # Дисперсия: 0.001461
# # # # # # Матожидание частоты: 30.653527
# # # # # # Дисперсия: 0.001496
# 22K
# # # # # Матожидание частоты: 30.681813
# # # # # Дисперсия: 0.001022
# # # # # Матожидание частоты: 30.681927
# # # # # Дисперсия: 0.001069
# 23.5K
# # # # Матожидание частоты: 30.699008
# # # # Дисперсия: 0.000539
# # # # Матожидание частоты: 30.698960
# # # # Дисперсия: 0.000589
# 28K
# # # Матожидание частоты: 30.716397
# # # Дисперсия: 0.000221
# # # Матожидание частоты: 30.716540
# # # Дисперсия: 0.000248
# 33K
# # Матожидание частоты: 30.720693
# # Дисперсия: 0.000198
# Матожидание частоты: 30.720414
# # Дисперсия: 0.000239
# 40K
# Матожидание частоты: 30.723243
# Дисперсия: 0.000184
# Матожидание частоты: 30.723134
# Дисперсия: 0.000213
# 50K
# Матожидание частоты: 30.724316
# Дисперсия: 0.000155
# Матожидание частоты: 30.724579
# Дисперсия: 0.000188
# 62.9K
# Матожидание частоты: 30.725008
# Дисперсия: 0.000159
# Матожидание частоты: 30.725386
# Дисперсия: 0.000207
# 70.2K
# Матожидание частоты: 30.724994
# Дисперсия: 0.000132
# Матожидание частоты: 30.724992
# Дисперсия: 0.000152
# 81.7K
# Матожидание частоты: 30.725429
# Дисперсия: 0.000143
# Матожидание частоты: 30.725958
# Дисперсия: 0.000181
# 100K
# Матожидание частоты: 30.726386
# Дисперсия: 0.000145
# Матожидание частоты: 30.725960
# Дисперсия: 0.000161
# 120K
# Матожидание частоты: 30.725779
# Дисперсия: 0.000105
# Матожидание частоты: 30.725124
# Дисперсия: 0.000126
# 150.4K
# Матожидание частоты: 30.727197
# Дисперсия: 0.000114
# Матожидание частоты: 30.726931
# Дисперсия: 0.000131
# 197.7K
# Матожидание частоты: 30.728354
# Дисперсия: 0.000066
# Матожидание частоты: 30.727780
# Дисперсия: 0.000081
"""

# Парсинг данных с учетом структуры
temps = []
auto_means = []
auto_vars = []
manual_means = []
manual_vars = []

current_temp = None
pair_counter = 0

for line in data.split('\n'):
    line = line.strip()
    if not line:
        continue
    
    if line.startswith('# ') and 'K' in line:
        # Обрабатываем новую температуру
        current_temp = float(line.split()[1].replace('K', '').replace('#', ''))
        temps.append(current_temp)
        pair_counter = 0
    elif 'Матожидание' in line:
        value = float(line.split(': ')[1])
        if pair_counter == 0:
            auto_means.append(value)
        else:
            manual_means.append(value)
    elif 'Дисперсия' in line:
        value = float(line.split(': ')[1])
        if pair_counter == 0:
            auto_vars.append(value)
        else:
            manual_vars.append(value)
        pair_counter += 1
        if pair_counter == 2:
            pair_counter = 0

# Проверяем размерности
print(f"Temps: {len(temps)}")
print(f"Auto means: {len(auto_means)}")
print(f"Manual means: {len(manual_means)}")

# Создание файлов
def write_file(filename, temps, means, vars):
    with open(filename, 'w', encoding='utf-8') as f:
        for t, m, v in zip(temps, means, vars):
            f.write(f"{t}K\n")
            f.write(f"Матожидание частоты: {m}\n")
            f.write(f"Дисперсия: {v}\n\n")

write_file('auto_trim.txt', temps, auto_means, auto_vars)
write_file('manual_trim.txt', temps, manual_means, manual_vars)

# Построение графиков
plt.figure(figsize=(12, 6))

# График матожидания
plt.subplot(1, 2, 1)
plt.plot(temps, auto_means, 'bo-', label='Автообрезание')
plt.plot(temps, manual_means, 'rs--', label='Ручная обрезка')
plt.xlabel('Температура (K)')
plt.ylabel('Матожидание частоты')
plt.title('Зависимость матожидания от температуры')
plt.grid(True)
plt.legend()

# График дисперсии
plt.subplot(1, 2, 2)
plt.plot(temps, auto_vars, 'bo-', label='Автообрезание')
plt.plot(temps, manual_vars, 'rs--', label='Ручная обрезка')
plt.xlabel('Температура (K)')
plt.ylabel('Дисперсия')
plt.title('Зависимость дисперсии от температуры')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

#FILE_PATHS = [
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\300K_R995,1_Omh\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=7K\Spectrum\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=9K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=12K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=15K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=17K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=19K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=20K5\Spectra\1p\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=20K5\Spectra\5p\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=22K\Spectra\1p\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=22K\Spectra\3p\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=23K5\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=25K5\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=28K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=33K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=40K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=50K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=62K9\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=70K2\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=80K\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=81K7\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=100K\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=120K\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=150K4\Spectra\FFT LV.txt',
    #r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=197K7\Spectra\FFT LV.txt"'
#]#