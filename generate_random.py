import random

def generate_random_numbers(start, end, count):
  """Генерирует список случайных чисел из заданного диапазона без повторений.

  Args:
    start: Начальная граница диапазона (включительно).
    end: Конечная граница диапазона (исключительно).
    count: Количество случайных чисел для генерации.

  Returns:
    Список случайных чисел из заданного диапазона без повторений.
  """
  if count > (end + 1 - start) and count != 0:
    raise ValueError("количество чисел больше, чем размер диапазона")

  unique_numbers = set()
  while len(unique_numbers) < count:
    unique_numbers.add(random.randint(start, end))

  return list(unique_numbers)