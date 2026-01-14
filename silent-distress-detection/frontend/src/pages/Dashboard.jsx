import React, { useState, useEffect } from 'react';
import StatusBadge from '../components/StatusBadge';
import { getSystemStatus, startMonitoring, stopMonitoring } from '../services/api';

const Dashboard = () => {
    const [status, setStatus] = useState({
        is_running: false,
        camera_status: 'Idle',
        active_alerts_count: 0,
        last_alert: null
    });

    // State for Emergency Popup
    const [showPopup, setShowPopup] = useState(false);
    const [popupData, setPopupData] = useState(null);
    const [lastProcessedAlertTime, setLastProcessedAlertTime] = useState(0);

    const fetchStatus = async () => {
        const data = await getSystemStatus();
        if (data) {
            setStatus(data);

            // Checks for Critical Alert
            if (data.last_alert && data.last_alert.time > lastProcessedAlertTime) {
                // User Requirement: Start Popup ONLY if confidence is 100% (or Impact Triggered which sets it to 1.0)
                const isCritical = data.last_alert.score >= 0.99 ||
                    (data.last_alert.details && data.last_alert.details.trigger === "IMPACT_DETECTED");

                if (isCritical) {
                    setPopupData(data.last_alert);
                    setShowPopup(true);
                    setLastProcessedAlertTime(data.last_alert.time);
                }
            }
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 1000); // Faster polling for alerts
        return () => clearInterval(interval);
    }, [lastProcessedAlertTime]);

    const handleStart = async () => {
        await startMonitoring();
        fetchStatus();
    };

    const handleStop = async () => {
        await stopMonitoring();
        fetchStatus();
    };

    const closePopup = () => setShowPopup(false);

    return (
        <div className="page-container">
            {/* EMERGENCY POPUP MODAL */}
            {showPopup && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
                    backgroundColor: 'rgba(255,0,0,0.5)', zIndex: 9999,
                    display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                    <div style={{
                        background: '#fff', padding: '40px', borderRadius: '12px',
                        boxShadow: '0 0 50px rgba(255,0,0,0.8)',
                        textAlign: 'center', maxWidth: '500px', border: '5px solid red',
                        animation: 'pulse 1s infinite'
                    }}>
                        <h1 style={{ color: 'red', fontSize: '3rem', margin: 0 }}>⚠️ WARNING ⚠️</h1>
                        <h2 style={{ fontSize: '2rem' }}>PHYSICAL IMPACT DETECTED</h2>
                        <p style={{ fontSize: '1.2rem', margin: '20px 0' }}>
                            High confidence distress signal received.<br />
                            <strong>Confidence: {popupData ? (popupData.score * 100).toFixed(1) : 0}%</strong>
                        </p>
                        <button
                            className="btn btn-danger btn-lg"
                            style={{ fontSize: '1.5rem', padding: '15px 40px' }}
                            onClick={closePopup}
                        >
                            ACKNOWLEDGE
                        </button>
                    </div>
                    <style>
                        {`@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }`}
                    </style>
                </div>
            )}

            <h1>System Dashboard</h1>

            <div className="status-panel">
                <div className="status-item">
                    <h3>System State</h3>
                    <StatusBadge status={status.is_running ? "Active" : "Idle"} />
                </div>
                <div className="status-item">
                    <h3>Camera</h3>
                    <StatusBadge status={status.camera_status} />
                </div>
                <div className="status-item">
                    <h3>Active Alerts</h3>
                    <span className="count-badge">{status.active_alerts_count}</span>
                </div>
            </div>

            <div className="control-panel">
                <div className="video-feed-container" style={{ marginBottom: '20px', border: '2px solid #333', borderRadius: '8px', overflow: 'hidden' }}>
                    {status.is_running ? (
                        <img
                            src="http://localhost:8000/video_feed"
                            alt="Live Camera Feed"
                            style={{ width: '100%', maxWidth: '640px', display: 'block', margin: '0 auto' }}
                        />
                    ) : (
                        <div style={{ padding: '40px', textAlign: 'center', background: '#f0f0f0', color: '#666' }}>
                            <p>Camera is Offline. Automatic Privacy Mode Active.</p>
                        </div>
                    )}
                </div>

                {!status.is_running ? (
                    <button className="btn btn-primary btn-lg" onClick={handleStart}>
                        Start Monitoring
                    </button>
                ) : (
                    <button className="btn btn-danger btn-lg" onClick={handleStop}>
                        Stop Monitoring
                    </button>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
