import { initializeApp } from "firebase/app";
import { getFirestore, collection, query, orderBy, onSnapshot, limit } from "firebase/firestore";

// Hackathon: Replace with your actual config from Firebase Console
const firebaseConfig = {
    apiKey: "AIzaSy_MOCK_API_KEY",
    authDomain: "hackathon-distress-detection.firebaseapp.com",
    projectId: "hackathon-distress-detection",
    storageBucket: "hackathon-distress-detection.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export const subscribeToAlerts = (callback) => {
    const q = query(
        collection(db, "alerts"),
        orderBy("timestamp", "desc"),
        limit(20)
    );

    const unsubscribe = onSnapshot(q, (snapshot) => {
        const alerts = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data(),
            // handle timestamp depending on how it's stored (firebase timestamp vs string)
            timestamp: doc.data().timestamp?.toDate() || new Date()
        }));
        callback(alerts);
    });

    return unsubscribe;
};
