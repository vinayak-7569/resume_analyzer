document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('uploadForm');
    const resultDiv = document.getElementById('result');
    const submitBtn = form.querySelector("button[type='submit']");
    const downloadBtn = document.getElementById('downloadBtn');
  
    form.onsubmit = async function (event) {
      event.preventDefault();
      resultDiv.innerHTML = "<p>🔍 Analyzing resume, please wait...</p>";
      submitBtn.disabled = true;
      submitBtn.textContent = "Analyzing...";
      downloadBtn.style.display = "none";
  
      const formData = new FormData(form);
      const fileInput = form.querySelector('input[type="file"]');
      const jdInput = form.querySelector('textarea[name="job_description"]');
  
      formData.append("job_description", jdInput.value);
  
      if (fileInput.files.length && !fileInput.files[0].name.toLowerCase().endsWith('.pdf')) {
        resultDiv.innerHTML = '<p style="color:red;">❌ Please upload a PDF file.</p>';
        resetButton();
        return;
      }
  
      try {
        const response = await fetch('/analyze', {
          method: 'POST',
          body: formData
        });
  
        const data = await response.json();
  
        if (data.error) {
          resultDiv.innerHTML = '<p style="color:red;">❌ Error: ' + escapeHTML(data.error) + '</p>';
          return;
        }
  
        const htmlContent = `
          <div id="analysisResult" style="max-width: 600px; margin: 0 auto; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); background: #fff; font-family: sans-serif;">
            <h2>${escapeHTML(data.name || 'Candidate')}</h2>
            <p>📧 ${escapeHTML(data.email || 'N/A')}<br>📞 +91 ${escapeHTML(data.phone || 'N/A')}</p>
  
            <h3>🎯 Career Objective</h3>
            <p>${escapeHTML(data.experience[0] || '')} ${escapeHTML(data.experience[1] || '')}</p>
  
            <h3>🎓 Education</h3>
            <ul>${data.education.map(e => `<li>${escapeHTML(e)}</li>`).join('')}</ul>
  
            <h3>💼 Experience & Projects</h3>
            <ul>${data.experience.slice(2).map(e => `<li>${escapeHTML(e)}</li>`).join('')}</ul>
  
            <h3>📋 Job Description Suggestions</h3>
            <details><summary>💡 Suggestions</summary>
            <ul>${renderSuggestions(data.suggestions)}</ul>
            </details>
  
            <h3>🛠️ Matched Skills</h3>
            <p>${escapeHTML((data.matched_skills || []).join(', ') || 'N/A')}</p>
  
            <h3>📊 Scores</h3>
            <strong>Final Score:</strong> ${escapeHTML((data.final_score || 0).toString())}<br>
            <strong>Match Score:</strong> ${escapeHTML((data.match_score || 0).toString())}%<br>
            <em>${escapeHTML(data.feedback_summary || '')}</em>
          </div>`;
  
        resultDiv.innerHTML = htmlContent;
        downloadBtn.style.display = "inline-block";
      } catch (error) {
        console.error("Error analyzing resume:", error);
        resultDiv.innerHTML = '<p style="color:red;">❌ Unexpected error occurred.</p>';
      } finally {
        resetButton();
      }
    };
  
    function resetButton() {
      submitBtn.disabled = false;
      submitBtn.textContent = "Analyze";
    }
  
    function escapeHTML(str) {
      return String(str || '').replace(/[&<>"']/g, match => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
      })[match]);
    }
  
    function renderSuggestions(suggestions) {
      return Array.isArray(suggestions) && suggestions.length > 0
        ? suggestions.map(s => `<li>${escapeHTML(s)}</li>`).join('')
        : '<li>No suggestions available</li>';
    }
  });
  
  // Download result text content
  function downloadResultAsText() {
    const content = document.getElementById("analysisResult")?.innerText;
    if (!content) return alert("No result to download");
  
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "resume_analysis.txt";
    a.click();
    URL.revokeObjectURL(url);
  }
  