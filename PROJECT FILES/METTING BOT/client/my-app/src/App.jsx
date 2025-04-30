import { useState } from 'react'

function App() {
  const [meetingUrl, setMeetingUrl] = useState('')
  const [transcript, setTranscript] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setTranscript('')

    try {
      const response = await fetch('http://127.0.0.1:5000/transcribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ meeting_url: meetingUrl }),
      })

      if (response.ok) {
        const data = await response.json()
        setTranscript(data.transcript)
      } else {
        console.error('Error fetching transcript')
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">


      <div className="w-full max-w-2xl bg-black rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center text-white mb-6">
          Meeting Transcription
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="meetingUrl"
              className="block text-gray-300 font-medium mb-1"
            >
              Enter Meeting URL:
            </label>
            <input
              type="text"
              id="meetingUrl"
              value={meetingUrl}
              onChange={(e) => setMeetingUrl(e.target.value)}
              placeholder="Paste meeting URL here"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-gray-600 text-white py-2 rounded-md hover:bg-gray-700 transition"
          >
            Start Transcription
          </button>
        </form>

        {loading && (
          <p className="mt-4 text-center text-gray-500 font-medium">
            Loading transcription...
          </p>
        )}

        {transcript && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              Transcript:
            </h2>
            <pre className="bg-black text-white p-4 rounded-md max-h-80 overflow-y-auto whitespace-pre-wrap break-words">
              {transcript}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
