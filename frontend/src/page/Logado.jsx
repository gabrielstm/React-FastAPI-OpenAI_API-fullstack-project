import { useLocation } from 'react-router-dom';

function Logado() {
  const location = useLocation();
  const email = location.state?.email || 'usuário';

  return (
    <div className="logado-container">
      <div className="logado-card">
        <h2>Bem vindo, {email}!</h2>
        <p>Você está logado com sucesso.</p>
      </div>
    </div>
  );
}

export default Logado;