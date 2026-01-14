import React, { useEffect, useState } from 'react'
import { listenAlerts, updateAlertStatus } from '../services/firebase'

export default function AlertList(){
  const [alerts, setAlerts] = useState([])

  useEffect(()=>{
    const unsub = listenAlerts(setAlerts)
    return ()=> unsub()
  }, [])

  return (
    <div>
      {alerts.length === 0 && <div>No active alerts</div>}
      {alerts.map(a => (
        <div key={a.id} className="alert-card">
          <div className="alert-meta">
            <div>
              <strong>{a.location_id || a.camera_id}</strong>
              <div>Confidence: {(a.confidence || 0).toFixed(2)}</div>
            </div>
            <div>
              <button className="btn btn-confirm" onClick={()=>updateAlertStatus(a.id, 'confirmed', 'operator')}>Confirm Distress</button>
              <button className="btn btn-dismiss" style={{marginLeft:8}} onClick={()=>updateAlertStatus(a.id, 'dismissed', 'operator')}>Dismiss</button>
            </div>
          </div>
          <div style={{marginTop:8}}>
            <small>Status: {a.status}</small>
          </div>
        </div>
      ))}
    </div>
  )
}
