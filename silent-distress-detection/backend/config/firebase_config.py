import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import time

# Check for service account key
# You should place your 'serviceAccountKey.json' in the root or backend folder
cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")

class MockDocumentSnapshot:
    def __init__(self, data, doc_id):
        self._data = data
        self.id = doc_id
    
    def to_dict(self):
        return self._data

class MockCollectionReference:
    def __init__(self, name):
        self.name = name
        self._docs = [] # In-memory store for the session
    
    def add(self, data):
        # Mock add
        doc_id = f"mock_id_{int(time.time()*1000)}"
        print(f"[MOCK FIRESTORE] Added to {self.name}: {data}")
        self._docs.append(MockDocumentSnapshot(data, doc_id))
        return (None, type('obj', (object,), {'id': doc_id}))

    def stream(self):
        # Return what we have stored in memory
        return self._docs

class MockFirestore:
    def __init__(self):
        self._collections = {}

    def collection(self, name):
        if name not in self._collections:
            self._collections[name] = MockCollectionReference(name)
        return self._collections[name]

try:
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("[FIREBASE] Initialized successfully.")
    else:
        raise FileNotFoundError(f"Credential file {cred_path} not found.")
except Exception as e:
    print(f"[FIREBASE] Warning: Could not initialize Firebase ({e}). Using Mock Firestore.")
    db = MockFirestore()
