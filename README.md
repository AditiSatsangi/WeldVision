# WeldVision: Deploying Deep learning model for Welding Defect Detection

Real-time deep learning system for welding defect detection and classification. This project deploys a trained YOLO-based model as a web application using Flask + Docker + Azure App Service.

---

## 🚀 Features

- Real-time welding defect detection using a YOLO model
- Web-based interface for uploading or streaming weld images
- Fast inference pipeline optimized for deployment
- Dockerized application for reproducible deployment
- Azure App Service CI/CD workflow included

---

## 📂 Repository Structure

```
WeldVision/
│
├── app.py               # Flask backend
├── static/              # CSS, JS, images
├── templates/           # HTML front-end
│
├── Data/                # Dataset link + info
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build
├── Procfile             # Gunicorn entrypoint
├── .github/workflows/   # Deployment workflow
└── README.md
```

---

## 📦 Setup & Run (Local)

**1. Clone the repository**

```bash
git clone https://github.com/AditiSatsangi/WeldVision.git
cd WeldVision
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the Flask app**

```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## 🐳 Run with Docker

**Build the Docker image**

```bash
docker build -t weldvision .
```

**Run the container**

```bash
docker run -p 5000:5000 weldvision
```

Access the application at `http://localhost:5000`

---

## ☁️ Deployment

This project includes a GitHub Actions workflow for automated deployment to Azure App Service.

**Prerequisites**

- Azure account with an active subscription
- Azure App Service instance created
- Deployment credentials configured in GitHub Secrets

**Deployment Steps**

1. Fork or clone this repository
2. Configure GitHub Secrets with your Azure credentials
3. Push to the main branch to trigger automatic deployment
4. The workflow file is located at `.github/workflows/`

---

## 📄 Dataset

Dataset information and download link are provided in:

```
Data/Link
```

---

## 🛠️ Technologies Used

- **Backend:** Flask, Python
- **ML Framework:** YOLO (You Only Look Once)
- **Containerization:** Docker
- **Deployment:** Azure App Service
- **CI/CD:** GitHub Actions
- **Server:** Gunicorn

---

## 📋 Requirements

All Python dependencies are listed in `requirements.txt`. Key libraries include:

- Flask
- PyTorch / TensorFlow (depending on YOLO implementation)
- OpenCV
- NumPy
- Pillow

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## ✍️ Author

**Aditi Satsangi**  
MSc Computer Science, Western University  
GitHub: [@AditiSatsangi](https://github.com/AditiSatsangi)

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub or reach out via email.

---

⭐ **If you find this project useful, please consider giving it a star on GitHub!**
