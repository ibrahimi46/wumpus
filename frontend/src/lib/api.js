export const newGame = async () => {
  const res = await fetch("http://localhost:8000/api/new-game", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  return res.json();
};

export const aiMove = async () => {
  const res = await fetch("http://localhost:8000/api/ai-move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  return res.json();
};
