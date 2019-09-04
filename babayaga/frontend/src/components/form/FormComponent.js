import React from 'react'
import './FormComponent.scss'

function FormComponent(props) {

        return (
            <form onSubmit={props.handleSubmit}>
                <div className="form-group border-bottom border-danger">
                    <legend className="form-header">{props.formName} Database Details</legend>
                </div>
                <div className="form-row">
                <div className="form-group col">
                    <label className="text-white">Host Name</label>
                    <input 
                        type="text"
                        className="form-control"
                        value={props.data.hostName}
                        name="hostName"
                        aria-describedby="inputGroup-sizing-sm"
                        onChange={props.handleChange}
                        placeholder="Enter Host Name"
                        required
                    />
                </div>
                <div className="form-group col">
                    <label className="text-white">Port</label>
                    <input 
                        type="text"
                        className="form-control"
                        value={props.data.port}
                        name="port"
                        aria-describedby="inputGroup-sizing-sm"
                        onChange={props.handleChange}
                        placeholder="Enter Port Number"
                        required
                    />
                </div>
                </div>
                <div className="form-group">
                    <label className="text-white">Database Name</label>
                        <input 
                            type="text"
                            className="form-control"
                            value={props.data.databaseName}
                            name="databaseName"
                            aria-describedby="inputGroup-sizing-sm"
                            onChange={props.handleChange}
                            placeholder="Enter Database Name"
                            required
                        />
                    </div>
                    <div className="form-group">
                    <label className="text-white">User Name</label>
                        <input 
                            type="text"
                            className="form-control"
                            value={props.data.userName}
                            name="userName"
                            aria-describedby="inputGroup-sizing-sm"
                            onChange={props.handleChange}
                            placeholder="Enter User Name"
                            required
                        />
                    </div>
                    <div className="form-group">
                    <label className="text-white">Password</label>
                        <input 
                            type="text"
                            className="form-control"
                            value={props.data.password}
                            name="password"
                            aria-describedby="inputGroup-sizing-sm"
                            onChange={props.handleChange}
                            placeholder="Enter Password"
                            required
                        />
                    </div>
                    <div className="form-group">
                    <label className="text-white">Schema Name</label>
                        <input 
                            type="text"
                            className="form-control"
                            value={props.data.schemaName}
                            name="schemaName"
                            aria-describedby="inputGroup-sizing-sm"
                            onChange={props.handleChange}
                            placeholder="Enter Schema Name"
                            required
                        />
                    </div>
                    <button className="btn btn-outline-light">Submit</button>
                </form>
        )
}

export default FormComponent