# parallel-computing-sfcurves

## Инструкция по установке и запуску 

Инициализация виртуального окружения Python, установка зависимостей:

```bash
python3 -m venv venv 
source ./venv/bin/activate 
pip install -r requirements.txt
```

Запуск: 
```bash
python3 main.py <path_to_config>
```

Пример конфига расположен в [./config.example.json](config.example.json)

После этого результат разбиения запишется в `output/mapping.csv` и визуализация в `output/hilbert_map.png`

## TODO 
- [x] Кривые Гилберта на плоскости для случая 2^n 
- [x] Простое разбиение на N_p процессоров 
- [x] Визуализация, экспорт в .csv 
- [x] Обработка случаев N != 2^n (кривые Пеано)
- [x] Трёхмерная кривая на сфере 
- [x] Разбиение на сфере
- [x] Обработка неквадратных тайлов
- [x] Обработка сетки со сгущением 
- [x] Нахождение метрики суммарного периметра для заданного алгоритма
- [ ] Обработка узлов с неодинаковым весом

### Пример результата разбиения для N = 32, N_p = 16
![hilbert_32x32_into_16.png](docs/imgs/hilbert_32x32_into_16.png)

(Цвет обозначает номер назначенного процессора.) 

### Пример разбиения развёртки куба
![hilbert_map.png](docs/imgs/hilbert_map.png)

### Пример разбиения с неквадратными панелями
![hilbert_map.png](docs/imgs/hilbert_map_non_square.png)

### Сравнение с геометрическим алгоритмом (чем меньше суммарный периметр, тем лучше)
![hilbert_vs_geometric.png](docs/imgs/hilbert_vs_geometric.png)
