import matplotlib.pyplot as plt
import pandas as pd

# Загрузка данных
data = pd.read_csv(r'C:\Users\Владимир\Desktop\Department_Project\Analysis_Results\results.txt', 
                  sep='|', skipinitialspace=True)

# Удаление возможных пробелов в именах столбцов
data.columns = data.columns.str.strip()

# Сортировка данных по температуре (столбец 'T(K)')
data = data.sort_values('T(K)')

# Создание фигуры с 4 подграфиками
fig, axs = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Анализ данных резонансных кривых', fontsize=16)

# График 1: MaxValue vs T(K) с погрешностями
axs[0, 0].errorbar(data['T(K)'], data['MaxValue(a.u.)'], yerr=data['ErrMax(a.u.)'], 
                  fmt='o-', markersize=5, capsize=3, color='tab:blue')
axs[0, 0].set_xlabel('Температура, K')
axs[0, 0].set_ylabel('Максимальное значение, a.u.')
axs[0, 0].set_title('Зависимость максимального значения от температуры')
axs[0, 0].grid(True, linestyle='--', alpha=0.6)

# График 2: MaxFreq vs T(K) с погрешностями
axs[0, 1].errorbar(data['T(K)'], data['MaxFreq(MHz)'], yerr=data['ErrFreq(MHz)'], 
                  fmt='o-', markersize=5, capsize=3, color='tab:orange')
axs[0, 1].set_xlabel('Температура, K')
axs[0, 1].set_ylabel('Частота в максимуме, MHz')
axs[0, 1].set_title('Зависимость частоты в максимуме от температуры')
axs[0, 1].grid(True, linestyle='--', alpha=0.6)

# График 3: Variance vs T(K) с погрешностями
axs[1, 0].errorbar(data['T(K)'], data['Variance(kHz²)'], yerr=data['ErrVar(kHz²)'], 
                  fmt='o-', markersize=5, capsize=3, color='tab:green')
axs[1, 0].set_xlabel('Температура, K')
axs[1, 0].set_ylabel('Дисперсия, kHz²')
axs[1, 0].set_title('Зависимость дисперсии от температуры')
axs[1, 0].grid(True, linestyle='--', alpha=0.6)

# График 4: NoiseVar vs T(K) в логарифмическом масштабе
axs[1, 1].errorbar(data['T(K)'], data['NoiseVar(a.u.²)'], 
                  fmt='o-', markersize=5, color='tab:red')
axs[1, 1].set_xlabel('Температура, K')
axs[1, 1].set_ylabel('Дисперсия шума, a.u.²')
axs[1, 1].set_yscale('log')
axs[1, 1].set_title('Зависимость дисперсии шума от температуры (лог. масштаб)')
axs[1, 1].grid(True, linestyle='--', alpha=0.6, which='both')

plt.tight_layout()
plt.show()