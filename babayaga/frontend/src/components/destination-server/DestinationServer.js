import React, { Component } from 'react'
import FormComponent from '../form/FormComponent';
import SchemaComponent from '../schema/SchemaComponent';
// import Axios from 'axios';
import todosData from '../test-data/test';
import SchemaListComponent from "../schema-list/SchemaListComponent"

const formName = 'Destination'

class DestinationServer extends Component {


    constructor() {
        super()
        this.state = {
            hostName: "",
            port: "",
            databaseName: "",
            userName: "",
            password: "",
            schemaName: ""
        }
        this.submited = false;
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.createSource = this.createSource.bind(this)
    }

    handleChange(event) {
        const {name, value} = event.target
        this.setState({
            [name]: value
        })
    }

    handleSubmit(e) {
        console.log('DESTINATION-DATA', this.state)
        this.createSource()
        e.preventDefault();
    }

    createSource(){
        const response = Axios.post('http://localhost:8000/api/schemas', this.state, {
            headers: { 'Content-Type': 'multipart/form-data' },
        })
        this.response = todosData;
        this.schemas = this.response.map(schema => {
            return <SchemaComponent key={schema.id} schema={schema} />
        })
        this.submited = true;
        console.log('res', this.response)
        this.forceUpdate()
    }
    onDragOver(e) {
        console.log(JSON.parse(e.dataTransfer.getData('data')));
    }
    render() {
        if(!this.submited){
            return (
                <FormComponent
                formName={formName}
                handleChange={this.handleChange}
                handleSubmit={this.handleSubmit}
                data={this.state}
                />
            )
        }
        return (
            <div onDragOver={(event)=>event.preventDefault()} onDrop={(e)=>this.onDragOver(e)}>
                <SchemaListComponent schemaList={this.response}></SchemaListComponent>
            </div>
        )

    }
}

export default DestinationServer