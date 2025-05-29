import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function Result() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const result = state?.result;

  if (!result) {
    return (
      <div className="container text-center mt-5">
        <h4>No result found!</h4>
        <button className="btn btn-primary mt-3" onClick={() => navigate('/')}>
          Go Back to Upload
        </button>
      </div>
    );
  }

  const { score, quality, message, suggestions = [] } = result;

  return (
    <div className="container mt-5">
      <div className="card shadow p-4">
        <h3 className="text-center mb-4">📊 Resume Analysis Result</h3>

        <p><strong>✅ Resume Score:</strong> <span className="text-success">{score}%</span></p>
        <p><strong>📈 Quality:</strong> {quality || 'N/A'}</p>
        <p><strong>📌 Status:</strong> {message}</p>

        {suggestions.length > 0 && (
          <div className="mt-4">
            <p className="fw-bold">💡 Suggestions for Improvement:</p>
            <ul>
              {suggestions.map((tip, idx) => (
                <li key={idx}>{tip}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="text-center mt-4">
          <button className="btn btn-outline-secondary" onClick={() => navigate('/')}>
            Analyze Another Resume
          </button>
        </div>
      </div>
    </div>
  );
}

export default Result;
