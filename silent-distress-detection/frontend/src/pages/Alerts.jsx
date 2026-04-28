import React, { useState, useEffect } from 'react';
import AlertCard from '../components/AlertCard';

const API_URL = "https://silent-distress-detection.onrender.com";
const Alerts = () => {
    const [alerts, setAlerts] = useState([]);

    const fetchAlerts = async () => {
        try {
            // Fetch from our backend wrapper which simulates/proxies Firestore
            const res = await fetch(`${API_URL}/alerts`);
            if (res.ok) {
                const data = await res.json();
                setAlerts(data);
            }
        } catch (err) {
            console.error("Failed to fetch alerts", err);
        }
    };

    useEffect(() => {
        fetchAlerts();
        const interval = setInterval(fetchAlerts, 3000); // Poll every 3 seconds
        return () => clearInterval(interval);
    }, []);

    const handleConfirm = (id) => {
        console.log("Confirmed alert:", id);
        // In a real app, send API call to update status
        // For now, optimistically update UI
        setAlerts(prev => prev.map(a => a.id === id ? { ...a, status: 'confirmed' } : a));
    };

    const handleDismiss = (id) => {
        console.log("Dismissed alert:", id);
        setAlerts(prev => prev.map(a => a.id === id ? { ...a, status: 'dismissed' } : a));
    };

    return (
        <div className="page-container">
            <h1>Live Alerts</h1>
            <div className="alerts-grid">
                {alerts.length === 0 ? (
                    <p className="no-data">No alerts detected yet.</p>
                ) : (
                    alerts.map(alert => (
                        <AlertCard
                            key={alert.id}
                            alert={alert}
                            onConfirm={handleConfirm}
                            onDismiss={handleDismiss}
                        />
                    ))
                )}
            </div>
        </div>
    );
};

export default Alerts;
