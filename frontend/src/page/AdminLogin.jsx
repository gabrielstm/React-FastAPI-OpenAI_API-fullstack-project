import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (res.ok && data.token) {
        localStorage.setItem("adminToken", data.token);
        navigate("/admin");
      } else {
        setError(data.detail || "Credenciais inválidas");
      }
    } catch {
      setError("Erro ao conectar ao servidor");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "60px auto", padding: 32, boxShadow: "0 0 16px #ccc", borderRadius: 8 }}>
      <h2>Login Admin</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Usuário" value={username} onChange={e => setUsername(e.target.value)} required style={{ width: "100%", marginBottom: 12, padding: 8 }} />
        <input type="password" placeholder="Senha" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: "100%", marginBottom: 12, padding: 8 }} />
        <button type="submit" style={{ width: "100%", padding: 10, background: "#007bff", color: "#fff", border: "none", borderRadius: 4 }}>Entrar</button>
        {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}
      </form>
    </div>
  );
}

export default AdminLogin;
