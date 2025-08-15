

# 📮 Cold Email Generator

A modern **AI-powered cold email generator** that scrapes job postings, extracts key details, and crafts tailored outreach emails with relevant portfolio links — all in seconds.

Built with **LangChain**, **Streamlit**, and **Python**, it’s perfect for developers, freelancers, and business professionals looking to connect with potential clients or employers effectively.

---

## 🚀 Features

✅ **One-click job scraping** – Enter any job posting URL, and the tool automatically extracts job details.
✅ **AI-powered email crafting** – Generates personalized cold emails based on job role, company, and required skills.
✅ **Portfolio integration** – Links your relevant portfolio projects directly in the email.
✅ **Copy & download options** – Copy to clipboard or download as `.txt` instantly.
✅ **Clean, professional UI** – Mobile-friendly, modern interface for smooth user experience.

---

## 📸 Screenshots

### Homepage & Job Input

<img width="1920" height="1020" alt="Screenshot 2025-08-15 120748" src="https://github.com/user-attachments/assets/c7de7d4a-caf8-4f22-a80d-b5f31c0e9de8" />  

---

### Extracted Job Details & Email Generation

<img width="1920" height="1020" alt="Screenshot 2025-08-15 120804" src="https://github.com/user-attachments/assets/cb952b6e-1143-4293-a3b7-756a022e5c54" />  

---

### Email Preview with Copy & Download Buttons

<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/1e2b12aa-8fb1-40e3-932d-ddce6f78ccbc" />  

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit** – Web app framework
* **LangChain** – AI orchestration & prompt engineering
* **WebBaseLoader** – Job post scraping
* **pysqlite3** – Ensures compatibility with ChromaDB
* **Custom Portfolio Integration** – Links to relevant projects

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Cold-Email-Generator.git
cd Cold-Email-Generator

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
streamlit run main.py
```

1. Paste a job post URL.
2. Click **"🚀 Generate Email"**.
3. View extracted job details & AI-crafted email.
4. Copy or download your email instantly.

---

## 📌 Notes

* Requires an **LLM API key** (e.g., OpenAI API) configured in `.env`.
* Works best with public job postings.
* Portfolio integration is customizable in `portfolio.py`.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue to discuss your ideas.

---

## 📜 License

This project is licensed under the **MAVERICK License**.
