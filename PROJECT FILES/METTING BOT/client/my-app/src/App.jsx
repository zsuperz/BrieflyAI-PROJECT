import { useState } from 'react'

function App() {
  const [chartUrl, setChartUrl] = useState('')
  const [meetingUrl, setMeetingUrl] = useState('')
  const [transcript, setTranscript] = useState('')
  const [summary, setSummary] = useState('')  // New state to hold the summary
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setTranscript('')
    setSummary('')  // Reset summary when submitting new meeting URL

    try {
      const response = await fetch('http://127.0.0.1:5003/transcribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ meeting_url: meetingUrl }),
      })

      if (response.ok) {
        const data = await response.json()
        setTranscript(data.transcript)
        setSummary(data.summary)  // Set the summary
        setChartUrl(data.chart_url)
      } else {
        console.error('Error fetching transcript or summary')
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }


  
  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
     <div className="absolute top-7 text-7xl font-extrabold bg-gradient-to-r from-pink-500 via-yellow-400 to-blue-500 bg-[length:200%_200%] bg-clip-text text-transparent animate-gradient">
  Bot Meeting Summary App
</div>
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
  <div className="mt-6 flex flex-col items-center justify-center">
  <div className="flex space-x-2">
  <span className="w-3 h-3 bg-gray-500 rounded-full animate-dots"></span>
  <span className="w-3 h-3 bg-gray-500 rounded-full animate-dots"></span>
  <span className="w-3 h-3 bg-gray-500 rounded-full animate-dots"></span>
</div>
    <p className="mt-2 text-gray-300 font-medium">Transcribing meeting...</p>
  </div>
)}

        {transcript && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              Transcript:
            </h2>
            <pre className="bg-black text-white p-4 rounded-md whitespace-pre-wrap break-words">
              {transcript}
            </pre>
          </div>
        )}

        {summary && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              Summary of the Meeting:
            </h2>
            <pre className="bg-black text-white p-4 rounded-md whitespace-pre-wrap break-words">
              {summary}
            </pre>
          </div>
        )}

        {chartUrl && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              Speaker Chart:
            </h2>
            <img src={chartUrl} alt="Speaker chart" className="w-full h-auto rounded-md" />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
