import matplotlib.pyplot as plt
import numpy as np
import os
import re
import bisect

FILE_PATHS = [
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\300K_R995,1_Omh\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=7K\Spectrum\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=9K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=12K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=15K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=17K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=19K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=20K5\Spectra\1p\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=20K5\Spectra\5p\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=22K\Spectra\1p\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=22K\Spectra\3p\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=23K5\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=25K5\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=28K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=33K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=40K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=50K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=62K9\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=70K2\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=80K\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=81K7\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=100K\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=120K\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=150K4\Spectra\FFT LV.txt',
    r'C:\Users\Владимир\Desktop\Department_Project\Averievite data\Tp=197K7\Spectra\FFT LV.txt"'
]

def extract_temperature(file_path):
    """Извлекает температуру из имени файла"""
    match = re.search(r'(?:Tp=)?(\d+\.?\d*)K', file_path, re.IGNORECASE)
    return float(match.group(1)) if match else None

def read_data(filename):
    """Чтение данных из файла"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            next(f)  # Пропускаем заголовок
            for line in f:
                line = line.strip().replace(',', '.')
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        data.append((float(parts[0]), float(parts[1])))
    except Exception as e:
        print(f"Ошибка чтения {filename}: {str(e)}")
    return data

def trim_auto(data, threshold_percent=5):
    """Автоматическая обрезка данных по порогу"""
    if not data:
        return []
    
    real_abs = [abs(d[1]) for d in data]
    max_val = max(real_abs)
    threshold = max_val * threshold_percent / 100
    
    start = next(i for i, v in enumerate(real_abs) if v >= threshold)
    end = len(real_abs) - next(i for i, v in enumerate(reversed(real_abs)) if v >= threshold) - 1
    
    return data[start:end+1]

def calculate_stats(data):
    """Расчет статистических характеристик"""
    if not data:
        return {}
    
    freqs = np.array([d[0] for d in data])
    real = np.array([d[1] for d in data])
    weights = np.abs(real)
    
    if np.sum(weights) == 0:
        return {}

    # Находим частоту, соответствующую максимальному значению
    max_idx = np.argmax(real)
    max_freq = freqs[max_idx]
    
    mean = np.average(freqs, weights=weights)
    variance = np.average((freqs - mean)**2, weights=weights)
    
    return {
        'max_value': real[max_idx],
        'max_freq': max_freq,
        'mean': mean,
        'variance': variance,
        'std_dev': np.sqrt(variance)
    }

def save_plot(frequencies, real_parts, max_freq, max_val, file_path):
    """Сохранение графика с отметкой максимума"""
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, real_parts, 'b-', linewidth=1)
    
    # Добавляем маркер для максимума
    plt.plot(max_freq, max_val, 'ro', label=f'Max: {max_val:.2f} @ {max_freq:.2f} Hz')
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Real Part')
    plt.title(f'Spectrum (T = {extract_temperature(file_path)} K)')
    plt.grid(True)
    plt.legend()
    
    plot_filename = os.path.splitext(file_path)[0] + '_plot.png'
    plt.savefig(plot_filename)
    plt.close()
    print(f"График сохранен: {plot_filename}")

if __name__ == "__main__":
    with open("spectrum_results.txt", "w", encoding="utf-8") as result_file:
        # Заголовок таблицы с фиксированной шириной
        header = f"{'T(K)':<8}{'Max_Value':>15}{'Max_Freq':>15}{'Mean':>12}{'Variance':>12}{'Std_Dev':>12}"
        result_file.write(header + "\n")
        result_file.write("-"*len(header) + "\n")
        
        for file_path in FILE_PATHS:
            file_path = file_path.strip('"')
            temp = extract_temperature(file_path)
            
            if not temp:
                print(f"Не удалось определить температуру для {file_path}")
                continue
            
            data = read_data(file_path)
            if not data:
                print(f"Нет данных в {file_path}")
                continue
            
            auto_data = trim_auto(data)
            if not auto_data:
                print(f"Не удалось обрезать данные в {file_path}")
                continue
            
            freqs = [d[0] for d in auto_data]
            real = [d[1] for d in auto_data]
            stats = calculate_stats(auto_data)
            
            if not stats:
                print(f"Не удалось рассчитать статистику для {file_path}")
                continue
            
            # Сохраняем график с отметкой максимума
            save_plot(freqs, real, stats['max_freq'], stats['max_value'], file_path)
            
            # Запись результатов с фиксированной шириной столбцов
            result_file.write(
                f"{temp:<8.1f}{stats['max_value']:>15.6f}"
                f"{stats['max_freq']:>15.6f}{stats['mean']:>12.6f}"
                f"{stats['variance']:>12.6f}{stats['std_dev']:>12.6f}\n"
            )
            
            print(f"Обработан T = {temp} K: Max {stats['max_value']:.2f} @ {stats['max_freq']:.2f} Hz")

    print("\nОбработка завершена. Результаты в spectrum_results.txt")

##############################################################################
# Закомментированный код для ручной обрезки (раскомментировать при необходимости)
##############################################################################
'''
def trim_manual(data, freq_start, freq_end):
    """
    Ручная обрезка данных по заданному диапазону частот
    """
    if not data:
        return []
    
    freqs = [d[0] for d in data]
    start_idx = find_closest_index(freqs, freq_start)
    end_idx = find_closest_index(freqs, freq_end)
    
    # Убедимся, что start_idx <= end_idx
    if start_idx > end_idx:
        start_idx, end_idx = end_idx, start_idx
    
    return data[start_idx:end_idx+1]

def find_closest_index(frequencies, target_freq):
    """
    Находит индекс ближайшего значения частоты в массиве
    Использует бинарный поиск для эффективности
    """
    pos = bisect.bisect_left(frequencies, target_freq)
    if pos == 0:
        return 0
    if pos == len(frequencies):
        return len(frequencies) - 1
    before = frequencies[pos-1]
    after = frequencies[pos]
    return pos-1 if abs(before - target_freq) < abs(after - target_freq) else pos

def process_manual_trim(file_path, result_file):
    """
    Обработка файла с ручной обрезкой (дополнительная функция)
    """
    data = read_data(file_path)
    if not data:
        return
    
    freqs = [d[0] for d in data]
    real = [d[1] for d in data]
    
    # Показываем график для определения границ обрезки
    plt.figure(figsize=(12, 6))
    plt.plot(freqs, real, 'b-', linewidth=1)
    plt.xlabel('Frequency')
    plt.ylabel('Real Part')
    plt.title(f'Определение границ обрезки: {os.path.basename(file_path)}')
    plt.grid(True)
    plt.show()
    
    # Запрос границ обрезки у пользователя
    print(f"Доступный диапазон частот: {min(freqs):.6f} - {max(freqs):.6f}")
    while True:
        try:
            f1 = float(input("Введите начальную частоту: ").replace(',', '.'))
            f2 = float(input("Введите конечную частоту: ").replace(',', '.'))
            if min(freqs) <= f1 <= max(freqs) and min(freqs) <= f2 <= max(freqs):
                break
            print("Ошибка: частоты должны быть в доступном диапазоне!")
        except ValueError:
            print("Некорректный ввод! Используйте точку как разделитель")
    
    # Выполняем ручную обрезку
    manual_data = trim_manual(data, f1, f2)
    
    # Рассчитываем статистику
    stats = calculate_stats(manual_data)
    
    # Записываем результаты
    if stats:
        result_file.write(
            f"{extract_temperature(file_path)}\t{stats['max_value']:.6f}\t"
            f"{stats['mean']:.6f}\t{stats['variance']:.6f}\t"
            f"{stats['std_dev']:.6f}\n"
        )
'''