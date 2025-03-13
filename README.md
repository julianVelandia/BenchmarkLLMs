Benchmark LLMs Evaluation Pipeline

![image](https://github.com/user-attachments/assets/2291ecd5-f723-40f6-8aa8-16580d997ae3)

![image](https://github.com/user-attachments/assets/4ca683f6-4245-42bc-a383-50dcc40de717)

Este repositorio implementa un flujo automatizado para evaluar múltiples modelos de lenguaje (LLMs) y clasificarlos según la calidad de sus respuestas.

## Flujo de Evaluación

1. **Generación de respuestas**: Cada modelo de la familia LLM genera respuestas a un conjunto de preguntas de prueba contenidas en `finetuning_dataset_test.json`.
2. **Ranking de respuestas**: Un modelo evaluador clasifica las respuestas generadas para determinar su calidad.
3. **Almacenamiento de resultados**: 
   - `model_answers_ranking.json`: Contiene las preguntas y el ranking de modelos según su desempeño. Ejemplo:
     ```json
     [
         {
             "question": "¿Qué tipo de confusión se intenta evitar al utilizar 'HRV' para referirse a la HRV de 24 horas y no a la HRV a corto plazo?",
             "ranking": [
                 "JulianVelandia/Llama-3.2-1B-unal-instruct-ft-gguf/model-f16.gguf",
                 "JulianVelandia/Llama-3.2-1B-unal-instruct-q-ft-gguf/model-f16.gguf+RAG",
                 "JulianVelandia/Llama-3.2-1B-unal-instruct-ft-gguf/model-f16.gguf+RAG"
             ]
         }
     ]
     ```
   - `models_answers.json`: Contiene las respuestas generadas por cada modelo. Ejemplo:
     ```json
     {
         "lmstudio-community/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q8_0.gguf": [
             {
                 "question": "¿Qué tipo de confusión se intenta evitar al utilizar 'HRV' para referirse a la HRV de 24 horas y no a la HRV a corto plazo?",
                 "answer": "La confusión se intenta evitar al considerar que la HRV de 24 horas puede ser utilizada como sinónimo de la HRV a corto plazo, lo que podría llevar a errores en la interpretación de los resultados.",
                 "llm_answer": ""
             }
         ]
     }
     ```

## Resultados

Los resultados almacenados en `model_answers_ranking.json` y `models_answers.json` permiten analizar el desempeño de cada modelo en la tarea evaluada y comparar su calidad en la generación de respuestas.

