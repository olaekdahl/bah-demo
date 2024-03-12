import React, { useEffect, useState } from 'react';

const BoardGames = () => {
  const [boardGames, setBoardGames] = useState([]);

  useEffect(() => {
    fetch('http://ec2-54-197-6-33.compute-1.amazonaws.com:5000/boardgames')
      .then(response => response.json())
      .then(data => setBoardGames(data))
      .catch(error => console.error("Error fetching data: ", error));
  }, []);

  return (
    <div>
      <h1>Top Board Games</h1>
      <div>
        {boardGames.map(game => (
          <div key={game._id} style={{ margin: '20px', padding: '10px', border: '1px solid #ccc' }}>
            <img src={game.Thumbnail} alt={game.Name} />
            <h2>{game.Name} ({game.Year})</h2>
            <p>Rank: {game.Rank}</p>
            <p>Average Rating: {game.Average}</p>
            <p>Date Updated: {game.Date}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BoardGames;
