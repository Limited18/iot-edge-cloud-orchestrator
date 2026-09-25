# Firebase / Firestore

1. Create a Firebase project.
2. Enable Firestore Database.
3. Project Settings → Service Accounts → Firebase Admin SDK.
4. Generate a private key JSON.
5. Store it outside source control.
6. Set FIREBASE_CREDENTIALS in .env to the path.

The backend writes decision records to the configured decisions collection. Extend the same helper for raw sensor and resource collections as needed.

Never commit the service-account JSON.
