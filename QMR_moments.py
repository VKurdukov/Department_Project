import matplotlib.pyplot as plt
import bisect

def read_data(filename):
    """Чтение данных из файла с обработкой десятичных разделителей"""
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)  # Пропускаем заголовок
        for line in f:
            line = line.strip().replace(',', '.')
            if line:
                parts = line.split()
                if len(parts) == 3:
                    try:
                        freq = float(parts[0])
                        real = float(parts[1])
                        imag = float(parts[2])
                        data.append((freq, real, imag))
                    except ValueError:
                        continue
    return data

def plot_data(data, title='Данные'):
    """Визуализация данных с возможностью выбора диапазона"""
    if not data:
        return

    frequencies = [row[0] for row in data]
    real_parts = [row[1] for row in data]

    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, real_parts, 'b-', linewidth=1, label='Данные')
    plt.xlabel('Frequency')
    plt.ylabel('Real Part')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

def find_closest_index(data, target_freq):
    """Находит индекс ближайшего значения частоты в данных"""
    freqs = [row[0] for row in data]
    pos = bisect.bisect_left(freqs, target_freq)
    if pos == 0:
        return 0
    if pos == len(freqs):
        return len(freqs)-1
    before = freqs[pos-1]
    after = freqs[pos]
    return pos-1 if abs(before - target_freq) < abs(after - target_freq) else pos

def trim_data_manual(data, freq_start, freq_end):
    """Обрезка данных по заданным частотам"""
    if not data:
        return []
    
    start_idx = find_closest_index(data, freq_start)
    end_idx = find_closest_index(data, freq_end)
    
    if start_idx > end_idx:
        start_idx, end_idx = end_idx, start_idx
    
    return data[start_idx:end_idx+1]

def trim_data_auto(data, threshold_percent=5):
    """Автоматическая обрезка шумов по пороговому значению"""
    if not data:
        return []
    
    real_values = [abs(row[1]) for row in data]
    max_real = max(real_values)
    threshold = (threshold_percent/100) * max_real

    # Находим первый и последний индекс превышения порога
    start_idx = next(i for i, v in enumerate(real_values) if v >= threshold)
    end_idx = len(real_values) - next(i for i, v in enumerate(reversed(real_values)) if v >= threshold) - 1
    
    return data[start_idx:end_idx+1]

def calculate_statistics(data):
    """Расчет статистических характеристик"""
    if not data:
        return 0.0, 0.0
    
    total = sum(row[1] for row in data)
    if total == 0:
        return 0.0, 0.0
    
    mean = sum(row[0]*row[1] for row in data) / total
    variance = sum(row[1]*(row[0]-mean)**2 for row in data) / total
    
    return mean, variance

# Основной поток выполнения
filename = r'C:\Users\Владимир\Desktop\QMR\drive-download-20250326T154655Z-001\Tp=197K7\Spectra\FFT LV.txt'
data = read_data(filename)

# Шаг 0: Визуализация исходных данных
plot_data(data, 'Исходные данные')

# Шаг 1: Ручной выбор диапазона частот
print(f"Доступный диапазон частот: {data[0][0]:.6f} - {data[-1][0]:.6f}")
while True:
    try:
        f1 = float(input("Введите начальную частоту: ").replace(',', '.'))
        f2 = float(input("Введите конечную частоту: ").replace(',', '.'))
        if data[0][0] <= f1 <= data[-1][0] and data[0][0] <= f2 <= data[-1][0]:
            break
        print("Ошибка: частоты должны быть в доступном диапазоне!")
    except ValueError:
        print("Некорректный ввод! Используйте точку как разделитель")

trimmed_manual = trim_data_manual(data, f1, f2)
plot_data(trimmed_manual, 'После ручной обрезки')

# Шаг 2: Автоматическая очистка
trimmed_auto = trim_data_auto(trimmed_manual)
plot_data(trimmed_auto, 'После автоматической очистки')

# Шаг 3-4: Расчет и вывод статистики
mean1, variance1 = calculate_statistics(trimmed_auto)
mean2, variance2 = calculate_statistics(trimmed_manual)


print("\nРезультаты обработки:")
print(f"Исходное количество точек: {len(data)}")
print(f"После ручной обрезки: {len(trimmed_manual)}")
print(f"После автоматической очистки: {len(trimmed_auto)}")
print(f"Матожидание частоты: {mean1:.6f}")
print(f"Дисперсия: {variance1:.6f}")
print(f"Матожидание частоты: {mean2:.6f}")
print(f"Дисперсия: {variance2:.6f}")