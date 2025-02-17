document.addEventListener("DOMContentLoaded", () => {
  // Fetch odds data from JSON file
  fetch("scripts/odds_data.json")
    .then(response => response.json())
    .then(data => {
      updateColumn("nhl-games", data.nhl);
      updateColumn("nba-games", data.nba);
      updateColumn("mlb-games", data.mlb);
      updateColumn("nfl-games", data.nfl);
    })
    .catch(error => {
      console.error("Error loading odds data:", error);
    });
});

// Function to update each column
function updateColumn(elementId, sportData) {
  const column = document.getElementById(elementId);
  
  if (!sportData || !sportData.games || sportData.games === "No games scheduled") {
    column.innerHTML = "<p>No games scheduled</p>";
    return;
  }

  let content = "";
  sportData.games.forEach(game => {
    content += `
      <div class="game">
        <p><strong>${game.away_team} vs ${game.home_team}</strong></p>
        <p>Date: ${game.date}</p>
        <p>Odds: ${game.odds ? JSON.stringify(game.odds) : "No odds available"}</p>
      </div>
    `;
  });

  column.innerHTML = content;
}
