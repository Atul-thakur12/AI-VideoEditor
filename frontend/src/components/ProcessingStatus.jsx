function ProcessingStatus({ loading, status }) {
  if (!status) return null;

  return (
    <div className="mt-6">
      {loading ? (
        <p className="text-yellow-400">{status}</p>
      ) : (
        <p className="text-green-400">{status}</p>
      )}
    </div>
  );
}

export default ProcessingStatus;