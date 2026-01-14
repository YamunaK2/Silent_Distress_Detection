import React, { useState } from 'react'
import { auth } from '../services/firebase'
import { signInWithEmailAndPassword } from 'firebase/auth'

export default function Login({onLogin}){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  const submit = async (e)=>{
    e.preventDefault()
    try{
      await signInWithEmailAndPassword(auth, email, password)
      onLogin && onLogin()
    }catch(err){
      setError(err.message)
    }
  }

  return (
    <form onSubmit={submit} style={{maxWidth:360}}>
      <h3>Staff Login</h3>
      <div>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
      </div>
      <div style={{marginTop:8}}>
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      </div>
      <div style={{marginTop:12}}>
        <button className="btn" type="submit">Sign in</button>
      </div>
      {error && <div style={{color:'red', marginTop:8}}>{error}</div>}
    </form>
  )
}