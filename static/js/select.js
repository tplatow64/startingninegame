(function() {

  const teamDict = {
    "Anaheim Angels": "Anaheim Angels",
    "Arizona Diamondbacks": "Arizona Diamondbacks",
    "Atlanta Braves": "Atlanta Braves",
    "Baltimore Orioles": "Baltimore Orioles",
    "Boston Red Sox": "Boston Red Sox",
    "Chicago Cubs": "Chicago Cubs",
    "Chicago White Sox": "Chicago White Sox",
    "Cincinnati Reds": "Cincinnati Reds",
    "Cleveland Guardians": "Cleveland Guardians",
    "Cleveland Indians": "Cleveland Indians",
    "Colorado Rockies": "Colorado Rockies",
    "Detroit Tigers": "Detroit Tigers",
    "Florida Marlins": "Florida Marlins",
    "Houston Astros": "Houston Astros",
    "Kansas City Royals": "Kansas City Royals",
    "Los Angeles Angels": "Los Angeles Angels",
    "Los Angeles Angels of Anaheim": "Los Angeles Angels of Anaheim",
    "Los Angeles Dodgers": "Los Angeles Dodgers",
    "Miami Marlins": "Miami Marlins",
    "Milwaukee Brewers": "Milwaukee Brewers",
    "Minnesota Twins": "Minnesota Twins",
    "Montreal Expos": "Montreal Expos",
    "New York Mets": "New York Mets",
    "New York Yankees": "New York Yankees",
    "Oakland Athletics": "Oakland Athletics",
    "Philadelphia Phillies": "Philadelphia Phillies",
    "Pittsburgh Pirates": "Pittsburgh Pirates",
    "San Diego Padres": "San Diego Padres",
    "San Francisco Giants": "San Francisco Giants",
    "Seattle Mariners": "Seattle Mariners",
    "St. Louis Cardinals": "St. Louis Cardinals",
    "Tampa Bay Devil Rays": "Tampa Bay Devil Rays",
    "Tampa Bay Rays": "Tampa Bay Rays",
    "Texas Rangers": "Texas Rangers",
    "Toronto Blue Jays": "Toronto Blue Jays",
    "Washington Nationals": "Washington Nationals"
  };

  // create year boundaries
  const minYear = 2000;
  const maxYear = 2024;

  // some teams have special year ranges, so we can filter the year dropdown based on the team selection
  const teamYearRanges = {
    "Anaheim Angels": [minYear, 2004],
    "Loas Angeles Angels of Anaheim": [2005, 2015],
    "Los Angeles Angels": [2016, maxYear],
    "Florida Marlins": [minYear, 2011],
    "Miami Marlins": [2012, maxYear],
    "Montreal Expos": [minYear, 2004],
    "Washington Nationals": [2005, maxYear],
    "Tampa Bay Devil Rays": [minYear, 2007],
    "Tampa Bay Rays": [2008, maxYear],
    "Cleveland Indians": [minYear, 2021],
    "Cleveland Guardians": [2022, maxYear],
    "": [minYear, maxYear] // default for "Any" option
  };

  const modal = document.getElementById("filterModal");
  const openBtn = document.getElementById("newGame");
  const closeBtn = document.getElementById("closeFilterModal");
  const applyBtn = document.getElementById("applyFilters");
  const teamSelect = document.getElementById("teamSelect");
  const yearSelect = document.getElementById("yearSelect");

  // Populate team dropdown
  function populateTeams() {
    teamSelect.innerHTML = "";

    const anyOption = document.createElement("option");
    anyOption.value = "";
    anyOption.textContent = "Any";
    teamSelect.appendChild(anyOption);

    Object.entries(teamDict).forEach(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;     // URL value
      option.textContent = label; // Display text
      teamSelect.appendChild(option);
    });
  }

  function populateYears() {
    yearSelect.innerHTML = "";
    const anyOption = document.createElement("option");
    anyOption.value = "";
    anyOption.textContent = "Any";
    yearSelect.appendChild(anyOption);
    let startYear = minYear;
    let endYear = maxYear;
    const selectedTeam = teamSelect.value;
    if (selectedTeam && teamYearRanges[selectedTeam]) {
      [startYear, endYear] = teamYearRanges[selectedTeam];
    }

    for (let year = startYear; year <= endYear; year++) {
      const option = document.createElement("option");
      option.value = year;
      option.textContent = year;
      yearSelect.appendChild(option);
    }
  }

  teamSelect.addEventListener("change", populateYears);

  function syncFromURL() {
    const params = new URLSearchParams(window.location.search);
    teamSelect.value = params.get("team") || "";
    yearSelect.value = params.get("year") || "";
  }

  function updateURL() {
    const url = new URL(window.location);
    const params = url.searchParams;

    if (teamSelect.value) {
      params.set("team", teamSelect.value);
    } else {
      params.delete("team");
    }

    if (yearSelect.value) {
      params.set("year", yearSelect.value);
    } else {
      params.delete("year");
    }

    // reload the page
    window.location.search = params.toString();
  }

  openBtn.onclick = () => {
    syncFromURL();
    modal.style.display = "flex";
  };

  closeBtn.onclick = () => {
    modal.style.display = "none";
  };

  applyBtn.onclick = () => {
    updateURL();
    modal.style.display = "none";
  };

  // Close when clicking outside
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
  });

  document.addEventListener("DOMContentLoaded", () => {
    populateTeams();
    syncFromURL();
    populateYears();
  });

})();