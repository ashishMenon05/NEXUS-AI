# NEXUS: Autonomous Incident Investigation Dashboard

NEXUS is a next-generation, autonomous dual-agent environment designed to investigate and validate software incidents in real-time. Using a combination of an **Investigator** and a **Validator** agent, NEXUS autonomously forms hypotheses, executes systems tools, and reaches consensus on root causes.

![NEXUS Dashboard Mockup](https://raw.githubusercontent.com/ashishMenon05/NEXON-AI/main/frontend/public/hero.png)

## 🚀 Features
- **Dual-Agent Autonomy**: Agents collaborate word-by-word via real-time LLM streaming.
- **Provider Agnostic**: Seamlessly switch between **Local Ollama** and **Hugging Face Inference API**.
- **Dynamic Scenario Injection**: Type natural language scenarios directly into the dashboard; NEXUS handles the rest.
- **Limitless Communication**: Agents talk until the job is done, with a global "Kill Switch" for manual control.
- **Modern Tactical UI**: Glass-morphic, high-performance dashboard built with React and Tailwind CSS.

---

## 🛠️ Prerequisites
- **Ollama**: [Download here](https://ollama.com) (For local models like Dolphin-Phi or Qwen)
- **Python 3.10+**: Backend engine.
- **Node.js 18+**: Frontend dashboard.
- **Hugging Face Token** (Optional): If you wish to use cloud-based models.

---

## ⚡ Quick Start

### 1. Clone & Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the `backend/` directory:
```env
OLLAMA_BASE_URL=http://localhost:11434/v1
AGENT_A_MODEL=dolphin-phi
AGENT_B_MODEL=qwen2.5:3b
HF_TOKEN=your_token_here_if_using_hf
```

### 3. Start the Engines
**Terminal 1 (Backend):**
```bash
cd backend
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install
npm run dev
```

---

## 🕹️ How to Use
1. Open [http://localhost:5173](http://localhost:5173).
2. Go to **Settings** to select your models (Ollama is default).
3. On the **Dashboard**, use the **Scenario Configurator** at the bottom.
4. Paste your incident description (e.g., "The payment gateway is timing out for users in EU-West").
5. Click **Inject & Reset**, then hit **START**.
6. Watch the terminal logs as the agents investigate and resolve the issue!

---

## 🧩 Architecture
- **API**: FastAPI (Python)
- **Real-time**: WebSockets for live agent communication and state sync.
- **Frontend**: React + Tailwind CSS + Framer Motion.
- **Models**: OpenAI-compatible API (Ollama/HuggingFace/vLLM).

---

## 🤝 Contributing
Feel free to fork and submit PRs for new tools or better agent prompts!

**Developed by: Ashish Menon**
