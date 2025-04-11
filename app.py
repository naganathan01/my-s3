# IPL 2025 match ID
import json
import requests
import time
from flask import Flask, render_template, jsonify, send_from_directory
import threading
import os

# Create Flask application
app = Flask(__name__)

class CricketDataFetcher:
    def __init__(self, match_id):
        """
        Initialize the Cricket Data Fetcher
        :param match_id: Cricbuzz match ID
        """
        self.match_id = match_id
        self.base_url = "https://www.cricbuzz.com/api/cricket-match/commentary/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.latest_data = None
        self.last_updated = None

    def fetch_match_data(self):
        """
        Fetch match commentary data from Cricbuzz API
        :return: JSON data of match commentary
        """
        try:
            url = f"{self.base_url}{self.match_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Update our data
            self.latest_data = data
            self.last_updated = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return data
        except requests.RequestException as e:
            print(f"Error fetching match data: {e}")
            return None

    def get_latest_data(self):
        """
        Get the latest match data along with the timestamp
        :return: Tuple of (match_data, timestamp)
        """
        return self.latest_data, self.last_updated

def update_cricket_data(fetcher, update_interval=3):
    """
    Background task to continuously update cricket data
    :param fetcher: CricketDataFetcher instance
    :param update_interval: Time between updates in seconds
    """
    while True:
        fetcher.fetch_match_data()
        time.sleep(update_interval)

# Create cricket data fetcher instance
cricket_fetcher = CricketDataFetcher("115111")  # IPL 2025 match ID

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/match-data')
def get_match_data():
    """API endpoint to get the latest match data"""
    data, timestamp = cricket_fetcher.get_latest_data()
    if data:
        return jsonify({
            'success': True,
            'data': data,
            'last_updated': timestamp
        })
    else:
        return jsonify({
            'success': False,
            'error': 'No match data available'
        }), 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

def ensure_directories_and_files():
    """Create the required directories and files"""
    # Make sure the directories exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template file
    with open('templates/index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Cricket Match Summary</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Live Cricket Match Summary</h1>
        
        <div class="header">
            <div class="last-update">Last Updated: <span id="last-updated">Loading...</span></div>
            <div class="refresh-countdown">Next refresh in <span id="countdown">3</span>s</div>
        </div>
        
        <div id="loading" class="loading">Loading match data...</div>
        
        <div id="match-content" style="display: none;">
            <!-- First row with match details -->
            <div class="section match-details">
                <div class="section-title">MATCH DETAILS</div>
                <div class="data-row" id="series">Series: <span id="series-name">Loading...</span></div>
                <div class="data-row" id="match-desc">Match: <span id="match-description">Loading...</span></div>
                <div class="data-row" id="teams">Teams: <span id="team-names">Loading...</span></div>
                <div class="data-row" id="toss">Toss: <span id="toss-result">Loading...</span></div>
            </div>
            
            <div class="section innings-details">
                <div class="section-title">INNINGS DETAILS</div>
                <div id="innings-scores"></div>
            </div>
            
            <div class="section match-progress">
                <div class="section-title">MATCH PROGRESS</div>
                <div class="match-status" id="match-status">Loading...</div>
                <div class="data-row" id="target">Target: <span id="target-runs">--</span></div>
                <div class="data-row" id="runs-required">Needed: <span id="req-runs">--</span></div>
                <div class="data-row" id="req-rate">RRR: <span id="req-run-rate" class="required-rate">--</span></div>
            </div>
            
            <!-- Second row with batting and bowling -->
            <div class="section batting-details">
                <div class="section-title">CURRENT BATTING</div>
                <div class="batsman">
                    <div class="name striker">
                        <span id="striker-name">Loading...</span> *
                    </div>
                    <div class="stats">
                        <span id="striker-runs">--</span> (<span id="striker-balls">--</span>)
                    </div>
                </div>
                <div class="batsman">
                    <div class="name">
                        <span id="non-striker-name">Loading...</span>
                    </div>
                    <div class="stats">
                        <span id="non-striker-runs">--</span> (<span id="non-striker-balls">--</span>)
                    </div>
                </div>
            </div>
            
            <div class="section bowling-details">
                <div class="section-title">CURRENT BOWLING</div>
                <div class="bowler">
                    <div class="name">
                        <span id="bowler-name">Loading...</span>
                    </div>
                    <div class="stats">
                        <span id="bowler-overs">--</span>-<span id="bowler-runs">--</span>-<span id="bowler-wickets">--</span>
                    </div>
                </div>
            </div>
            
            <div class="section recent-performance">
                <div class="section-title">RECENT PERFORMANCE</div>
                <div id="recent-performance">Loading...</div>
            </div>
            
            <!-- Current over section -->
            <div class="section current-over-section">
                <div class="section-title">CURRENT OVER</div>
                <div id="current-over-balls">
                    <!-- This will be populated by JavaScript -->
                </div>
            </div>
        </div>
        
        <button id="refresh-button" class="refresh-button">Refresh Now</button>
    </div>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>''')

    # Create CSS file
    with open('static/css/styles.css', 'w') as f:
        f.write('''body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.4;
    margin: 0;
    padding: 10px;
    background-color: #f0f8ff;
    color: #333;
    font-size: 14px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background-color: #fff;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 10px;
}

h1 {
    text-align: center;
    color: #0c4da2;
    margin-bottom: 15px;
    font-size: 22px;
    grid-column: span 3;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #0c4da2;
    padding-bottom: 5px;
    margin-bottom: 10px;
    grid-column: span 3;
}

.last-update,
.refresh-countdown {
    font-size: 12px;
}

.refresh-countdown {
    background-color: #0c4da2;
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
}

.section {
    background-color: #f9f9f9;
    border-left: 3px solid #0c4da2;
    border-radius: 5px;
    padding: 10px;
    height: fit-content;
    margin-bottom: 10px;
    transition: background-color 0.3s ease;
}

.section-title {
    font-weight: bold;
    color: #0c4da2;
    font-size: 14px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 3px;
    margin-bottom: 5px;
}

.match-status {
    font-weight: bold;
    color: #e74c3c;
    margin: 5px 0;
}

.team-score {
    font-weight: bold;
    margin-bottom: 4px;
}

.batsman,
.bowler {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}

.batsman .name,
.bowler .name {
    font-weight: bold;
}

.batsman .striker {
    color: #e74c3c;
}

.batsman .stats,
.bowler .stats {
    text-align: right;
}

.recent-overs {
    font-family: monospace;
    font-size: 13px;
    letter-spacing: 1.5px;
    margin-top: 8px;
}

.refresh-button {
    grid-column: span 3;
    display: block;
    margin: 10px auto 0;
    padding: 8px 12px;
    background-color: #0c4da2;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
    min-width: 120px; /* Prevent button size changes during text updates */
}

.refresh-button:hover {
    background-color: #083b7e;
}

.refresh-button:disabled {
    background-color: #b0bec5;
    cursor: not-allowed;
}

.required-rate {
    font-weight: bold;
    color: #e74c3c;
}

.loading {
    grid-column: span 3;
    text-align: center;
    font-style: italic;
    color: #666;
    padding: 20px;
}

.data-row {
    margin-bottom: 4px;
    transition: opacity 0.3s ease;
}

#match-content {
    grid-column: span 3;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 10px;
}

/* Ball styling for current over */
.current-over-section {
    grid-column: span 3; /* Make it take full width */
    padding: 15px;
    background-color: #f5f9ff;
    border-radius: 8px;
    margin-top: 10px;
}

.over-number {
    font-weight: bold;
    color: #0c4da2;
    margin-top: 5px;
    margin-bottom: 20px;
    text-align: center;
    font-size: 20px;
}

.over-balls {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    max-width: 500px;
    margin: 0 auto;
}

.ball {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    font-size: 22px;
    font-weight: bold;
    transition: transform 0.2s ease;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16);
    margin: 6px;
}

.ball:hover {
    transform: scale(1.1);
    box-shadow: 0 5px 10px rgba(0,0,0,0.2);
}

.ball-pending {
    background-color: #f0f0f0;
    color: #999;
    border: 2px dashed #ccc;
}

.ball-dot {
    background-color: #f2f2f2;
    color: #333;
    border: 2px solid #ccc;
}

.ball-run {
    background-color: #e3f2fd;
    color: #0c4da2;
    border: 2px solid #0c4da2;
}

.ball-4 {
    background-color: #e8f5e9;
    color: #2e7d32;
    border: 2px solid #2e7d32;
    font-size: 24px;
}

.ball-6 {
    background-color: #1a237e;
    color: white;
    border: 2px solid #0d1445;
    font-size: 24px;
}

.ball-wicket {
    background-color: #ffebee;
    color: #e74c3c;
    border: 2px solid #c0392b;
}

.ball-wide, .ball-noball {
    background-color: #fff3e0;
    color: #e65100;
    border: 2px solid #e65100;
}

.ball-bye, .ball-legbye {
    background-color: #f3e5f5;
    color: #7b1fa2;
    border: 2px solid #7b1fa2;
}

/* Updated animation for new content */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.new-data {
    animation: highlight 2s ease-in-out;
}

@keyframes highlight {
    0% { background-color: #f9f9f9; }
    30% { background-color: #fffde7; }
    100% { background-color: #f9f9f9; }
}''')

    # Create JavaScript file
    with open('static/js/script.js', 'w') as f:
        f.write('''let refreshInterval = 3000; // 3 seconds
let countdownInterval;
let countdown = 3;
let isFirstLoad = true; // Track if this is the first load

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
});''')

if __name__ == "__main__":
    print("Starting the cricket match live update server...")
    
    # Create necessary directories and files
    ensure_directories_and_files()
    
    # Get initial data
    cricket_fetcher.fetch_match_data()
    
    # Start the background thread for continuous updates
    updater_thread = threading.Thread(
        target=update_cricket_data, 
        args=(cricket_fetcher, 3),  # Update every 3 seconds
        daemon=True
    )
    updater_thread.start()
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)