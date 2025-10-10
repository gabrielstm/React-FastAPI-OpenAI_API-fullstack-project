import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("adminToken");
    if (!token) {
      navigate("/admin-login");
      return;
    }
    fetch("/api/admin/data", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(res => res.json())
      .then(json => setData(json))
      .catch(() => setError("Erro ao buscar dados"));
  }, [navigate]);

  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (!data) return <div>Carregando...</div>;

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: 24 }}>
      <h2>Dados do Banco</h2>
      <div style={{ maxWidth: 600, margin: "0 auto" }}>
        <h3>Usuários</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f0f0f0" }}>
              <th>ID</th>
              <th>Email</th>
              <th>Foto</th>
              <th>Criado em</th>
            </tr>
          </thead>
          <tbody>
            {data.users.map(u => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.email}</td>
                <td>{u.profile_pic ? <img src={u.profile_pic.startsWith('/uploads/') ? u.profile_pic : `/uploads/${u.profile_pic}`} alt="pic" style={{width:32, height:32, borderRadius:16}}/> : '-'}</td>
                <td>{u.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AdminPage;
