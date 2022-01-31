import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button onClick={performRequest}>Perform request</button>
      </header>
    </div>
  );
}

function performRequest() {
  axios.get(`http://127.0.0.1:8000/api/todos/`)
  .then(res => {
    const persons = res.data;
    console.log(persons);
  })
}

export default App;
