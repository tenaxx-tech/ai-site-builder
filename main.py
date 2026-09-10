import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Загружаем переменные окружения (для локального запуска)
load_dotenv()

# 1. Настраиваем LLM. Ключ будет взят из переменной OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 2. Создаем промпт-шаблон
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — опытный веб-разработчик. Ты создаешь только код. Твой ответ должен содержать только HTML-файл с встроенными CSS и JS. Не пиши никаких объяснений."),
    ("human", "Создай одностраничный сайт для: {user_request}. Сделай его современным и адаптивным.")
])

# 3. Формируем цепочку
chain = prompt | llm

# 4. Простой пример генерации
user_input = "кофейни с меню и формой связи"
response = chain.invoke({"user_request": user_input})

# 5. Сохраняем результат
with open("index.html", "w", encoding="utf-8") as f:
    f.write(response.content)

print("Сайт сгенерирован в файл index.html")
