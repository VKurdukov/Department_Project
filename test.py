import matplotlib.pyplot as plt
import numpy as np
import os
import re
from pathlib import Path

# Настройки
OUTPUT_DIR = "Analysis_Results"
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
    """Извлекает температуру из пути файла"""
    try:
        match = re.search(r'(?:Tp=)?(\d+[\.,]?\d*)K', file_path, re.IGNORECASE)
        return float(match.group(1).replace(',', '.')) if match else None
    except Exception as e:
        print(f"Ошибка извлечения температуры: {e}")
        return None

def read_data(filename):
    """Чтение данных из файла (Frequency в МГц, Real Part в a.u.)"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            next(f)  # Пропуск заголовка
            for line in f:
                line = line.strip().replace(',', '.')
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        freq_mhz = float(parts[0])  # Частота в МГц
                        real_part = float(parts[1])  # Амплитуда в a.u.
                        data.append((freq_mhz, real_part))
    except Exception as e:
        print(f"Ошибка чтения {filename}: {e}")
    return np.array(data)

def interactive_noise_selection(freq_mhz, values):
    """Интерактивный выбор границ шумовых областей"""
    plt.figure(figsize=(12, 6))
    plt.plot(freq_mhz, values, 'b-', label='Данные')
    plt.title("Выберите границы шумов:\nЛКМ - левая граница, ПКМ - правая\nEnter - подтвердить")
    plt.xlabel('Частота (МГц)')
    plt.ylabel('Амплитуда (a.u.)')
    plt.grid(True)
    
    selected_points = []
    
    def on_click(event):
        if event.inaxes != plt.gca(): return
        if event.button == 1:  # Левая кнопка - левая граница
            selected_points.append(event.xdata)
            plt.axvline(event.xdata, color='r', linestyle='--', alpha=0.7)
        elif event.button == 3:  # Правая кнопка - правая граница
            selected_points.append(event.xdata)
            plt.axvline(event.xdata, color='m', linestyle='--', alpha=0.7)
        plt.draw()
    
    def on_key(event):
        if event.key == 'enter':
            plt.close()
    
    plt.connect('button_press_event', on_click)
    plt.connect('key_press_event', on_key)
    plt.show()
    
    return sorted(selected_points[:2]) if len(selected_points) >= 2 else None

def calculate_stats(freq_mhz, values, noise_var):
    """Расчет статистик с правильными единицами"""
    weights = np.abs(values)
    sum_weights = np.sum(weights)
    
    # Основные статистики
    stats = {
        'max_value': np.max(values),  # В a.u.
        'max_freq': freq_mhz[np.argmax(values)],  # В МГц
        'mean': np.average(freq_mhz, weights=weights),  # В МГц
        'variance': np.average((freq_mhz - np.average(freq_mhz, weights=weights))**2, weights=weights) * 1e6,  # кГц²
        'noise_var': noise_var,  # В a.u.²
    }
    
    # Расчет погрешностей
    n = len(freq_mhz)
    df = np.mean(np.diff(freq_mhz))  # Шаг по частоте в МГц
    
    stats['err_max_freq'] = df / 2  # В МГц
    stats['err_mean'] = df / (2 * np.sqrt(n))  # В МГц
    stats['err_var'] = stats['variance'] / np.sqrt(n)  # В кГц²
    stats['err_max_value'] = np.sqrt(noise_var)  # В a.u.
    
    return stats

def process_file(file_path):
    """Обработка файла с интерактивным выбором шумов"""
    try:
        data = read_data(file_path)
        if data.size == 0:
            print(f"Пустой файл: {file_path}")
            return None
        
        freq_mhz = data[:,0]  # Частота в МГц
        vals = data[:,1]      # Амплитуда в a.u.
        
        # Интерактивный выбор границ
        bounds = interactive_noise_selection(freq_mhz, vals)
        if not bounds or len(bounds) < 2:
            print("Границы не выбраны! Использую автоматические (5% от максимума).")
            threshold = np.max(vals) * 0.05
            mask = vals >= threshold
            bounds = [freq_mhz[mask][0], freq_mhz[mask][-1]]
        
        # Визуализация выбранных областей
        plt.figure(figsize=(12, 6))
        plt.plot(freq_mhz, vals, 'b-', label='Данные')
        plt.axvspan(freq_mhz[0], bounds[0], color='r', alpha=0.2, label='Левый шум')
        plt.axvspan(bounds[1], freq_mhz[-1], color='m', alpha=0.2, label='Правый шум')
        plt.axvline(bounds[0], color='r', linestyle='--')
        plt.axvline(bounds[1], color='m', linestyle='--')
        plt.title(f"{Path(file_path).name} - Выбранные шумовые области")
        plt.xlabel('Частота (МГц)')
        plt.ylabel('Амплитуда (a.u.)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
        # Разделение данных
        peak_mask = (freq_mhz >= bounds[0]) & (freq_mhz <= bounds[1])
        peak_data = data[peak_mask]
        noise_data = data[~peak_mask]
        
        # Расчет дисперсии шума (в a.u.²)
        noise_var = np.mean(noise_data[:,1]**2) if len(noise_data) > 0 else 0
        
        # Расчет статистик
        stats = calculate_stats(peak_data[:,0], peak_data[:,1], noise_var)
        stats['temperature'] = extract_temperature(file_path)
        
        return stats
    except Exception as e:
        print(f"Ошибка обработки {file_path}: {e}")
        return None

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results_path = os.path.join(OUTPUT_DIR, "results.txt")
    
    with open(results_path, 'w', encoding='utf-8') as f:
        # Заголовок таблицы с единицами
        header = "T(K) |MaxValue(a.u.) |ErrMax(a.u.) |MaxFreq(MHz) |ErrFreq(MHz) |Mean(MHz) |ErrMean(MHz) |Variance(kHz²) |ErrVar(kHz²) |NoiseVar(a.u.²)"
        f.write(header + "\n")
        
        for path in FILE_PATHS:
            path = path.strip('"')
            print(f"\nОбработка: {path}")
            
            stats = process_file(path)
            if not stats:
                continue
            
            # Форматирование строки результатов
            line = (
                f"{stats['temperature']:.2f}|"
                f"{stats['max_value']:.5f}|"
                f"{stats['err_max_value']:.5f}|"
                f"{stats['max_freq']:.5f}|"
                f"{stats['err_max_freq']:.5f}|"
                f"{stats['mean']:.5f}|"
                f"{stats['err_mean']:.5f}|"
                f"{stats['variance']:.5f}|"
                f"{stats['err_var']:.5f}|"
                f"{stats['noise_var']:.5f}"
            )
            f.write(line + "\n")
    
    print(f"\nАнализ завершен. Результаты сохранены в:\n{os.path.abspath(OUTPUT_DIR)}")