import React from 'react';
import StatusBadge from './StatusBadge';

const AlertCard = ({ alert, onConfirm, onDismiss }) => {
    const { id, timestamp, location, confidence_score, status, details } = alert;

    const dateStr = new Date(timestamp * 1000).toLocaleString();

    return (
        <div className={`alert-card ${status === 'pending' ? 'alert-pending' : ''}`}>
            <div className="alert-header">
                <h3>DISTRESS DETECTED</h3>
                <StatusBadge status={status} />
            </div>
            <div className="alert-body">
                <p><strong>Time:</strong> {dateStr}</p>
                <p><strong>Location:</strong> {location}</p>
                <p><strong>Confidence:</strong> {(confidence_score * 100).toFixed(1)}%</p>
                <div className="alert-details">
                    {details.trigger === "IMPACT_DETECTED" && (
                        <div className="alert-trigger-badge">⚠️ PHYSICAL IMPACT DETECTED ⚠️</div>
                    )}
                    <small>AI Feedback: {JSON.stringify(details, null, 2)}</small>
                </div>
            </div>
            {status === 'pending' && (
                <div className="alert-actions">
                    <button className="btn btn-danger" onClick={() => onConfirm(id)}>Confirm</button>
                    <button className="btn btn-secondary" onClick={() => onDismiss(id)}>Dismiss</button>
                </div>
            )}
        </div>
    );
};

export default AlertCard;
