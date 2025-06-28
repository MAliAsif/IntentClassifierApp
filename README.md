# Intent Classifier Application  

## 📁 Project Structure
INTENT_CLASSIFIER/
├── api/
├── Auth/
├── ml/ 
├── response_models/
├── requirements.txt
├── Dockerfile
└── README.md


## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maliasif/IntentClassifierApp.git
   cd IntentClassifierApp


2. Create and activate a virtual environment:

python -m venv myenv
myenv\Scripts\activate

3. Install required dependencies:

pip install -r requirements.txt

4. Use the following command to start the server locally, a local URL will be displayed in your terminal, from here Endpoints can be tested :

uvicorn api.main:app --reload     

5. Open your browser at: 
localURL/docs e-g http://127.0.0.1:8000/docs to test the Post Endpoints

6. User is required to Sign up. After enterings its detail, a unique token key will be generated. From this key user can Authorize and test the Post Endpoints. Click on the Lock Sign at left, to provide the secret token key and sign in.

## 🧪 Running Unit Tests

To run the unit tests, open the terminal in VS Code, activate your virtual environment, and run:

```bash
$env:PYTHONPATH = "."; pytest api/tests/test_main.py

For macOS/Linux, use:
PYTHONPATH=. pytest api/tests/test_main.py



