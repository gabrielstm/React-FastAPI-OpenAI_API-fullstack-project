import './App.css'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import Storys from "./page/Storys.jsx"
import Register from "./page/Register.jsx"
import Login from "./page/Login.jsx"
import Logado from "./page/Logado.jsx"
import AdminLogin from "./page/AdminLogin.jsx";
import AdminPage from "./page/AdminPage.jsx";

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <h1>Interactive Story Generator</h1>
        </header>
        <main>
          <Routes>
            <Route path={"/stories"} element={<Storys />}/>
            <Route path={"/"} element={<Login />}/>
            <Route path={"/register"} element={<Register />}/>
            <Route path={"/logado"} element={<Logado />}/>
            <Route path={"/story/:id"} element={<StoryLoader />} />
            <Route path={"/admin-login"} element={<AdminLogin />} />
            <Route path={"/admin"} element={<AdminPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
