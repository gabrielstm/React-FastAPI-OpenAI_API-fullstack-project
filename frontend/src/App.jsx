import './App.css'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import Storys from "./page/Storys.jsx"
import Register from "./page/Register.jsx"
import Login from "./page/Login.jsx"

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
            <Route path={"/story/:id"} element={<StoryLoader />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
