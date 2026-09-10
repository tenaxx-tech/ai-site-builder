import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Загружаем переменные окружения для локального запуска
load_dotenv()

app = Flask(__name__)

# Настраиваем LLM. Ключ будет взят из переменной окружения OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Создаем промпт-шаблон, который четко инструктирует модель
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — опытный веб-разработчик. Ты создаешь ТОЛЬКО код. Твой ответ должен содержать только полноценный HTML-файл с встроенными CSS и JS. Не пиши никаких объяснений, приветствий или markdown-разметки. Только чистый HTML."),
    ("human", "Создай одностраничный сайт для: {user_request}. Сделай его современным, адаптивным и эстетичным.")
])

# Собираем цепочку: промпт -> LLM
chain = prompt | llm

@app.route('/')
def index():
    """Отдает главную страницу с интерфейсом."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Принимает запрос пользователя и возвращает сгенерированный HTML."""
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')

        if not user_prompt:
            return jsonify({'error': 'Prompt is empty'}), 400

        # Вызываем LLM
        response = chain.invoke({"user_request": user_prompt})
        
        # Возвращаем сгенерированный HTML как часть JSON-ответа
        return jsonify({'html': response.content})

    except Exception as e:
        # Логируем ошибку и возвращаем сообщение об ошибке
        print(f"Error during generation: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Важно: слушаем 0.0.0.0, чтобы Bothost мог пробросить трафик
    # Порт также должен браться из переменной окружения, но Bothost подставит свой
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
