function PromptSelector({ prompt, setPrompt }) {
  return (
    <div className="mb-6">
      <label className="block mb-2">Choose Edit Style</label>

      <select
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="bg-gray-800 p-3 rounded"
      >
        <option value="shorts">Create Shorts</option>
        <option value="captions">Add Captions</option>
        <option value="highlights">Highlight Moments</option>
        <option value="cinematic">Cinematic Edit</option>
      </select>
    </div>
  );
}

export default PromptSelector;