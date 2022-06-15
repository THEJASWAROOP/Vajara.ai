import React, { useState, useEffect } from 'react'
import './App.css'

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition
const mic = new SpeechRecognition()

mic.continuous = true
mic.interimResults = true
mic.lang = 'en-US'

function App() {
  const [isListening, setIsListening] = useState(false)
  const [note, setNote] = useState(null)
  const [savedNotes, setSavedNotes] = useState([])

  useEffect(() => {
    handleListen()
  }, [isListening])

  const handleListen = () => {
    if (isListening) {
      mic.start()
      mic.onend = () => {
        console.log('continue..')
        mic.start()
      }
    } else {
      mic.stop()
      mic.onend = () => {
        console.log('Stopped Mic on Click')
      }
    }
    mic.onstart = () => {
      console.log('Mics on')
    }

    mic.onresult = event => {
      const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('')
      console.log(transcript)
      setNote(transcript)
      mic.onerror = event => {
        console.log(event.error)
      }
    }
  }

  const handleSaveNote = () => {
    setSavedNotes([...savedNotes, note])
    setNote('')
  }

  return (
    <>
    <div class="container d-flex justify-content-center">
    <div class="card mt-10">
     <div class="d-flex flex-row justify-content-between p-3 adiv text-white">
      <i class="fas fa-chevron"></i>
      <br/>
      <span class="pb-1">Chat</span>
      <i class="fas fa-times"></i>
    </div>
     <div class="d-flex flex-row p-3-scroll">
        <div class="chat scroll">
        <br/>
        {savedNotes.map(n => (
            <div class="chat1">
            <p key={n}>{n}</p>
        </div>
          ))}
        </div>
      </div>
      <div class="d-flex flex-row p-3">
      </div>    
      <div class="box">
          <button onClick={handleSaveNote} disabled={!note}>
            Send 
          </button>
          <button onClick={() => setIsListening(prevState => !prevState)} >
            {isListening ?  <span>🛑</span>:<span>🎙</span>}  {handleSaveNote}
          </button>
          <p>{note}</p>
         </div>
    </div>
    </div>
    </>
    )
}

export default App
