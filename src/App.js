import React from 'react';
import EventManagerVTT from './events-vtt.js';
import './App.css';

// Example video:
const VIDEO_SRC = "https://cdn.lbryplayer.xyz/api/v3/streams/free/jadecominghomereaction/706d6f8f8a046e144d83fb056581ac2837cbb808/7799df"
const CHANNEL_URL = "https://lbry.tv/@VilmaTheKitty:3"
const VIDEO_URL = "https://lbry.tv/@VilmaTheKitty:3/jadecominghomereaction:7"
function App() {
  const player = React.useRef(null);
  const [cueState, setCueState] = React.useState({ title: null, show: false })

  // Basic event handler.
  // You can use any state manager like Redux to handle this events.
  function handleCueEvents(cueEvent) {
    if (cueEvent.type === "link") {
      const { title, type } = cueEvent
      setCueState({title, type, show: true })
    }
    if (cueEvent.type === "poll") {
      const { title, type } = cueEvent
      setCueState({title, type, show: true })
    }
  }

  function hideOverlay() {
    setCueState({ show: false })
  }

  React.useEffect(() => {
    if(player && player.current) {
      const test = new EventManagerVTT(player.current, {});

      test.addEventListener('event:start', (event) => {
        handleCueEvents(event.detail.data)
        // debug
        console.info("New event requested:", event.detail)
      })

      test.addEventListener('event:end', (event) => {
        hideOverlay()
        // debug
        console.info("Event life time reached:", event.detail)
      })
    }

  }, [ player ])
  return (
    <div className="App">
      <header className="App-header">
        <h1>Interactive video - Demo 🚀</h1>
      </header>
      <div className="App-content">
      { cueState.show && (
        <div className="App-overlay">
          <div>{cueState.title}</div>
          {cueState.type === 'poll' && <button onClick={hideOverlay}>No</button> }
          {cueState.type === 'poll'&& <button onClick={hideOverlay}>Yes</button> }
        </div>
        ) }
        <video ref={player} src={VIDEO_SRC} controls crossOrigin={"anonymous"}>
          <track default src="./events.vtt" kind="metadata" label="events" />
        </video>
      </div>
      <footer>
        <div>Demo video by <a href={CHANNEL_URL}>@VilmaTheKitty</a> published on <a href={VIDEO_URL}>Lbry</a></div>
      </footer>
    </div>
  );
}

export default App;
