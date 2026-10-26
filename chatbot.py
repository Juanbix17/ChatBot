"""Chatbot CeniChat con API FastAPI e interfaz web adaptable para CENIGRAF."""

import random
import re
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from iagenerativa import generar_respuestas

app = FastAPI(title="CeniChat - CENIGRAF", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


""" def responder(mensaje: str) -> str:
    ""Genera una respuesta por reglas basada en la oferta educativa de CENIGRAF.""
    texto = mensaje.strip().lower()

    if any(saludo in texto for saludo in ("hola", "buenas", "oe", "saludos")):
        return "¡Hola! Bienvenido a CeniChat. ¿En qué te puedo ayudar sobre la oferta educativa de CENIGRAF?"
    
    if "nombre" in texto:
        return "Soy CeniChat, el asistente virtual de la oferta educativa del Centro de la Industria de la Comunicación Gráfica (CENIGRAF)."
    
    if any(palabra in texto for palabra in ("adiós", "chao", "hasta luego", "nos vemos")):
        return "¡Hasta luego! Recuerda que estamos para ayudarte en tu proceso de formación."
    
    if "ayuda" in texto:
        return "Puedo informarte sobre nuestros programas técnicos y tecnológicos, requisitos de inscripción, horarios, duración y ubicación de CENIGRAF."

    # Preguntas sobre la oferta educativa de CENIGRAF
    if any(p in texto for p in ("inscripcion", "inscripciones", "inscrito", "abierta", "abiertas", "fecha")):
        return "Actualmente las inscripciones están sujetas al calendario académico del SENA. Puedes verificar fechas en el portal Sofia Plus o consultar con la administración del centro."

    if any(p in texto for p in ("software", "adso", "programacion")):
        return "El programa tecnológico en 'Análisis y Desarrollo de Software' (ADSO) tiene una duración de 27 meses. En nivel técnico, contamos con 'Programación de Software' con duración de 15 meses."

    if any(p in texto for p in ("virtual", "virtuales", "tecnologia", "tecnologias")):
        return "Las Tecnologías Virtuales incluyen: Análisis y Desarrollo de Software (ADSO), Animación 3D, Animación Digital, Desarrollo de Medios Gráficos Visuales, Desarrollo Publicitario, Desarrollo Multimedia y Web, Desarrollo de Videojuegos y Coordinación de Procesos Logísticos (duración: 27 meses)."

    if any(p in texto for p in ("animacion", "multimedia", "grafico", "videojuego", "videojuegos", "diseno")):
        return "En el área gráfica y digital contamos con programas como Animación 3D, Animación Digital, Desarrollo de Videojuegos, Producción Multimedia y Desarrollo de Medios Gráficos Visuales."

    if any(p in texto for p in ("presencial", "presenciales", "tecnico", "tecnicos")):
        return "Entre los Técnicos Presenciales (duración: 15 meses) en CENIGRAF tenemos: Preprensa Digital, Impresión (Offset, Flexográfica, Serigráfica, Digital), Programación de Software, Sistemas Teleinformáticos, Elaboración de Audiovisuales y Encuadernación."

    if any(p in texto for p in ("requisito", "requisitos", "matrícula", "matricula", "documentos")):
        return "Los requisitos básicos incluyen: documento de identidad actualizado, certificado de noveno o bachiller (según el nivel del programa) y registro en la plataforma Sofia Plus."

    if any(p in texto for p in ("donde", "ubicacion", "direccion", "centro")):
        return "CENIGRAF es el Centro de la Industria de la Comunicación Gráfica del SENA, enfocado en formar profesionales en artes gráficas, diseño, medios digitales y desarrollo de software."

    if any(p in texto for p in ("horario", "horarios", "jornada", "jornadas")):
        return "Contamos con jornadas diurna, nocturna y mixta según la disponibilidad de cupos y el programa seleccionado."
      
    if any(p in texto for p in ("programas", "ofertas", "ofrece")):
            return "Contamos con una amplia gama de programas y ofertas educativas en CENIGRAF relacionadas al ambito de la comunicación gráfica y digital."

    return f"No comprendo totalmente tu consulta sobre: «{mensaje.strip()}». Puedes seleccionar una de las preguntas frecuentes o detallar más tu inquietud." """


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    
  respuesta = await generar_respuestas(request.message)

  return ChatResponse(reply=respuesta)


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CeniChat - Oferta educativa CENIGRAF</title>
  <style>
    :root {
      --sena-green: #39a900;
      --sena-dark: #00324d;
      --bg-color: #f4f6f9;
      --card-bg: #ffffff;
      --border-color: #e2e8f0;
      --text-color: #2d3748;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background-color: var(--bg-color);
      color: var(--text-color);
      line-height: 1.5;
      padding: 1rem;
    }

    .container {
      max-width: 780px;
      margin: 0 auto;
    }

    /* Header */
    .header-card {
      background: var(--card-bg);
      border-left: 6px solid var(--sena-green);
      border-radius: 10px;
      padding: 1rem 1.25rem;
      margin-bottom: 1rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    .brand-info {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .avatar-bg {
      width: 44px;
      height: 44px;
      background-color: var(--sena-green);
      color: white;
      font-weight: bold;
      font-size: 1.2rem;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
    }

    .title-area h1 {
      font-size: 1.25rem;
      color: var(--sena-dark);
    }

    .title-area p {
      font-size: 0.85rem;
      color: #64748b;
    }

    .btn-clear {
      background: transparent;
      border: 1px solid #ef4444;
      color: #ef4444;
      padding: 0.4rem 0.8rem;
      border-radius: 20px;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-clear:hover {
      background: #ef4444;
      color: white;
    }

    /* Main Container */
    .chat-card {
      background: var(--card-bg);
      border-radius: 10px;
      padding: 1.25rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      border: 1px solid var(--border-color);
    }

    #chat {
      height: 380px;
      overflow-y: auto;
      background-color: #fafafa;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1rem;
      margin-bottom: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    .message {
      max-width: 82%;
      display: flex;
      flex-direction: column;
      word-wrap: break-word;
    }

    .bot-message {
      align-self: flex-start;
    }

    .bot-message .message-content {
      background-color: #ffffff;
      border: 1px solid var(--border-color);
      color: var(--text-color);
      border-radius: 12px 12px 12px 2px;
      padding: 0.75rem 1rem;
    }

    .user-message {
      align-self: flex-end;
    }

    .user-message .message-content {
      background-color: var(--sena-green);
      color: #ffffff;
      border-radius: 12px 12px 2px 12px;
      padding: 0.75rem 1rem;
    }

    .message-time {
      font-size: 0.7rem;
      color: #94a3b8;
      margin-top: 0.25rem;
    }

    .bot-message .message-time { align-self: flex-start; }
    .user-message .message-time { align-self: flex-end; }

    /* Indicador de carga */
    .typing-indicator {
      display: none;
      font-size: 0.85rem;
      color: #64748b;
      margin-bottom: 0.75rem;
      align-items: center;
      gap: 0.5rem;
    }

    .typing-indicator.active {
      display: flex;
    }

    .dots {
      display: inline-flex;
      gap: 3px;
    }

    .dots span {
      width: 6px;
      height: 6px;
      background-color: var(--sena-green);
      border-radius: 50%;
      animation: pulse 1.4s infinite ease-in-out both;
    }

    .dots span:nth-child(1) { animation-delay: -0.32s; }
    .dots span:nth-child(2) { animation-delay: -0.16s; }

    @keyframes pulse {
      0%, 80%, 100% { transform: scale(0); }
      40% { transform: scale(1); }
    }

    /* FAQ Section */
    .faq-section {
      margin-bottom: 1rem;
    }

    .faq-title {
      font-size: 0.8rem;
      font-weight: 600;
      color: #64748b;
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .faq-container {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .faq-btn {
      background: transparent;
      border: 1px solid var(--sena-green);
      color: var(--sena-green);
      padding: 0.4rem 0.8rem;
      border-radius: 20px;
      font-size: 0.82rem;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
    }

    .faq-btn:hover {
      background: var(--sena-green);
      color: white;
    }

    /* Input Form */
    form {
      display: flex;
      gap: 0.5rem;
    }

    input {
      flex: 1;
      padding: 0.75rem 1rem;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-size: 0.95rem;
      outline: none;
    }

    input:focus {
      border-color: var(--sena-green);
    }

    button[type="submit"] {
      padding: 0.75rem 1.25rem;
      border: 0;
      border-radius: 8px;
      background: var(--sena-green);
      color: white;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s ease;
    }

    button[type="submit"]:hover {
      background: #2f8c00;
    }

    footer {
      text-align: center;
      color: #94a3b8;
      font-size: 0.8rem;
      margin-top: 1rem;
    }

    /* Responsive Design */
    @media (max-width: 576px) {
      body {
        padding: 0.5rem;
      }

      .header-card {
        flex-direction: column;
        align-items: flex-start;
      }

      .btn-clear {
        align-self: flex-end;
      }

      #chat {
        height: 300px;
      }

      .message {
        max-width: 90%;
      }

      .faq-container {
        flex-direction: column;
      }

      .faq-btn {
        width: 100%;
      }

      form {
        flex-direction: column;
      }

      button[type="submit"] {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Encabezado -->
    <header class="header-card">
      <div class="brand-info">
        <div class="avatar-bg">C</div>
        <div class="title-area">
          <h1>CeniChat</h1>
          <p>Oferta educativa CENIGRAF</p>
        </div>
      </div>
      <button id="btnClear" class="btn-clear" type="button">🗑️ Limpiar chat</button>
    </header>

    <!-- Área Principal de Chat -->
    <main class="chat-card">
      <div id="chat" aria-live="polite">
        <div class="message bot-message">
          <div class="message-content">
            ¡Hola! Soy <strong>CeniChat</strong>, tu asistente virtual para la oferta educativa de CENIGRAF. Selecciona una pregunta frecuente o escribe tu inquietud.
          </div>
          <span class="message-time">10:00</span>
        </div>
      </div>

      <!-- Indicador de Respuesta (Actividad 2) -->
      <div id="typingIndicator" class="typing-indicator">
        <div class="dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <em>CeniChat está escribiendo...</em>
      </div>

      <!-- Preguntas Frecuentes (Actividad 1) -->
      <div class="faq-section">
        <p class="faq-title">Preguntas frecuentes</p>
        <div class="faq-container">
          <button type="button" class="faq-btn">¿Qué programas ofrece CENIGRAF?</button>
          <button type="button" class="faq-btn">¿Cuáles son los requisitos de inscripción?</button>
          <button type="button" class="faq-btn">¿Qué tecnologías virtuales existen?</button>
          <button type="button" class="faq-btn">¿Cuáles son los horarios y jornadas?</button>
        </div>
      </div>

      <!-- Campo de Escritura -->
      <form id="form">
        <input id="message" autocomplete="off" placeholder="Escribe tu mensaje aquí..." required maxlength="2000">
        <button type="submit">Enviar</button>
      </form>
    </main>

    <footer>
      SENA - Centro de la Industria de la Comunicación Gráfica (CENIGRAF)
    </footer>
  </div>

  <script>
    const chat = document.querySelector('#chat');
    const form = document.querySelector('#form');
    const input = document.querySelector('#message');
    const typingIndicator = document.querySelector('#typingIndicator');
    const btnClear = document.querySelector('#btnClear');
    const faqButtons = document.querySelectorAll('.faq-btn');

    function getCurrentTime() {
      const now = new Date();
      return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function addMessage(who, text) {
      const isUser = who === 'Tú';
      const messageDiv = document.createElement('div');
      messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

      const contentDiv = document.createElement('div');
      contentDiv.className = 'message-content';
      contentDiv.textContent = text;

      const timeSpan = document.createElement('span');
      timeSpan.className = 'message-time';
      timeSpan.textContent = getCurrentTime();

      messageDiv.appendChild(contentDiv);
      messageDiv.appendChild(timeSpan);

      chat.appendChild(messageDiv);
      chat.scrollTop = chat.scrollHeight;
    }

    function showTyping() {
      typingIndicator.classList.add('active');
      chat.scrollTop = chat.scrollHeight;
    }

    function hideTyping() {
      typingIndicator.classList.remove('active');
    }

    async function sendMessage(message) {
      if (!message) return;

      addMessage('Tú', message);
      showTyping();

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });

        hideTyping();

        if (!response.ok) throw new Error('No se pudo obtener una respuesta.');
        const data = await response.json();
        addMessage('CeniChat', data.reply);
      } catch (error) {
        hideTyping();
        addMessage('CeniChat', `Error: ${error.message}`);
      }
    }

    // Evento Formulario
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;
      input.value = '';
      sendMessage(message);
    });

    // Actividad 1: Eventos para Preguntas Frecuentes
    faqButtons.forEach(button => {
      button.addEventListener('click', () => {
        const question = button.textContent.trim();
        sendMessage(question);
      });
    });

    // Actividad 3: Botón para Limpiar Chat con Confirmación
    btnClear.addEventListener('click', () => {
      if (confirm("¿Está seguro de que desea limpiar el historial de la conversación?")) {
        chat.innerHTML = `
          <div class="message bot-message">
            <div class="message-content">
              ¡Hola! Soy <strong>SENAI</strong>, tu asistente virtual de CENIGRAF. ¿En qué puedo ayudarte?
            </div>
            <span class="message-time">${getCurrentTime()}</span>
          </div>
        `;
      }
    });
  </script>
</body>
</html>"""