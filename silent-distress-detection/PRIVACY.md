# Privacy & Security Notes

- The system is explicitly designed to avoid identity or face recognition.
- Frames are processed in memory only; no images, no audio files, and no video are stored to disk or uploaded.
- Alerts store only camera/location IDs (non-identifying), timestamp, confidence scores and status.
- Role-based access: dashboard requires Firebase Authentication; Firestore rules restrict writes/updates to limited fields.
- For production, enable App Check and use server-side verification to ensure only authorized edge devices can write alerts.
