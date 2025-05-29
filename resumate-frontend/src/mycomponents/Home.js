import axios from 'axios';
import React, { useState } from 'react';
import bgImage from './resumate-bgi.jpg';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [loading, setLoading] = useState(false); // State to track loading

  const handleResumeChange = (e) => setResume(e.target.files[0]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resume) {
      alert("Please upload a resume file.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("jobdesc", jobDesc);

    // Set loading state to true when the request starts
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/analyze/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Log and show score
      console.log(response.data);
      navigate('/result', { state: { result: response.data } });

    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      // Set loading state to false when the request ends (either success or failure)
      setLoading(false);
    }
  };

  return (
    <div style={{ position: 'relative', height: '100vh', overflow: 'hidden' }}>
      {/* Blurred Background */}
      <div
        style={{
          backgroundImage: `url(${bgImage})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'blur(5px)',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: 1
        }}
      />

      {/* Dark Overlay */}
      <div
        style={{
          backgroundColor: 'rgba(0, 0, 0, 0.5)',  // opacity 
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: 2
        }}
      />

      {/* Foreground Content */}
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100%', position: 'relative', zIndex: 3 }}>
        <div className="card p-4 shadow" style={{ width: '100%', maxWidth: '600px', backgroundColor: 'rgb(231, 221, 221)', borderRadius: '12px' }}>
          <h3 className="text-center mb-3">📄 Upload Resume for ATS Check</h3>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label fw-bold">Resume (PDF/DOCX)</label>
              <input type="file" className="form-control" onChange={handleResumeChange} accept=".pdf,.doc,.docx" required />
            </div>
            <div className="mb-3">
              <label className="form-label fw-bold">Job Description <small className="text-muted">(Optional)</small></label>
              <textarea className="form-control" rows="4" value={jobDesc} onChange={(e) => setJobDesc(e.target.value)} />
            </div>
            <button 
              type="submit" 
              className="btn btn-success w-100 d-flex justify-content-center align-items-center" 
              disabled={loading} // Disable button when loading
            >
              {loading ? (
                <div className="spinner-border text-light" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
              ) : (
                'Analyze Resume'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Home;
