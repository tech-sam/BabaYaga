import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import "./modal.scss";
function CustomModal(props) {
    let inputval = "";
  return (
    <Modal
      {...props}
      size="sm"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Schema Name
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <input
          type="text"
          className="form-control"
                  placeholder="Enter schema name to be store"
                  onChange={evt => { inputval = evt.target.value;}}
          required
        />
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={evt=>props.onHide(inputval)}>Submit</Button>
      </Modal.Footer>
    </Modal>
  );
}
export default CustomModal;
