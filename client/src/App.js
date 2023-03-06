import './App.css';
import React from "react";

function App() {
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    fetch("/api")
      .then((res) => res.json())
      .then((data) => setData(data.message));
  }, []);
  // const [title, setTitle] = React.useState('');

  // const handleSubmit = (e) => {
  //   e.preventDefault();

  //   const userInput = { title };
    
  //   fetch('/api', {
  //     headers: {"Conted-Type": "application/json"},
  //     body: JSON.stringify(userInput)
  //   });
  // }


  return (
    <div className="App">
      <header className="App-header">
        <p>
          {!data ? "Loading..." : data}
        </p>
        {/* Article Selection
        <form onSubmit={handleSubmit}>
        <label>Enter an article:</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          />
          <button>Run script</button>
      </form> */}
      </header>
      
    </div>

  );
}

export default App;
