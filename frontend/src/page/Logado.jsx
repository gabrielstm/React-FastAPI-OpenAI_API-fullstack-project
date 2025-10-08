import { useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../util';

function Logado() {
  const location = useLocation();
  const email = location.state?.email || 'usuário';
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          setError('Token não encontrado');
          setLoading(false);
          return;
        }

        const response = await axios.get(`${API_BASE_URL}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        setUser(response.data);
      } catch (err) {
        console.error('Erro ao buscar usuário:', err);
        setError('Erro ao carregar dados do usuário');
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (loading) {
    return (
      <div className="logado-container">
        <div className="logado-card">
          <p>Carregando...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="logado-container">
        <div className="logado-card">
          <p>Erro: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="logado-container">
      <div className="logado-card">
        <h2>Bem vindo, {user?.email || email}!</h2>
        {user?.profile_pic && (
          <div className="profile-pic-container">
            <img 
              src={`${API_BASE_URL.replace('/api', '')}${user.profile_pic}`} 
              alt="Foto de perfil" 
              className="profile-pic" 
            />
          </div>
        )}
        <p>Você está logado com sucesso.</p>
      </div>
    </div>
  );
}

export default Logado;