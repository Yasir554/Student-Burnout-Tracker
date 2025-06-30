import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import { FaMoon, FaSun } from 'react-icons/fa';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext'; 
import '../style/Global.css';
import '../style/pages/LoginPage.css';

const decodeJWT = (token) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (err) {
    console.error('Failed to decode token:', err);
    return null;
  }
};

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const buttonRef = useRef(null);
  const navigate = useNavigate();
  const { setCurrentUser } = useAuth();
  const { theme, toggleTheme, isDark } = useTheme();

  const handleMouseMove = (e) => {
    const button = buttonRef.current;
    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    button.style.setProperty('--x', `${x}px`);
    button.style.setProperty('--y', `${y}px`);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username_or_email: email, password }),
      });

      const data = await res.json();

      if (res.ok && data.access_token) {
        localStorage.setItem('accessToken', data.access_token);
        const decoded = decodeJWT(data.access_token);

        if (!decoded?.sub?.role || !decoded?.sub?.username) {
          throw new Error('Missing role or username in token');
        }

        localStorage.setItem('role', decoded.sub.role);
        localStorage.setItem('user_id', decoded.sub.id);
        localStorage.setItem('username', decoded.sub.username);

        setCurrentUser({
          role: decoded.sub.role,
          userId: decoded.sub.id,
          username: decoded.sub.username,
        });

        setSuccessMsg('Login successful!');
        setEmail('');
        setPassword('');
        navigate(`/${decoded.sub.username}/profile`);
      } else {
        setErrorMsg(data.error || 'Login failed.');
      }
    } catch (err) {
      console.error('Login error:', err);
      setErrorMsg('Network error or server not responding.');
    } finally {
      setLoading(false);
    }
  };

  const logoSrc = isDark ? "/logo.png" : "/logo2.png";

  return (
    <div className="LoginLandingPage">
      <button className="theme-toggle-button-landing-login" onClick={toggleTheme}>
        {theme === 'dark' ? <FaSun /> : <FaMoon />}
      </button>
      <img src={logoSrc} alt="Logo" className="logoimage" />
      <h1 className="Mannol">Student Burnout Tracker</h1>
      <form onSubmit={handleSubmit} className="L-Container">
        <h2 className="L-message">Login</h2>
        {errorMsg && <p className="error-msg">{errorMsg}</p>}
        {successMsg && <p className="success-msg">{successMsg}</p>}
        <div className="input-group">
          <input id="email" type="text" value={email}
            onChange={e => {
              setEmail(e.target.value);
              setErrorMsg('');
            }} placeholder=" " required autoComplete="username"
          />
          <label htmlFor="email">Email or Username</label>
        </div>
        <div className="input-group password-group">
          <input id="password" type={showPassword ? 'text' : 'password'} value={password}
            onChange={e => {
              setPassword(e.target.value);
              setErrorMsg('');
            }} placeholder=" " required autoComplete="current-password"
          />
          <label htmlFor="password">Password</label>
          <span className="toggle-password" onClick={() => setShowPassword(prev => !prev)} title={showPassword ? 'Hide password' : 'Show password'} >
            {showPassword ? <FiEyeOff /> : <FiEye />}
          </span>
        </div>
        <button type="submit" disabled={loading} ref={buttonRef} className="login" onMouseMove={handleMouseMove} >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default Login;
