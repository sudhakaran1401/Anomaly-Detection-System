import React from "react";
import PropTypes from "prop-types";

const Message = ({
  type = "success",
  message = "",
  onClose,
}) => {
  if (!message) return null;

  return (
    <div
      className={`alert alert-${type} alert-dismissible fade show`}
      role="alert"
    >
      {message}

      <button
        type="button"
        className="btn-close"
        aria-label="Close"
        onClick={onClose}
      ></button>
    </div>
  );
};

Message.propTypes = {
  type: PropTypes.string,
  message: PropTypes.string,
  onClose: PropTypes.func,
};

export default Message;