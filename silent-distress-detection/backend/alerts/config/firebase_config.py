import firebase_admin
from firebase_admin import credentials, firestore
from google.auth import exceptions as google_auth_exceptions

# In-memory storage for mock alerts
MOCK_DB = {
    "alerts": []
}

class MockDocumentRef:
    def __init__(self, doc_id):
        self._id = doc_id
    
    @property
    def id(self):
        return self._id

class MockCollection:
    def __init__(self, name):
        self.name = name

    def add(self, data):
        doc_id = f"mock_id_{len(MOCK_DB[self.name]) + 1}"
        data_with_id = data.copy()
        data_with_id['id'] = doc_id
        MOCK_DB[self.name].append(data_with_id)
        print(f"[MOCK FIRESTORE] Added to {self.name}: {data['confidence_score']}")
        return (None, MockDocumentRef(doc_id))
    
    def stream(self):
        # Return list of objects that look like firestore docs
        results = []
        for data in MOCK_DB.get(self.name, []):
            # Create a localized object to mimic doc.to_dict() and doc.id
            class MockDoc:
                def __init__(self, d):
                    self._d = d
                    self.id = d['id']
                def to_dict(self):
                    return self._d
            results.append(MockDoc(data))
        return results

class MockFirestore:
    def collection(self, name):
        if name not in MOCK_DB:
            MOCK_DB[name] = []
        return MockCollection(name)

def initialize_firebase():
    """Initializes Firebase Admin SDK with a fallback to Mock if creds are missing."""
    try:
        if not firebase_admin._apps:
            try:
                # Try default credentials (e.g. from gcloud or env var)
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
                print("Firebase initialized with Application Default Credentials.")
            except Exception:
                # Fallback: try init without specific creds (sometimes works in some envs)
                firebase_admin.initialize_app()
                print("Firebase initialized without explicit credentials.")

        # Try to get the client. This is where it usually fails if no creds are present.
        return firestore.client()

    except (ValueError, google_auth_exceptions.DefaultCredentialsError) as e:
        print(f"\n[WARNING] Firebase Authentication failed: {e}")
        print("[INFO] Switching to MOCK FIRESTORE. Alerts will be stored in memory.\n")
        return MockFirestore()
    except Exception as e:
        print(f"\n[WARNING] Unexpected Firebase error: {e}")
        print("[INFO] Switching to MOCK FIRESTORE.\n")
        return MockFirestore()

db = initialize_firebase()
