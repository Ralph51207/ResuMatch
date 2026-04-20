async function matchResume() {
    const resumeText = document.getElementById('resume-input').value.trim();

    if (!resumeText) {
        alert('Please paste your resume text first!');
        return;
    }

    const btn = document.getElementById('match-btn');
    btn.textContent = 'Matching...';
    btn.disabled = true;

    try {
        const response = await fetch('http://127.0.0.1:5000/match', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume: resumeText })
        });

        const data = await response.json();
        displayResults(data.matches);
    } catch (error) {
        alert('Error connecting to backend. Make sure Flask is running!');
    } finally {
        btn.textContent = 'Find Matches';
        btn.disabled = false;
    }
}

function displayResults(matches) {
    const resultsDiv = document.getElementById('results');
    const matchesList = document.getElementById('matches-list');

    matchesList.innerHTML = '';
    matches.forEach((match, index) => {
        matchesList.innerHTML += `
            <div class="match-card">
                <span class="job-title">#${index + 1} ${match.job_title}</span>
                <span class="score">${match.score}%</span>
            </div>
        `;
    });

    resultsDiv.classList.remove('hidden');
}