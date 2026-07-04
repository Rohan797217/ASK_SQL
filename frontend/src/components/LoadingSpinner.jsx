export default function LoadingSpinner() {
  return (
    <div className="message message--assistant">
      <div className="message__bubble message__bubble--assistant">
        <div className="loading">
          <div className="loading__dots">
            <div className="loading__dot" />
            <div className="loading__dot" />
            <div className="loading__dot" />
          </div>
          <span className="loading__text">
            Analyzing question, generating SQL...
          </span>
        </div>
      </div>
    </div>
  )
}
