import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../util';

function Register() {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Validate email
    if (!formData.email) {
      newErrors.email = 'Email é obrigatório';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    // Validate password
    if (!formData.password) {
      newErrors.password = 'Senha é obrigatória';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Senha deve ter pelo menos 6 caracteres';
    }

    // Validate confirm password
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Confirmação de senha é obrigatória';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'As senhas não coincidem';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setErrors({});
    setSuccessMessage('');

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, {
        email: formData.email,
        password: formData.password
      });

      console.log('Registro bem-sucedido:', response.data);
      setSuccessMessage('Registro realizado com sucesso! Redirecionando...');
      
      // Reset form
      setFormData({
        email: '',
        password: '',
        confirmPassword: ''
      });

      // Redirect to home page after 2 seconds
      setTimeout(() => {
        navigate('/');
      }, 2000);

    } catch (error) {
      console.error('Erro no registro:', error);
      
      if (error.response) {
        // Error response from backend
        const errorMessage = error.response.data.detail || 'Erro ao registrar usuário';
        
        // Check if it's an email already exists error
        if (error.response.status === 400 && errorMessage.includes('já cadastrado')) {
          setErrors({ email: errorMessage });
        } else {
          setErrors({ general: errorMessage });
        }
      } else if (error.request) {
        // No response from server
        setErrors({ general: 'Não foi possível conectar ao servidor. Verifique se o backend está rodando.' });
      } else {
        // Other errors
        setErrors({ general: 'Erro ao processar requisição' });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2>Registrar</h2>
        
        {successMessage && (
          <div className="success-banner">
            {successMessage}
          </div>
        )}
        
        {errors.general && (
          <div className="error-banner">
            {errors.general}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="seu@email.com"
              className={errors.email ? 'error' : ''}
              disabled={loading}
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Senha</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Digite sua senha"
              className={errors.password ? 'error' : ''}
              disabled={loading}
            />
            {errors.password && <span className="error-message">{errors.password}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirmar Senha</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirme sua senha"
              className={errors.confirmPassword ? 'error' : ''}
              disabled={loading}
            />
            {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
          </div>

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Registrando...' : 'Registrar'}
          </button>
        </form>
        
        <div className="login-link">
          <p>Já tem uma conta? <a href="/">Voltar para home</a></p>
        </div>
      </div>
    </div>
  );
}

export default Register;
