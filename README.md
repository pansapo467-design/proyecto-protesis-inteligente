# Prótesis Mamaria Inteligente de Monitoreo Continuo

# Descripción del Proyecto
brasie es un sistema integral de salud diseñado para mujeres que han pasado por una mastectomía
Consiste en una prótesis mamaria equipada con sensores avanzados que monitorean en tiempo real signos vitales críticos como 
( temperatura, ritmo cardíaco y presión arterial )
El sistema se conecta a una plataforma web ( desarrollada en Lovable ) y un backend en Python ( Flask ) para procesar datos y ofrecer alertas preventivas mediante inteligencia artificial que en seria el plus de la app

# Justificación del Proyecto
Tras una cirugía de mastectomía el seguimiento médico es vital para detectar complicaciones como infecciones o desequilibrios hemodinámicos
brasie soluciona la falta de monitoreo constante fuera del entorno hospitalario Ofreciendo
Prevención- Detección temprana de fiebre o anomalías cardíacas
Comodidad- Integración del monitoreo en un dispositivo de uso diario ( OSEA LA PROTESIS )
Tranquilidad- Un sistema de alerta de emergencia con geolocalización para respuesta inmediata

#  Desarrollo del Proyecto ( Arquitectura Técnica )
El desarrollo se ha dividido en cuatro partes o pilares principale

# Base de Datos ( PostgreSQL )
Se diseñó una estructura relacional para gestionar
Perfiles de usuario y expedientes médicos
Historial- de lecturas de sensores ( temperatura, ritmo, presión )
Estado- técnico de la prótesis ( batería y mantenimiento de motores )
Auditoría- de interacciones con el asistente de IA 

# Backend ( Python & Flask )
Se construyó una API REST que actúa como puente de comunicación
Conexión segura con PostgreSQL mediante ( psycopg2 )
Implementación de CORS para permitir la comunicación con el frontend
Exposición del servidor local a la red mediante un túnel seguro con ngrok

# Frontend ( Lovable & React )
Interfaz de usuario moderna y responsiva que incluye
Dashboard- de signos vitales con actualización automática cada 5 segundos
Chatbot- integrado para consultas médicas básicas
Sistema- de gestión de citas y botón de pánico con envío de coordenadas

# Integración de IA
El sistema utiliza modelos de lenguaje para analizar las tendencias de los signos vitales y proporcionar diagnósticos preliminares al usuario, mejorando la interacción humano-máquina