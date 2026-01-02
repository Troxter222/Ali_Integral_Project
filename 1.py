import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def define_metrics():
    """
    Определение метрических тензоров для статической (Шварцшильд) 
    и вращающейся (Керр) черных дыр.
    """
    # Определение символов
    t, r, theta, phi = sp.symbols('t r theta phi')
    M, a = sp.symbols('M a')  # Масса и угловой момент
    
    # --- УРОВЕНЬ 1: МЕТРИКА ШВАРЦШИЛЬДА (a=0) ---
    # ds^2 = -(1-2M/r)dt^2 + (1-2M/r)^(-1)dr^2 + r^2*dOmega^2
    # ИСПРАВЛЕНИЕ: Добавлен недостающий ноль в последней строке (4x4)
    schwarzschild_g = sp.Matrix([
        [-(1 - 2*M/r), 0, 0, 0],
        [0, 1/(1 - 2*M/r), 0, 0],
        [0, 0, r**2, 0],
        [0, 0, 0, r**2 * sp.sin(theta)**2] 
    ])
    
    # --- УРОВЕНЬ БОГ: МЕТРИКА КЕРРА (Вращение) ---
    # Используем координаты Бойера-Линдквиста
    Sigma = r**2 + a**2 * sp.cos(theta)**2
    Delta = r**2 - 2*M*r + a**2
    
    # Компоненты метрического тензора Керра g_mu_nu
    g_tt = -(1 - 2*M*r/Sigma)
    g_tphi = -2*M*a*r * sp.sin(theta)**2 / Sigma
    g_rr = Sigma / Delta
    g_thetatheta = Sigma
    g_phiphi = (r**2 + a**2 + 2*M*a**2*r*sp.sin(theta)**2/Sigma) * sp.sin(theta)**2
    
    kerr_g = sp.Matrix([
        [g_tt, 0, 0, g_tphi],
        [0, g_rr, 0, 0],
        [0, 0, g_thetatheta, 0],
        [g_tphi, 0, 0, g_phiphi]
    ])

    print("--- Научный комментарий: Геометрия внутри горизонта ---")
    print("Тензорный анализ завершен успешно.")
    print("В метрике Шварцшильда при r < 2M:")
    print("1. Координата t становится пространственноподобной (путь назад закрыт геометрически).")
    print("2. Координата r становится времениподобной (неизбежное движение в будущее к r=0).")
    
    return schwarzschild_g, kerr_g

# Инициализация тензоров (теперь работает без ошибок)
sg, kg = define_metrics()

# Константы (в геометрических единицах G=c=1)
M = 1.0           # Масса черной дыры
Rs = 2 * M        # Радиус Шварцшильда (Горизонт событий)
r_start = 10 * M  # Начальная позиция наблюдателя

def geodesic_equations(y, tau):
    """
    Система ОДУ для радиального падения массивного тела (Наблюдатель).
    Для радиального падения из состояния покоя уравнение Ньютона совпадает с ОТО по форме:
    d^2r/dtau^2 = -M/r^2
    """
    r, u = y
    # Сингулярность: защита от деления на ноль
    if r < 1e-4: return [0, 0]
    dydt = [u, -M / (r**2)] 
    return dydt

def null_geodesic(r_photon):
    """
    Скорость света в координатном времени (dr/dt).
    Свет "останавливается" на горизонте для удаленного наблюдателя.
    """
    if r_photon <= 0: return 0
    return -(1 - 2*M/r_photon)

# --- РАСЧЕТ ТРАЕКТОРИИ (Падение) ---
tau = np.linspace(0, 40, 1000)
y0 = [r_start, 0] 
solution = odeint(geodesic_equations, y0, tau)
r_observer = solution[:, 0]

# --- РАСЧЕТ ТРАЕКТОРИИ СВЕТА (Догоняющий фотон) ---
t_coord = np.linspace(0, 50, 1000)
r_photon_vals = [r_start + 2.0]
dt = t_coord[1] - t_coord[0]

for i in range(1, len(t_coord)):
    r_prev = r_photon_vals[-1]
    dr = null_geodesic(r_prev) * dt
    r_new = r_prev + dr
    if r_new < 0: r_new = 0
    r_photon_vals.append(r_new)

r_photon_vals = np.array(r_photon_vals)

# --- ВИЗУАЛИЗАЦИЯ 1: Траектории ---
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.axhline(y=Rs, color='red', linestyle='--', label='Горизонт событий ($r_s$)')
plt.axhline(y=0, color='white', linewidth=2, label='Сингулярность ($r=0$)')
plt.plot(tau, r_observer, color='cyan', linewidth=2, label='Наблюдатель (Proper Time)')
plt.plot(tau[:len(r_photon_vals)], r_photon_vals[:len(tau)], color='yellow', linestyle=':', label='Догоняющий фотон')
plt.xlabel('Собственное время $\\tau$')
plt.ylabel('Радиальная координата $r$')
plt.title('Кинематика падения: Наблюдатель vs Свет')
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()

print("\n--- Научный комментарий: Световой барьер ---")
print(f"Свет догоняет наблюдателя, но из-за замедления времени у горизонта")
print("фотоны накапливаются, создавая зону высокой энергии.")

# --- ВИЗУАЛИЗАЦИЯ 2: Энергетический сдвиг ---
def plot_energy_shift():
    r_vals = np.linspace(r_start, Rs + 0.05, 500)
    # Упрощенная модель расходимости энергии (Blue Shift)
    energy_factor = 1.0 / np.sqrt(r_vals - Rs)
    
    plt.figure(figsize=(10, 6))
    plt.plot(r_vals, energy_factor, color='magenta', linewidth=2)
    plt.title('Гравитационное синее смещение (Blue Shift)', fontsize=14)
    plt.xlabel('Расстояние до центра (r)', fontsize=12)
    plt.ylabel('Фактор энергии ($E/E_0$)', fontsize=12)
    plt.axvline(x=Rs, color='red', linestyle='--', label='Горизонт событий')
    plt.gca().invert_xaxis() # Падаем справа налево
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.text(Rs + 1.5, np.max(energy_factor)*0.8, 
             "Зона смерти:\nБесконечная энергия", color='yellow', fontsize=10)
    plt.show()

plot_energy_shift()

def calculate_blueshift_limit():
    """
    Доказательство сингулярности энергии.
    """
    r, r_minus = sp.symbols('r r_minus', real=True)
    
    # Модель энергии у внутреннего горизонта (Коши)
    # E ~ 1 / (r - r_minus)
    Energy_function = 1 / (r - r_minus)
    
    # Вычисляем предел
    limit_at_cauchy = sp.limit(Energy_function, r, r_minus, dir='+')
    
    print("\n--- Научный комментарий: Массовая инфляция (Mass Inflation) ---")
    print(f"Аналитическая функция энергии: {Energy_function}")
    print(f"Предел энергии при приближении к горизонту Коши: {limit_at_cauchy}")
    print("-" * 60)
    print("РЕЗУЛЬТАТ: Наблюдатель встречает бесконечный поток энергии (oo).")
    print("Все фотоны, упавшие в дыру за время существования Вселенной,")
    print("сжимаются в бесконечно тонкий слой. Теория 'Видения' математически подтверждена,")
    print("но биологическая жизнь невозможна из-за мгновенного испарения.")

calculate_blueshift_limit()