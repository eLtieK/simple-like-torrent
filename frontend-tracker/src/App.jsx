import './App.css';
import Home from "./views/pages/Home/Home"

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Peer Tracker</h1>
      </header>
      <main>
        <Home />
      </main>
      <div className="arrow-container">
        <span className="arrow"></span>
      </div>
    </div>
  );
}

export default App;
