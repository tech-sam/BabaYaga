import React, { Component } from 'react'
import FormComponent from '../form/FormComponent';
import Axios from 'axios';
import SchemaListComponent from "../schema-list/SchemaListComponent";
import { getBaseUrl } from "../../global";
import CustomModal from "../modal/modal"
import Button from "react-bootstrap/Button";
import "./DestinationServer.scss";
import destinationDefault from '../../static-data/static-destination-data.json';


const formName = 'Destination'

class DestinationServer extends Component {


    constructor() {
        super();
        this.state = {
            response: {},
            loadingPage: false,
            showModal: false        }
        this.formValue = {};
        this.submited = false;
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.createSource = this.createSource.bind(this);
        this.onDragOver = this.onDragOver.bind(this);
        this.onHideModal = this.onHideModal.bind(this);
        this.setDefaultValue = this.setDefaultValue.bind(this);
        this.requestData = {};
         this.httpClient = Axios.create();
        this.httpClient.defaults.timeout = 6000000;
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
     return   this.httpClient.post(`${getBaseUrl()}api/schemas`, this.formValue)
        .then((response) => {
            this.setState({ response: response.data });
        });

    }
    onDragOver(e) {
        this.openModal();
        let dragTransferObj = JSON.parse(e.dataTransfer.getData('data'));
        delete dragTransferObj.key;
        const sourceDb = Object.assign({
            "restoreSchema": true,
            "s3Upload": false
        }, dragTransferObj);
        const destinationDb = Object.assign({ schemaName: sourceDb.schemaName }, this.formValue);
        this.requestData = { data: [{ sourceDb }, { destinationDb }] };
       
    }
    openModal() {
        this.setState({ ...this.state, showModal: true });
    }
    onHideModal(val) {
       
        if (val && this.requestData) {
            this.requestData.data[1].destinationDb.updatedSchemaName = val;
            this.setState({ ...this.state, showModal: false, loadingPage: true });
             this.httpClient.post(`${getBaseUrl()}api/dump-schema`, this.requestData)
                .then((response) => {
                    return this.createSource();
                })
                .then(() => {
                    this.setState({ ...this.state, loadingPage: false});
                });
        }
        else {
            this.setState({ showModal: false });
        }
    }
    setDefaultValue() {
        this.submited = true;
        this.setState({ ...this.state, response: destinationDefault });
        
    }
    render() {
        if (!this.submited) {
            return (
                <div>
                    <Button className="btn-default" onClick={evt => { this.setDefaultValue(); }}>
                        Default Destination Database
                    </Button>
                    <FormComponent
                        formName={formName}
                        handleChange={this.handleChange}
                        handleSubmit={this.handleSubmit}
                        data={this.state}
                    />

                </div>
            );
        }
        else {
            return (
                <div onDragOver={(event) => event.preventDefault()} onDrop={(e) => this.onDragOver(e)}>
                    <SchemaListComponent formName={formName} formValue={this.formValue} schemaList={this.state.response} isLoading={this.state.loadingPage}></SchemaListComponent>
                    <CustomModal show={this.state.showModal} onHide={(val) => this.onHideModal(val)}></CustomModal>
                </div>
                
            );
        }

    }
}

export default DestinationServer;