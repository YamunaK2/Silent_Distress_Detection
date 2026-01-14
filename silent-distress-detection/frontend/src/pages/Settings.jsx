import React, { useState } from 'react';

const Settings = () => {
    const [threshold, setThreshold] = useState(0.6);
    const [enableAudio, setEnableAudio] = useState(true);

    return (
        <div className="page-container">
            <h1>System Settings</h1>

            <div className="settings-card">
                <div className="form-group">
                    <label>Confidence Threshold ({threshold})</label>
                    <input
                        type="range"
                        min="0.1"
                        max="1.0"
                        step="0.05"
                        value={threshold}
                        onChange={(e) => setThreshold(parseFloat(e.target.value))}
                    />
                    <small>Alerts will trigger only if AI confidence exceeds this value.</small>
                </div>

                <div className="form-group checkbox-group">
                    <label>
                        <input
                            type="checkbox"
                            checked={enableAudio}
                            onChange={(e) => setEnableAudio(e.target.checked)}
                        />
                        Enable Audio Analysis
                    </label>
                </div>

                <button className="btn btn-primary">Save Configuration</button>
            </div>
        </div>
    );
};

export default Settings;
