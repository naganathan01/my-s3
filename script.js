let refreshInterval = 3000; // 3 seconds
let countdownInterval;
let countdown = 3;
let isFirstLoad = true; // Track if this is the first load

// Team logo mapping (you would replace these with actual logo paths)
const teamLogos = {
    'Gujarat Titans': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhAviPjlBbeRYz6ny9-HOVtr9VmyQJ3FXOw60rSy8ye_U_nMy9gPWtgEPpPMAO7va36UX6nyw9BNvWVrC5kwShXJT3V7FtA5HmDO9aAwsBS4iGQWFRQWOX_ltiBkSajurq-ulo_Mu82VYsIMDkIme9jCuqMxKTt0P1fO9bv_tdXBzYj51QgTcD7pz-2/s1024/Original%20Gujarat%20Titans%20Logo%20PNG-SVG%20File%20Download%20Free%20Download.png', // Replace with actual logo paths
    'Rajasthan Royals': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgHxGVAL3asVmq-N8vAbTJ0Wk1C7WQNO4yr_O-7dIDgrszmr7L1ODXPuc5IzB8VGr941igDjeEX8OSZ1db2sDpn5uziRk1BVYAVRZBltH4A5FJGhfjmn8PzDLcP7qxCXVyuYQr1uaLktAqoNefxAgjVGXGXIcec8WYXBO4lB-4vtCCmcu2C9RhG5XXm/s1024/Original%20Rajasthan%20Royals%20Logo%20PNG-SVG%20File%20Download%20Free%20Download.png',
    'Mumbai Indians': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhcIHFJONN-c6wVsb8I0TI5u1He8Vh5aUlmZ7vPzd6paraXfCf5r-bNdOoT3rqBA5S8Yu3DwefbB4C_Utu6a4E1XUXtdo28k2ViLDYs2fDS7cG9LO0S6ESd5pEZrE1GvYAf6M0_dTs9OibYMQAwkOQZvALvo-ggMxtTh_4JINiQsYeBWtQ0APFedzCZ/s7200/Original%20Mumbai%20Indians%20PNG-SVG%20File%20Download%20Free%20Download.png',
    'Chennai Super Kings': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhn3plcgt5OnAx_VelXAj9Z8TWBiqg6B-xgCJ__kuFeXr1ClntuhvVu0IugURU6TfyHk9qUuECEpos1E5ayEmx0fAupMIvNLQnLOwavDhBYxkIwvRv9cmm7_qHZmlcSwr3Un-hJpy92AooR9Qn77PUcr4yRgAORYwoTBjTYOmyYlHbZ0nDyaL3HWqUk/w400-h330/Original%20Chennai%20Super%20Fun%20Logo%20PNG%20-%20SVG%20File%20Download%20Free%20Download.png',
    'Royal Challengers Bangalore': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgEMirAmSelGzQqwMqkzMifgCNy9asa4lGjk7tFe7WlVAQ3NU7eGj8nP0c-NRXNY6ZN5FgrDJV0k_UjOLa8rUHJDfEzFsj9qxgL_DxfB0y4RlFli0AnCxNqWXZ9wCATAZ1FBoZafwsUWddYNpVOyBEAxK7yIdLy4OkVjkUMEDErfWKE_54Rt2WW9iXL/w271-h400/Original%20Royal%20Challengers%20Bangalore%20PNG-SVG%20File%20Download%20Free%20Download.png',
    'Kolkata Knight Riders': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhw4FPuHDf0g4n2Gaf_prBrTXdS7GO6zGVcS-Lx4ioHzH-HUUGm5gY7Sj2vmy_6HwxtSZ2fojvZrXqCUIljlZy_aenyml7DLwx3mRXTS-qWBHsBFpt85nq8Y7__HB6uK3JystxJDwx0KoLubgsAIWIH6xXoh2nxjLDM2bNV08uHlBj3zy6SQmfSIUuZ/s1024/Original%20Kolkata%20Knight%20Riders%20PNG-SVG%20File%20Download%20Free%20Download.png',
    'Delhi Capitals': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixNFCNIFm0aH1xUBTkbrLQdE__aSNP32JP1zsee3iJW5va96W_r3qyl486fHQilJQjaVBJt0Fl0xAawdBD4duYEg6Sj-MgCNvVfWuA3UpO4oXBr4qt8WeaaS2Fhtbac8mfzE_euPhJ9hQUVxAgWQDLG1WgrJaSv1I2L4XgNGvFoxrdWQq_LUi82XIw/s944/Original%20Delhi%20Capitals%20Logo%20PNG-SVG%20File%20Download%20Free%20Download.png',
    'Punjab Kings': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjWofXDOj6B3eYR3eBKQaPeJjTsblyohHrqK1JO4BEojD0u_Izr_2kIxmrI7Oli8_EvW9tNxB4Qi_OotqkyIWTkOsg6xIroj5U39vvmbGDPSJJXkSn5mzAF58_Mz5Fg8uIrXfJnXWlWrqSig2uxfuUGCrV3wPlZwuZ1OtWVXZUhWYeIzJyrH7klLVer/s1540/Original%20Punjab%20Kings%20PNG-SVG%20File%20Download%20Free%20Download.png',
    'Sunrisers Hyderabad': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFNUOHxX-5sofC3Iioht3A6_naxWEImhNUKs6eU6xqjxYJjOa1OLc_hxKRkckg_F6bnG2XzSrAsKQpgYpeXPzFkwNLHQwS5xVrYaL7aKn155nR2J0dPCunLn4LrR8d-bLjqfaLhpAG2tGRZF4RuWgblEy_1DhbmszchchOWOs3ZwAZ_Lj-1bT535Ye/s7200/Original%20Sunrisers%20Hyderabad%20PNG-SVG%20File%20Download%20Free%20Download.png',
    'Lucknow Super Giants': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEijb28SNOESbzSkJ5J8-YuxEweSWpHRLhF_uQ5Ceah9b61K8ytbL8fwmK9oMKbM2-ZZxlualj5wlNPlriod0mdrFFXBSx0dj0-_4DQIXwZmGkleqqiIpr0GmV7V8dkYbLXisxjWUPtf4joGikLHSiExgCpaO477APLpjA8_pGhnlvUEAJM4_TvabF85/s7201/Original%20Lucknow%20Super%20Giants%20PNG-SVG%20File%20Download%20Free%20Download.png'
};

// Function to fetch match data from the Python API
async function fetchMatchData() {
    try {
        // Only hide content on first load, not during refreshes
        if (isFirstLoad) {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('match-content').style.display = 'none';
        } else {
            // Use a less intrusive loading indicator for subsequent loads
            document.getElementById('refresh-button').disabled = true;
            document.getElementById('refresh-button').textContent = 'Updating...';
        }

        const response = await fetch('/api/match-data');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        if (result.success) {
            updateMatchSummary(result.data);
            updateTeamDisplay(result.data);
            updateCurrentOverDisplay(result.data);
            document.getElementById('last-updated').textContent =
                new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        } else {
            throw new Error(result.error || "Unknown error");
        }

        // Show content after first load
        if (isFirstLoad) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('match-content').style.display = 'grid';
            isFirstLoad = false;
        }

        // Re-enable the refresh button
        document.getElementById('refresh-button').disabled = false;
        document.getElementById('refresh-button').textContent = 'Refresh Now';

        // Start countdown
        startCountdown();

    } catch (error) {
        console.error("Error fetching match data:", error);
        if (isFirstLoad) {
            document.getElementById('loading').textContent = "Error loading match data. Please try again.";
            document.getElementById('loading').style.display = 'block';
        } else {
            alert("Error refreshing data. Please try again.");
            document.getElementById('refresh-button').disabled = false;
            document.getElementById('refresh-button').textContent = 'Refresh Now';
        }
    }
}

// Function to update team display with logos and scores
function updateTeamDisplay(data) {
    if (!data || !data.matchHeader) return;
    
    const matchHeader = data.matchHeader;
    const miniscore = data.miniscore || {};
    const matchScoreDetails = miniscore.matchScoreDetails || {};
    const inningsScores = matchScoreDetails.inningsScoreList || [];
    
    // Team 1 data
    if (matchHeader.team1) {
        const team1Name = matchHeader.team1.name;
        document.getElementById('team1-name').textContent = team1Name;
        document.getElementById('team1-logo').alt = team1Name;
        
        // Set team logo if available in our mapping
        if (teamLogos[team1Name]) {
            document.getElementById('team1-logo').src = teamLogos[team1Name];
        }
        
        // Find score for team 1
        const team1Score = inningsScores.find(innings => innings.batTeamName === team1Name);
        if (team1Score) {
            document.getElementById('team1-score').textContent = 
                `${team1Score.score || '0'}/${team1Score.wickets || '0'} (${team1Score.overs || '0'})`;
        } else {
            document.getElementById('team1-score').textContent = '';
        }
    }
    
    // Team 2 data
    if (matchHeader.team2) {
        const team2Name = matchHeader.team2.name;
        document.getElementById('team2-name').textContent = team2Name;
        document.getElementById('team2-logo').alt = team2Name;
        
        // Set team logo if available in our mapping
        if (teamLogos[team2Name]) {
            document.getElementById('team2-logo').src = teamLogos[team2Name];
        }
        
        // Find score for team 2
        const team2Score = inningsScores.find(innings => innings.batTeamName === team2Name);
        if (team2Score) {
            document.getElementById('team2-score').textContent = 
                `${team2Score.score || '0'}/${team2Score.wickets || '0'} (${team2Score.overs || '0'})`;
        } else {
            document.getElementById('team2-score').textContent = '';
        }
    }
}

// Function to start countdown timer
function startCountdown() {
    clearInterval(countdownInterval);
    countdown = 3;
    document.getElementById('countdown').textContent = countdown;

    countdownInterval = setInterval(() => {
        countdown--;
        document.getElementById('countdown').textContent = countdown;

        if (countdown <= 0) {
            clearInterval(countdownInterval);
            fetchMatchData();
        }
    }, 1000);
}

// Function to update current over display
function updateCurrentOverDisplay(data) {
    const currentOverDiv = document.getElementById('current-over-balls');
    if (!data || !data.miniscore) {
        return;
    }

    const currentOver = data.miniscore.overs || '0.0';
    const overNumber = Math.floor(parseFloat(currentOver));
    let currentOverBalls = [];

    // Try to get balls from commentary
    if (data.commentaryList) {
        let foundCommentary = false;
        for (const commentary of data.commentaryList) {
            if (commentary.overNumber === overNumber) {
                foundCommentary = true;
                if (commentary.commentaryFormats && commentary.commentaryFormats.bold) {
                    const ballDescription = commentary.commentaryFormats.bold;
                    currentOverBalls.push(parseBallDescription(ballDescription));
                }
            } else if (foundCommentary) {
                break;
            }
        }
    }

    // If we couldn't find in commentary, try currentOverDetail
    if (currentOverBalls.length === 0) {
        const currentOverInfo = data.miniscore ? data.miniscore.currentOverDetail : null;
        if (currentOverInfo) {
            const ballsArray = currentOverInfo.split(' ');
            currentOverBalls = ballsArray.map(ball => parseBallDescription(ball));
        }
    }

    // Create mock data for testing if no balls are found (remove in production)
    if (currentOverBalls.length === 0) {
        // This is just for testing UI - remove this in production
        currentOverBalls = [
            { type: 'dot', value: '0' },
            { type: 'run', value: '1' },
            { type: 'run', value: '2' },
            { type: '4', value: '4' },
            { type: 'wicket', value: 'W' },
            { type: '6', value: '6' }
        ];
    }

    // Create HTML for the current over
    let overHTML = `<div class="over-number">Over ${overNumber}</div>`;
    overHTML += `<div class="over-balls">`;

    // If there are balls, display them
    if (currentOverBalls.length > 0) {
        for (const ball of currentOverBalls) {
            overHTML += createBallHTML(ball);
        }
        
        // Add pending balls if needed to complete the over (assuming 6 balls per over)
        const remainingBalls = 6 - currentOverBalls.length;
        for (let i = 0; i < remainingBalls; i++) {
            overHTML += `<div class="ball ball-pending"></div>`;
        }
    } else {
        // If no balls are found, show pending balls
        for (let i = 0; i < 6; i++) {
            overHTML += `<div class="ball ball-pending"></div>`;
        }
    }
    
    overHTML += `</div>`;
    currentOverDiv.innerHTML = overHTML;
}

// Function to parse ball description
function parseBallDescription(description) {
    if (!description) return { type: 'dot', value: '0' };

    description = description.toString().trim();

    if (description.includes('W') || description.includes('OUT')) return { type: 'wicket', value: 'W' };
    if (description === '4' || description.includes('FOUR')) return { type: '4', value: '4' };
    if (description === '6' || description.includes('SIX')) return { type: '6', value: '6' };
    if (description.includes('WD') || description.toLowerCase().includes('wide')) return { type: 'wide', value: 'WD' };
    if (description.includes('NB') || description.toLowerCase().includes('no ball')) return { type: 'noball', value: 'NB' };
    if (description.includes('B') || description.toLowerCase().includes('bye')) return { type: 'bye', value: 'B' };
    if (description.includes('LB') || description.toLowerCase().includes('leg bye')) return { type: 'legbye', value: 'LB' };
    if (description === '0' || description === '.' || description === '•') return { type: 'dot', value: '0' };

    const runs = parseInt(description);
    if (!isNaN(runs) && runs > 0 && runs < 4) return { type: 'run', value: runs.toString() };

    return { type: 'dot', value: '0' };
}

// Function to create ball HTML
function createBallHTML(ball) {
    let className = 'ball';
    switch (ball.type) {
        case 'wicket': className += ' ball-wicket'; break;
        case '4': className += ' ball-4'; break;
        case '6': className += ' ball-6'; break;
        case 'wide': className += ' ball-wide'; break;
        case 'noball': className += ' ball-noball'; break;
        case 'bye': className += ' ball-bye'; break;
        case 'legbye': className += ' ball-legbye'; break;
        case 'run': className += ' ball-run'; break;
        default: className += ' ball-dot'; break;
    }
    return `<div class="${className}">${ball.value}</div>`;
}

// Function to update match summary
function updateMatchSummary(data) {
    if (!data) return;

    const matchHeader = data.matchHeader || {};
    const miniscore = data.miniscore || {};
    const matchScoreDetails = miniscore.matchScoreDetails || {};

    // Update series and match info
    if (document.getElementById('series-name')) {
        document.getElementById('series-name').textContent = matchHeader.seriesName || 'N/A';
    }
    
    if (document.getElementById('match-description')) {
        document.getElementById('match-description').textContent = matchHeader.matchDescription || 'N/A';
    }

    // Update team names
    if (document.getElementById('team-names')) {
        const team1 = matchHeader.team1 ? matchHeader.team1.name : 'Team 1';
        const team2 = matchHeader.team2 ? matchHeader.team2.name : 'Team 2';
        document.getElementById('team-names').textContent = `${team1} vs ${team2}`;
    }

    // Update toss result
    if (document.getElementById('toss-result')) {
        if (matchHeader.tossResults) {
            const tossWinner = matchHeader.tossResults.tossWinnerName || 'N/A';
            const decision = matchHeader.tossResults.decision || 'N/A';
            document.getElementById('toss-result').textContent = `${tossWinner} chose to ${decision}`;
        } else {
            document.getElementById('toss-result').textContent = 'N/A';
        }
    }

    // Update innings scores
    if (document.getElementById('innings-scores')) {
        const inningsScores = matchScoreDetails.inningsScoreList || [];
        let inningsHTML = '';

        for (const innings of inningsScores) {
            inningsHTML += `
                <div class="team-score">
                    ${innings.batTeamName || 'Team'}: 
                    ${innings.score || '0'}/${innings.wickets || '0'} 
                    (${innings.overs || '0'})
                </div>
            `;
        }

        document.getElementById('innings-scores').innerHTML = inningsHTML || 'No innings data available';
    }

    // Update match status
    if (document.getElementById('match-status')) {
        document.getElementById('match-status').textContent = miniscore.status || 'Match Status Not Available';
    }
    
    // Update target info
    if (document.getElementById('target-runs')) {
        document.getElementById('target-runs').textContent = miniscore.target || '--';
    }
    
    if (document.getElementById('req-runs')) {
        document.getElementById('req-runs').textContent = miniscore.remRunsToWin || '--';
    }
    
    if (document.getElementById('req-run-rate')) {
        document.getElementById('req-run-rate').textContent = miniscore.requiredRunRate || '--';
    }

    // Update batsman info
    const striker = miniscore.batsmanStriker || {};
    const nonStriker = miniscore.batsmanNonStriker || {};

    if (document.getElementById('striker-name')) {
        document.getElementById('striker-name').textContent = striker.batName || 'N/A';
    }
    
    if (document.getElementById('striker-runs')) {
        document.getElementById('striker-runs').textContent = striker.batRuns || '0';
    }
    
    if (document.getElementById('striker-balls')) {
        document.getElementById('striker-balls').textContent = striker.batBalls || '0';
    }

    if (document.getElementById('non-striker-name')) {
        document.getElementById('non-striker-name').textContent = nonStriker.batName || 'N/A';
    }
    
    if (document.getElementById('non-striker-runs')) {
        document.getElementById('non-striker-runs').textContent = nonStriker.batRuns || '0';
    }
    
    if (document.getElementById('non-striker-balls')) {
        document.getElementById('non-striker-balls').textContent = nonStriker.batBalls || '0';
    }

    // Update bowler info
    const bowlingStriker = miniscore.bowlerStriker || {};
    
    if (document.getElementById('bowler-name')) {
        document.getElementById('bowler-name').textContent = bowlingStriker.bowlName || 'N/A';
    }
    
    if (document.getElementById('bowler-overs')) {
        document.getElementById('bowler-overs').textContent = bowlingStriker.bowlOvs || '0';
    }
    
    if (document.getElementById('bowler-runs')) {
        document.getElementById('bowler-runs').textContent = bowlingStriker.bowlRuns || '0';
    }
    
    if (document.getElementById('bowler-wickets')) {
        document.getElementById('bowler-wickets').textContent = bowlingStriker.bowlWkts || '0';
    }

    // Update recent performance info
    if (document.getElementById('recent-performance')) {
        const recentPerformance = miniscore.latestPerformance || [];
        let performanceHTML = '';
        
        if (recentPerformance.length > 0) {
            for (const perf of recentPerformance) {
                performanceHTML += `
                    <div class="data-row">
                        ${perf.label || 'N/A'}: ${perf.runs || '0'} runs, ${perf.wkts || '0'} wkts
                    </div>
                `;
            }
        } else {
            performanceHTML = 'No recent performance data available';
        }

        document.getElementById('recent-performance').innerHTML = performanceHTML;
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    fetchMatchData();
    document.getElementById('refresh-button').addEventListener('click', () => {
        clearInterval(countdownInterval);
        fetchMatchData();
    });
});