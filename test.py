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
    """Чтение данных из файла"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            next(f)  # Пропуск заголовка
            for line in f:
                line = line.strip().replace(',', '.')
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        data.append((float(parts[0]), float(parts[1])))
    except Exception as e:
        print(f"Ошибка чтения {filename}: {e}")
    return np.array(data)

def interactive_noise_selection(frequencies, values):
    """Интерактивный выбор границ шумов с визуализацией"""
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, values, 'b-', label='Данные')
    plt.title("Выберите границы шумов:\nЛКМ - левая граница, ПКМ - правая\nEnter - подтвердить")
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    
    selected_points = []
    
    def on_click(event):
        if event.inaxes != plt.gca():
            return
        if event.button == 1:  # Левая кнопка
            selected_points.append(event.xdata)
            plt.axvline(event.xdata, color='r', linestyle='--')
        elif event.button == 3:  # Правая кнопка
            selected_points.append(event.xdata)
            plt.axvline(event.xdata, color='m', linestyle='--')
        plt.draw()
    
    def on_key(event):
        if event.key == 'enter':
            plt.close()
    
    plt.connect('button_press_event', on_click)
    plt.connect('key_press_event', on_key)
    plt.show()
    
    return sorted(selected_points[:2]) if len(selected_points) >= 2 else None

def calculate_stats(freq, values, noise_var):
    """Расчет статистик с погрешностями"""
    weights = np.abs(values)
    sum_weights = np.sum(weights)
    
    stats = {
        'max_value': np.max(values),
        'max_freq': freq[np.argmax(values)],
        'mean': np.average(freq, weights=weights),
        'variance': np.average((freq - np.average(freq, weights=weights))**2, weights=weights),
        'noise_var': noise_var,
        'err_mean': np.sqrt(noise_var * np.sum(weights**2)) / sum_weights if sum_weights > 0 else 0,
        'err_var': np.sqrt(2 * noise_var**2 / len(freq)) if len(freq) > 0 else 0
    }
    
    stats['std_dev'] = np.sqrt(stats['variance'])
    stats['err_std'] = stats['err_var'] / (2 * stats['std_dev']) if stats['std_dev'] > 0 else 0
    
    # Погрешность MaxFreq через ширину пика на уровне шума
    noise_std = np.sqrt(noise_var)
    threshold = stats['max_value'] - noise_std
    mask = values >= threshold
    if np.any(mask):
        f_left = freq[mask][0]
        f_right = freq[mask][-1]
        stats['err_max_freq'] = max(stats['max_freq'] - f_left, f_right - stats['max_freq'])
    else:
        stats['err_max_freq'] = 0.0
    
    return stats

def process_file(file_path):
    """Обработка файла с интерактивным выбором границ"""
    try:
        data = read_data(file_path)
        if data.size == 0:
            print(f"Пустой файл: {file_path}")
            return None
        
        freq = data[:,0]
        vals = data[:,1]
        
        # Интерактивный выбор границ
        bounds = interactive_noise_selection(freq, vals)
        if not bounds or len(bounds) < 2:
            print("Границы не выбраны! Использую автоматические границы.")
            threshold = np.max(vals) * 0.05  # 5% от максимума
            mask = vals >= threshold
            bounds = [freq[mask][0], freq[mask][-1]]
        
        # Разделение данных
        peak_mask = (freq >= bounds[0]) & (freq <= bounds[1])
        peak_data = data[peak_mask]
        noise_data = data[~peak_mask]
        
        # Расчет статистики
        noise_var = np.mean(noise_data[:,1]**2) if len(noise_data) > 0 else 0
        stats = calculate_stats(peak_data[:,0], peak_data[:,1], noise_var)
        stats['temperature'] = extract_temperature(file_path)
        
        # Визуализация результатов
        plt.figure(figsize=(12, 6))
        plt.plot(freq, vals, 'b-', label='Данные')
        plt.axvspan(freq[0], bounds[0], color='r', alpha=0.2, label='Левый шум')
        plt.axvspan(bounds[1], freq[-1], color='m', alpha=0.2, label='Правый шум')
        plt.axvline(bounds[0], color='r', linestyle='--')
        plt.axvline(bounds[1], color='m', linestyle='--')
        plt.plot(stats['max_freq'], stats['max_value'], 'ro', 
                label=f'Пик: {stats["max_value"]:.2f} ± {stats["err_max_freq"]:.2f} Гц')
        
        plt.title(f"{Path(file_path).name}\nТемпература: {stats['temperature']} K")
        plt.legend()
        plt.grid(True)
        plt.show()
        
        return stats
    except Exception as e:
        print(f"Ошибка обработки {file_path}: {e}")
        return None

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results_path = os.path.join(OUTPUT_DIR, "results.txt")
    
    with open(results_path, 'w', encoding='utf-8') as f:
        # Заголовок таблицы
        header = "T |MaxValue |ErrMax|MaxFreq |ErrFreq|Mean |ErrMean|Variance |ErrVar|NoiseVar"
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
                f"{stats['err_max_freq']:.5f}|"
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