import React, { Component } from 'react'
import FormComponent from '../form/FormComponent';
import Axios from 'axios';
import SchemaListComponent from "../schema-list/SchemaListComponent";

const formName = 'Destination'

class DestinationServer extends Component {


    constructor() {
        super();
        this.state = {
            response: {},
            loadingPage: true
        }
        this.formValue = {};
        this.submited = false;
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.createSource = this.createSource.bind(this);
        this.onDragOver = this.onDragOver.bind(this);
    }

    handleChange(event) {
        const {name, value} = event.target
        this.formValue[name] = value;
    }

    handleSubmit() {
        this.createSource();
        this.submited = true;
    }

    createSource(){
     return   Axios.post('http://localhost:8000/api/schemas', this.formValue)
        .then((response) => {
            this.setState({ response: response.data });
        });

    }
    onDragOver(e) {
        let dragTransferObj = JSON.parse(e.dataTransfer.getData('data'));
        delete dragTransferObj.key;
        const sourceDb = Object.assign({
            "restoreSchema": true,
            "s3Upload": false
        }, dragTransferObj);
        const destinationDb = Object.assign({ schemaName: sourceDb.schemaName }, this.formValue);
        const requestData = { data: [{ sourceDb }, { destinationDb }] };
        this.setState({...this.state, loadingPage: true });
        Axios.post('http://localhost:8000/api/dump-schema', requestData)
            .then((response) => { 
                return this.createSource();
            })
            .then(() => {
                this.setState({ ...this.state, loadingPage: false });
            });
    }
    render() {
        if (!this.submited) {
            return (
                <FormComponent
                    formName={formName}
                    handleChange={this.handleChange}
                    handleSubmit={this.handleSubmit}
                    data={this.state}
                />
            );
        }
        else {
            return (
                <div onDragOver={(event) => event.preventDefault()} onDrop={(e) => this.onDragOver(e)}>
                     <SchemaListComponent formName={formName} schemaList={this.state.response} isLoading={this.state.loadingPage}></SchemaListComponent>
                </div>
            );
        }

    }
}

export default DestinationServer;