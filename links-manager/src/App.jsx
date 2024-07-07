import { useState } from 'react'

import './App.css'

export default function App() {
  const [currentTime, setCurrentTime] = useState(0);
  
  useEffect(() => {
    fetch('/api/time',).then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
      <div className='App'>
        <header className="App-header">
        <p>Current time is {currentTime}</p>
        </header>
      </div>
  );
}
